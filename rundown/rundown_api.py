import os
import sys
import requests
import json
import time


RUNDOWN_ACCESS = os.environ['RUNDOWN_KEY']
HOST = 'therundown-therundown-v1.p.rapidapi.com'


def refresh_affiliates():
	"""Make an API call to the Rundown API for a list of offered sportsbooks"""
	path = 'https://' + HOST + '/affiliates'
	r = requests.get(path, headers={ "X-RapidAPI-Host": HOST, "X-RapidAPI-Key": RUNDOWN_ACCESS})
	with open('affiliates.txt', 'w+') as f:
		f.write(json.dumps(r.json(), indent=4, sort_keys=True))


def refresh_sports():
	"""Make an API call to the Rundown API for a list of offered sports"""
	path = 'https://' + HOST + '/sports'
	r = requests.get(path, headers={ "X-RapidAPI-Host": HOST, "X-RapidAPI-Key": RUNDOWN_ACCESS})
	sports_data = r.json()
	for s in sports_data['sports']:
		path = 'https://' + HOST + '/sports/' + str(s['sport_id']) + '/dates?format=epoch'
		r = requests.get(path, headers={ "X-RapidAPI-Host": HOST, "X-RapidAPI-Key": RUNDOWN_ACCESS})
		s['dates'] = r.json()['dates']

	with open('sports.txt', 'w+') as f:
		f.write(json.dumps(sports_data, indent=4, sort_keys=True))

	return r.json()


if __name__ == '__main__':
	refresh_affiliates()
	refresh_sports()
	