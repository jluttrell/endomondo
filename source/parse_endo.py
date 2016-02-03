import urllib2
import MySQLdb
import simplejson as json
import time
import random
import socket
import sys

con = MySQLdb.connect(host="", user="", passwd="", db="")
con.autocommit(True)

cur = con.cursor()

cur.execute("SELECT workoutId FROM EndoMondoWorkouts LIMIT 1000")
workoutIds = [x[0] for x in cur.fetchall()]

for workoutId in workoutIds:
  cur.execute("SELECT html FROM EndoMondoWorkouts WHERE workoutId='" + str(workoutId) + "'")
  html, = cur.fetchone()
  woutJson = html.split(".draw(")[1].split(");;});")[0]
  print wid,woutJson
  print workoutId
