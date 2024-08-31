"""
This is a (very) simple bot meant to post daily updates about live shows in Dresden Neustadt's jazzclub Blue Note. 

@author: mechko
@date: June 2024

Usage: pipenv run python bluebote-robot.py
"""
import os
from dotenv import load_dotenv
from ics import Calendar
import requests
from mastodon import Mastodon

load_dotenv()

bluenote_ics = "https://www.jazzdepartment.com/web/bluenoteics.ics"
mastodon_access_token = os.getenv('MASTODON_ACCESS_TOKEN')
mastodon_url = "https://dresden.network"

if not mastodon_access_token: 
    print("Mastodon token not provided, aborting. ")
    quit()

status = ""

try:
    ics_content = requests.get(bluenote_ics).text
    c = Calendar(ics_content)
    for e in c.timeline.today():    
        status += "Heute um " + e.begin.to('local').format("HH") + " Uhr im Blue Note: "
        status += e.name
        status += " https://" + e.description + "\n"
except:
    pass

if status:
    mastodon = Mastodon(
        access_token=mastodon_access_token,
        api_base_url=mastodon_url
    )

    print(status)
    mastodon.status_post(status + " #dresden #neustadt #jazz #music")
else:
    print("No events found for today.")
