#!/usr/bin/env python3

import datetime
import urllib
import pathlib
import json
import re
import lxml.html
from lxml.cssselect import CSSSelector
from feedgen.feed import FeedGenerator


def do_podcast(url, html, filter_date, filter_comp, filter_team):
	fg = FeedGenerator()
	fg.generator( "python" )
	fg.load_extension( "podcast" )
	fg.title( "Sportschau Livestreams" )
	fg.podcast.itunes_category( "Sports" )
	fg.description( "Applied filters: date=%s competition=%s team=%s" % (filter_date, filter_comp, filter_team) )
	fg.link( href=url, rel="self" )


	gameplan = lxml.html.fromstring( html ).find_class( "module-gameplan" )

	current_comp = None
	current_round = None
	current_game = None
	for element in gameplan[0].find( "div" ):
		classes = element.get("class")
		if re.search(r"\bcompetition-head\b", classes):
			current_comp = element.find(".//img").get("title")
		if re.search(r"\bround-head\b", classes):
			current_round = element.find(".//div[@class='match-round']").text
		if re.search(r"\bactivity-head\b", classes):
			if filter_comp is None or filter_comp == current_comp:
				if filter_team is None and element.find(".//div[@class='match-activity']") is not None:
					conf_name = element.find(".//div[@class='match-activity']").get("data-audiolivestream_title")
					conf_live = element.find(".//div[@class='match-activity']").get("data-audiolivestream")
					conf_info = element.find(".//a[@class='hs-conference-link']").get("href")
					fe = fg.add_entry()
					fe.id( conf_live )
					fe.title( conf_name )
					fe.description( conf_name )
					fe.link( href=url + conf_info )
					fe.enclosure( conf_live, 0, "audio/mpeg" )
		if re.search(r"\bmatch\b", classes):
			if filter_comp is None or filter_comp == current_comp:
				team_home = element.find( "div[@class='team-name team-name-home']" )
				team_away = element.find( "div[@class='team-name team-name-away']" )
				if team_home is not None and team_away is not None:
					team_home = team_home.text
					team_away = team_away.text
					game_info = element.find( "div[@class='match-more']/a" ).get("href")
					game_live = element.get("data-audiolivestream")
					if game_live is not None:
						if filter_team is None or (filter_team == team_home or filter_team == team_away): # full game
							fe = fg.add_entry()
							fe.id( game_live )
							fe.title( team_home + " - " + team_away )
							fe.description( current_comp + ", " + current_round + ": " + team_home + " - " + team_away )
							fe.link( href=url + game_info )
							fe.enclosure( game_live, 0, "audio/mpeg" )

	return fg.rss_str().decode()
