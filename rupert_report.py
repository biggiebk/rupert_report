"""
	Description: Module file for working with reports.
"""
import os
import subprocess
import requests
import json
from beartype import beartype
from jinja2 import Environment, PackageLoader, select_autoescape
from nfl import NFL

class RupertReport():
	"""
		Description: Class for generating reports in via JINJA2 templates
	"""
	@beartype
	def __init__(self, settings_file: str ) -> None:
		""" Construct for DocMarkJson """
		self.settings_file = settings_file
		self.settings = {}
		self.__load_settings()
		self.data_dictionary = {}

	@beartype
	def build(self, template_file, saved_output) -> None:
		"""
			Builds the mark down files
		"""
		self.git_ready(self.settings['repos']['daily_report']['remote'], self.settings['repos']['daily_report']['local'])
		env = Environment( loader=PackageLoader("rupert_report"), autoescape=select_autoescape())
		template = env.get_template(template_file)
		with open(f"{self.settings['repos']['daily_report']['local']}/{self.settings['repos']['daily_report']['sub_folder']}/{saved_output}", "w",
		encoding='utf-8')as markdown_file:
			markdown_file.write(template.render(self.data_dictionary))
		markdown_file.close()
		self.git_push(self.settings['repos']['daily_report']['local'], self.settings['repos']['daily_report']['sub_folder'], saved_output)

	@beartype
	def git_push(self, local: str, sub_folder: str, file: str) -> None:
		"""
			Add files/dirs and push to remote
		"""
		# Add file
		subprocess.run([f"git -C {local} add {sub_folder}/{file}"], shell=True)
		subprocess.run([f"git -C {local} commit -m 'Update today.md'"], shell=True)
		subprocess.run([f"git -C {local} push"], shell=True)

	@beartype
	def git_ready(self, remote: str, local: str) -> None:
		"""
			Clone remote repo if local does not exist, otherwise run pull to sync local
		"""
		# Does local exist?
		if os.path.exists(local):
			subprocess.run([f"git -C {local} switch main"], shell=True)
			subprocess.run([f"git -C {local} pull"], shell=True)
		else:
			subprocess.run([f"git clone {remote} {local}"], shell=True)

	@beartype
	def __load_settings(self) -> None:
		"""
			Responsible for:
				1. Loading settings
			Requires:
				settings_file - Path to the synapses setting file
		"""
		with open(self.settings_file, 'r', encoding='utf-8') as settings:
			settings_json = settings.read()
		self.settings = json.loads(settings_json)

class RupertReportWeather(RupertReport):
	"""
		Description: Class for generating daily news/updates
	"""

	@beartype
	def build(self, template_file, saved_output) -> None:
		self.data_dictionary['title'] = 'Weather'
		self.data_dictionary['risenset'] = self.rise_n_set(self.settings['location']['longitude'], self.settings['location']['latitude'])
		self.data_dictionary['weather'] = {}
		self.data_dictionary['weather']['today'] = self.weather(self.settings['location']['longitude'], self.settings['location']['latitude'])
		self.data_dictionary['weather']['tomorrow'] = self.weather(self.settings['location']['longitude'], self.settings['location']['latitude'])
		print(self.data_dictionary)
		super().build(template_file, saved_output)

	@beartype
	def rise_n_set(self, longitude: float, latitude: float) -> dict:
		session = requests.Session()
		session.headers.update({'User-Agent': self.settings['web']['user-agent']})
		print((f"https://api.sunrisesunset.io/json?lng={longitude}&lat={latitude}"))
		results = session.get(f"https://api.sunrisesunset.io/json?lng={longitude}&lat={latitude}")
		data = json.loads(results.content)
		rise_n_set = {}
		rise_n_set['dawn'] = data['results']['dawn']
		rise_n_set['sunrise'] = data['results']['sunrise']
		rise_n_set['sunset'] = data['results']['sunset']
		rise_n_set['dusk'] = data['results']['dusk']
		rise_n_set['solar_noon'] = data['results']['solar_noon']
		rise_n_set['golden_hour'] = data['results']['golden_hour']
		rise_n_set['day_length'] = data['results']['day_length']
		rise_n_set['first_light'] = data['results']['first_light']
		rise_n_set['last_light'] = data['results']['last_light']
		return rise_n_set

	@beartype
	def weather(self, longitude: float, latitude: float):
		# https://api.weather.gov/points/38.06355895008784%2C-122.16322946135749

		#ID STO X 13 Y 50
		#https://api.weather.gov/gridpoints/STO/13,50

		weather = {}
		weather['high'] = 58
		weather['low'] = 43
		weather['cor'] = 12
		return weather

class RupertReportSports(RupertReport):
	"""
		Description: Class for generating daily sports info
	"""

	@beartype
	def build(self, template_file, saved_output) -> None:
		self.data_dictionary['title'] = 'Sports'
		self.data_dictionary['nfl'] = self.__nfl()
		print(self.data_dictionary)
		super().build(template_file, saved_output)

	@beartype
	def __nfl(self) -> dict:
		""" Build NFL info """
		nfl = NFL(self.settings)
		return nfl.get_my_teams()