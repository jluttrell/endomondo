import pycurl
import httplib
import socket
import ssl
import cStringIO

import MySQLdb
import simplejson as json
import time
import random
import sys

### EXAMPLE WORKOUT URL ####
# https://www.endomondo.com/users/13820335/workouts/548521615
# users/userID/workouts/workoutID

con = MySQLdb.connect(host="", user="", passwd="", db="")
con.autocommit(True)

cur = con.cursor()

def wait(wt = 0.1):
  time.sleep(wt)

# if not "silk" in socket.gethostname():
#   while (True):
#     x = cur.execute("SELECT COUNT(*) FROM EndoMondoWorkouts")
#     nw = cur.fetchone()[0]
#     x = cur.execute("SELECT COUNT(*) FROM EndoMondoFailures")
#     nf = cur.fetchone()[0]
#     print "EndoMondo:", nw, "workouts", nf, "failures", nw+nf, "total"
#     time.sleep(60)

hostId = int(socket.gethostname().split("silk")[1].split('.')[0]) % 21

if hostId == 0:
  try:
    if (False):
      #cur.execute("DROP TABLE EndoMondoWorkouts")
      cur.execute("DROP TABLE EndoMondoFailures")
    cur.execute("CREATE TABLE EndoMondoWorkouts(workoutId INT, html MEDIUMBLOB) ROW_FORMAT=COMPRESSED")
    cur.execute("CREATE UNIQUE INDEX EndoMondoWorkouts_workoutId ON EndoMondoWorkouts(workoutId)")
    cur.execute("CREATE TABLE EndoMondoFailures(workoutId INT)")
    cur.execute("CREATE UNIQUE INDEX EndoMondoFailures_workoutId ON EndoMondoFailures(workoutId)")
  except Exception as e:
    print e
else:
  time.sleep(0.1)

def getPage(url):
  buf = cStringIO.StringIO()
  c = pycurl.Curl()
  #print url
  c.setopt(c.URL, url)
  c.setopt(c.WRITEFUNCTION, buf.write)
  c.perform()
  s = buf.getvalue()
  return s

  #req = urllib2.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"})
  #f = urllib2.urlopen(req, timeout=5)
  #s = f.read()
  #wait()
  #f.close()
  #return s

for workoutId in xrange(317000000-hostId,0,-21):
  x = cur.execute("SELECT COUNT(*) FROM EndoMondoWorkouts WHERE workoutId='" + str(workoutId) + "'")
  if cur.fetchone()[0] == 1:
    #print "Already got", workoutId
    continue
  x = cur.execute("SELECT COUNT(*) FROM EndoMondoFailures WHERE workoutId='" + str(workoutId) + "'")
  if cur.fetchone()[0] == 1:
    #print "Already failed on", workoutId
    continue
  u = "https://www.endomondo.com/workouts/" + str(workoutId) + '/'
  html = ""
  try:
    html = getPage(u)
  except Exception as e:
    print e
    exit(0)
    pass
  if len(html) == 0 or len(html) == 13703:
    print "Got no data for workout", workoutId
    cur.execute("INSERT INTO EndoMondoFailures (workoutId) VALUES(%(workoutId)s)", {"workoutId":workoutId})
    print "written"
    continue
  print "Got workout", workoutId, "with length", len(html)
  try:
    cur.execute("INSERT INTO EndoMondoWorkouts (workoutId, html) VALUES(%(workoutId)s, %(html)s)", {"workoutId":workoutId, "html":html})
    print "written"
  except Exception as e:
    print e