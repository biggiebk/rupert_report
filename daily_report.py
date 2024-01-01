#!/usr/bin/env python3.11
from rupert_report import RupertReportWeather, RupertReportSports

rrw = RupertReportWeather("cfg/settings.json")
rrw.build('weather.md.j2', 'weather.md')

rrs = RupertReportSports("cfg/settings.json")
rrs.build('sports.md.j2', 'sports.md')