#!/usr/bin/env python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python39_app]
# [START gae_python3_app]
import datetime
import requests
from flask import Flask
from flask import request as flask_request
from flask import Response as flask_response
from flask import redirect as flask_redirect
from flask import abort as flask_abort
from podcast import do_podcast
from redirect import do_redirect

app = Flask(__name__)
url = "https://livecenter.sportschau.de"


def fetch_html(date):
	return requests.get( url+"/dn"+date ).text


@app.route('/', methods=['GET'])
def index():
	return flask_redirect("https://github.com/juergenpabel/livecenter_sportschau_de", 302)


@app.route('/livestreams/podcast', methods=['GET'])
def podcast():
	podcast_title = flask_request.args.get("title", default="Sportschau Livecenter", type=str)
	filter_date = flask_request.args.get("date", default=datetime.date.today().strftime("%Y-%m-%d"), type=str)
	filter_comp = flask_request.args.get("comp", default=None, type=str)
	filter_team = flask_request.args.get("team", default=None, type=str)

	html = fetch_html(filter_date)
	xml = do_podcast(flask_request.url, url, html, podcast_title, filter_date, filter_comp, filter_team)
	return flask_response(xml, mimetype='text/xml')

@app.route('/livestreams/redirect', methods=['GET'])
def redirect():
	filter_date = flask_request.args.get("date", default=datetime.date.today().strftime("%Y-%m-%d"), type=str)
	filter_comp = flask_request.args.get("comp", default=None, type=str)
	filter_team = flask_request.args.get("team", default=None, type=str)

	html = fetch_html(filter_date)
	location = do_redirect(html, filter_date, filter_comp, filter_team)
	if location is None:
		return flask_abort(404)
	return flask_redirect(location, 302)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8888, debug=True)
# [END gae_python3_app]
# [END gae_python39_app]
