#!/usr/bin/env python3.11
from rupert_report import DailyRupertReport

drr = DailyRupertReport("cfg/settings.json")

drr.build('weather.md.j2', 'weather.md')