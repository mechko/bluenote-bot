# Blue Note Robot

Unofficial bot for the famous jazz club of Dresden Neustadt, meant to post daily updates about the evenings live show. Maintained by @mechko. 

Blue Note Website: https://www.jazzdepartment.com/, Mastdon identity: https://dresden.network/@bluenotebot

## Technique

Place MASTODON_ACCESS_TOKEN and MASTODON_ACCOUNT_ID in a .env file, install dependencies via pipenv, and then run

```pipenv run python bluenote-robot.py```

This bot is stateless and designed to boost today's entry if called multiple times within a day (for better timeline visibility). 
