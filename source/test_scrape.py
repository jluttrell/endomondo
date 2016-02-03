import pycurl
import httplib
import socket
import ssl
import cStringIO
import urllib2
import simplejson as json
import time
import random
import sys

def getPage(url):
  buf = cStringIO.StringIO()
  c = pycurl.Curl()
  #print url
  c.setopt(c.URL, url)
  c.setopt(c.WRITEFUNCTION, buf.write)
  c.perform()
  s = buf.getvalue()
  return s

def scrapeUrl(html):
  woutJson = html.split(".draw(")[1].split(");;});")[0]
  print woutJson
  #print workoutId

u = "https://www.endomondo.com/users/5965732/workouts/325058038"
try:
  html = getPage(u)
except Exception as e:
  print e
  exit(0)

print html
print "done"
#scrapeUrl(html)

https://www.endomondo.com/rest/v1/users/5965732/workouts?before=2014-05-15T06%3A59%3A59.999Z&after=2014-03-28T07%3A00%3A00.000Z

from lxml import html
import requests
page = requests.get('https://www.endomondo.com/users/13820335/workouts/571864306')
tree = html.fromstring(page.content)

content = tree.xpath('//div[@class="workoutStat-value ng-binding"]/text()')
labels = tree.xpath('//div[@class="workoutStat-name ng-binding"]/text()')
dictionary = dict(zip(labels,content))

w = tree.xpath('//div[@class="workoutStat-value workoutStat-value--weather ng-binding"]/text()')
dictionary['Weather'] = w[0]