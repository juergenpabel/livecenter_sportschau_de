#!/usr/bin/python3

import re
import lxml.html
from lxml.cssselect import CSSSelector

def do_redirect(html, filter_date, filter_comp, filter_team):
	current_comp = None
	current_round = None
	current_game = None
	location = None

	gameplan = lxml.html.fromstring(html).find_class("module-gameplan")
	for element in gameplan[0].find("ul"):
		if location is None:
			classes = element.get("class")
			if re.search(r"\bcompetition-head\b", classes):
				current_comp = element.find(".//img").get("title")
			if re.search(r"\bround-head\b", classes):
				current_round = element.find(".//h6").text
			if filter_team is None:
				if re.search(r"\bactivity-head\b", classes):
					if filter_comp is None or filter_comp == current_comp:
						location = element.get("data-audiolivestream")
			else:
				if re.search(r"\bmatch\b", classes):
					if filter_comp is None or filter_comp == current_comp:
						team_home = element.find("div[@class='team-name team-name-home']")
						team_away = element.find("div[@class='team-name team-name-away']")
						if team_home is not None and team_away is not None:
							team_home = team_home.text
							team_away = team_away.text
							game_live = element.get("data-audiolivestream")
							if game_live is not None:
								if filter_team is None or (filter_team == team_home or filter_team == team_away): # full game
									location = game_live
	return location
