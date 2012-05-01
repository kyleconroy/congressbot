#!/usr/bin/python

import reddit
import feedparser
import time
from pymongo import Connection

mdb = Connection()
wcdb = mdb.wc
hclc = wcdb.wc_house_today

r = reddit.Reddit(user_agent='WatchingCongress/1.0')
r.login('congressbot', '<BOTPASS>')

hf = feedparser.parse('http://www.govtrack.us/events/events.rss?feeds=misc%3Aintroducedbills')


for entry in hf.entries:
  if (entry['guid'].find('guid')):
    if hclc.find_one({'guid': entry['guid']}) == None:
      record = {'title': entry['title'],
        'description': entry['description'],
        'link': entry['link'],
        'guid': entry['guid']}
      try:
        r.submit('watchingcongress', entry['title'], text=entry['description'] +
          "\n\n[Govtrack.us Summary](" + entry['link'] + ")")
        hclc.insert(record)
      except:
        print "exception occured"
      time.sleep(2)
