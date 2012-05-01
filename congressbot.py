#!/usr/bin/python
import logging
import reddit
import feedparser
import time
from pymongo import Connection

mongo_db = Connection()
congress_db = mongo_db.wc
house_collection = congress_db.wc_house_today

r = reddit.Reddit(user_agent='WatchingCongress/1.0')
r.login('congressbot', '<BOTPASS>')

govfeed = feedparser.parse('http://www.govtrack.us/events/events.rss?'
                           'feeds=misc%3Aintroducedbills')

POST_TEMPLATE = """
{description}

[Govtrack.us Summary]({link})
"""

for entry in govfeed.entries:

    if not entry['guid'].find('guid'):
        continue

    if house_collection.find_one({'guid': entry['guid']}):
        continue

    record = {
        'title': entry['title'],
        'description': entry['description'],
        'link': entry['link'],
        'guid': entry['guid'],
    }

    try:
        text = SELF_POST.format(description=entry['description'],
                                link=entry['link'])
        r.submit('watchingcongress', entry['title'], text=text)
        house_collection.insert(record)
        logging.info("Created story: {}".format(entry['title']))
    except Exception as e:
        logging.error("Exception occured: {}".format(unicode(e)))
        time.sleep(2)
