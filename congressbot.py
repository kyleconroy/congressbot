#!/usr/bin/python
import logging
import feedparser
import time
from jinja2 import Template
from pymongo import Connection
from reddit import Reddit

mongo_db = Connection()
congress_db = mongo_db.wc
house_collection = congress_db.wc_house_today

template = Template(open('post_template.md').read())


def parse():
    govfeed = feedparser.parse('http://www.govtrack.us/events/events.rss?'
                               'feeds=misc%3Aintroducedbills')

    r = Reddit(user_agent='WatchingCongress/1.0')
    r.login('congressbot', '<BOTPASS>')

    for entry in govfeed.entries:
        if not entry['guid'].find('guid'):
            logging.info("Couldn't find GUID")
            continue

        if not entry['title']:
            logging.info("No title for bill: {}".format(entry['guid']))
            continue

        if house_collection.find_one({'guid': entry['guid']}):
            logging.info("Already created story: {}".format(entry['title']))
            continue

        if 'duty' in entry['title'] and 'temporar' in entry['title']:
            logging.info("Ignored boring bill: {}".format(entry['title']))
            continue

        if '.Res' in entry['title']:
            logging.info("Ignored resolution: {}".format(entry['title']))
            continue

        record = {
            'title': entry['title'],
            'description': entry['description'],
            'link': entry['link'],
            'guid': entry['guid'],
        }

        try:
            text = template.render(description=entry['description'],
                                   link=entry['link'])
            r.submit('watchingcongress', entry['title'], text=text)
            house_collection.insert(record)
            logging.info("Created story: {}".format(entry['title']))
        except Exception as e:
            logging.error("Exception occured: {}".format(unicode(e)))
            time.sleep(2)


if __name__ == '__main__':
    parse()
