"""
	Description: Module for collecting NFL data
"""

from beartype import beartype
from sportsipy.nfl.teams import Teams as NFL_Teams
from sportsipy.nba.teams import Teams as NBA_Teams

class Sports():
	"""
		Description: Parent class for sports news
	"""
	@beartype
	def __init__(self, settings: dict ) -> None:
		self.settings = settings
		self.data_dictionary = {}

## Private methods
	@beartype
	def _build_team_dictionary(self, teams) -> dict:
		""" build dictionary of teams using abbreviated team names"""
		team_dict = {}
		for team in teams:
			team_dict[team.abbreviation] = team
			print(team_dict[team.abbreviation])
		return team_dict

class NFL(Sports):
	"""
		Description: Class for retrieving NFL data
	"""

	@beartype
	def __init__(self, settings: dict ) -> None:
		super().__init__(settings)
		self.teams = self.__build_team_dictionary()

	@beartype
	def get_my_teams(self) -> dict:
		"""
			Return my teams information
				- Last game
				- Next game
				- Record
		"""
		my_teams = {}
		for team_abbr in self.settings['sports']['nfl']['teams']:
			team_data = self.teams[team_abbr]
			my_teams[team_abbr] = {}
			my_teams[team_abbr]['name'] = team_data.name
			my_teams[team_abbr]['record'] = f"{ team_data.wins } - {team_data.losses}"

			# Find Next and last game
			next = None
			last = None
			for game in team_data.schedule:
				if game.result is None:
					next = game
					break
				else:
					last = game
			
			my_teams[team_abbr]['last'] = f"{last.date} {last.opponent_name} - {last.result}"
			my_teams[team_abbr]['next'] = f"{next.date} {next.opponent_name}: {self.teams[next.opponent_abbr].wins} - {self.teams[next.opponent_abbr].losses} @ {next.location}"

		print(my_teams)
		return my_teams

## Private methods
	@beartype
	def __build_team_dictionary(self) -> dict:
		""" build dictionary of teams using abbreviated team names"""
		teams = NFL_Teams()
		return self._build_team_dictionary(teams)

class NBA(Sports):
	"""
		Description: Class for retrieving NBA data
	"""

	@beartype
	def __init__(self, settings: dict ) -> None:
		super().__init__(settings)
		self.teams = self.__build_team_dictionary()

	@beartype
	def get_my_teams(self) -> dict:
		"""
			Return my teams information
				- Last game
				- Next game
				- Record
		"""
		my_teams = {}
		for team_abbr in self.settings['sports']['nba']['teams']:
			team_data = self.teams[team_abbr]
			my_teams[team_abbr] = {}
			my_teams[team_abbr]['name'] = team_data.name
			my_teams[team_abbr]['record'] = f"{ team_data.wins } - {team_data.losses}"
			print(team_abbr)

			# Find Next and last game
			next = None
			last = None
			for game in team_data.schedule:
				print(f"{game.result} {game.date} {game.points_scored}")
				if game.points_scored is None:
					next = game
					break
				else:
					last = game
			
			my_teams[team_abbr]['last'] = f"{last.date} {last.opponent_name} - {last.result}"
			my_teams[team_abbr]['next'] = f"{next.date} {next.time} {next.opponent_name}: {self.teams[next.opponent_abbr].wins} - {self.teams[next.opponent_abbr].losses} @ {next.location}"

		print(my_teams)
		return my_teams

## Private methods
	@beartype
	def __build_team_dictionary(self) -> dict:
		""" build dictionary of teams using abbreviated team names"""
		teams = NBA_Teams()
		return self._build_team_dictionary(teams)
