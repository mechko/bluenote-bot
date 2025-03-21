"""
This is a (very) simple bot meant to post daily updates about live shows in Dresden Neustadt's jazzclub Blue Note. 

@author: mechko
@date: June 2024

Usage: pipenv run python bluenote-robot.py
"""
import os
from dotenv import load_dotenv
from ics import Calendar
import requests
from mastodon import Mastodon
from datetime import datetime

load_dotenv()

bluenote_ics = "https://www.bluenote-dresden.de/bluenoteics.ics"
mastodon_access_token = os.getenv('MASTODON_ACCESS_TOKEN')
mastodon_account_id = os.getenv('MASTODON_ACCOUNT_ID')
mastodon_url = "https://dresden.network"

if not mastodon_access_token: 
    print("Mastodon token not provided, aborting. ")
    quit()

if not mastodon_account_id: 
    print("Mastodon account ID not provided, aborting. ")
    quit()

mastodon = Mastodon(
    access_token=mastodon_access_token,
    api_base_url=mastodon_url
)

# Because this bot is stateless, we need to check for the current timeline first.
# If there is an update that was posted earlier today, we just boost this exsisting update.
mode_boost_only = False

statuses = mastodon.account_statuses(id=mastodon_account_id, limit = 3)
today = datetime.now().date()

for status in statuses:
    created_date = status.created_at.date()
    print("Checking status from " + str(created_date))
    if created_date == today:
        print("Boosting status with id " + str(status.id))
        mastodon.status_reblog(status.id)
        mode_boost_only = True


# If there was no update today yet, we go check if there's something in the calendar for today.
if not mode_boost_only:
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
        print(status)
        mastodon.status_post(status + " #dresden #neustadt #jazz #music")
    else:
        print("No events found for today.")
