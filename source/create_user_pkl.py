import os.path
import time
import pickle
import cPickle
import numpy as np
import gzip
from datetime import datetime
import time
import sys

#rename 's/^pkl_data//' *.pkl

dir_home = '../data/'

def readGz(f):
  for l in gzip.open(f):
    try: #skips first line of files that aren't dicts
      yield eval(l)
    except:
      pass

#returns list of all user workouts 
def getUserWorkouts(fn):
  w = []
  for l in readGz(fn):
    w.append(l)
  return w

def cleanData(userid, workouts):
  ret = []
  for workout in workouts:
    new_workout = {}
    new_workout['user_id'] = userid
    for key in workout.keys():
      if key == 'id':
        new_workout['workout_id'] = workout['id']
      elif key == 'duartion':
        new_workout['duration_in_seconds'] = workout['duration']
        new_workout['duration'] = time.strftime('%H:%M:%S', time.gmtime(workout['duration']))
      elif key == 'points':
        if workout['points'] != None:
          if 'points' in workout['points']:
            new_workout['time_series_data'] = workout['points']['points']
          else:
            new_workout['points'] = None
        else:
          new_workout['points'] = None
      elif key == 'speed_max':
        if workout['speed_max'] != None:
          new_workout['speed_max'] = workout['speed_max']
        else:
          if workout['points'] != None:
            if 'points' in workout['points']:
              new_workout['speed_max'] = getMaxSpeed(workout['points']['points'])
          else:
            new_workout['speed_max'] = None
      elif key == 'weather':
        if workout['weather'] != None:
          new_workout['weather_key'] = workout['weather']['type']
        else:
          new_workout['weather_key'] = None
      elif key == 'sport':
        new_workout['sport_key'] = workout['sport']
      else:
        new_workout[key] = workout[key]
    ret.append(new_workout)
  return ret

def getMaxSpeed(points):
  maxspeed = 0
  for point in points:
    if 'speed' in point:
      if point['speed'] > maxspeed:
        maxspeed = point['speed']
  return maxspeed

print "Starting @ ",
print time.strftime("%Y-%m-%d %H:%M:%S")

pkl_file = open('../pickle_files/user_has_hr.pkl', 'rb')
user_has_hr = pickle.load(pkl_file)
pkl_file = open('../pickle_files/user_count.pkl', 'rb')
user_count = pickle.load(pkl_file)

thresh = 10
users = [x for x in user_has_hr.keys() if user_count[x] > thresh]

user_count = 0
all_usersnames = []

print "On user:"
user_count = 0

for user in users:
  if(user_count % 10 == 0):
    print '\t' + str(user_count)

  filepath = dir_home + user + '.txt.gz'

  #check if user file exists
  if not os.path.isfile(filepath):
    continue

  try:
    workouts = getUserWorkouts(filepath)
  except:
    print "workouts for user %s failed to get workouts" %(user)

  if len(workouts) < 100:
    continue

  user_count += 1
  all_usersnames.append(user)

  clean_data = cleanData(user, workouts)

  pkl_filename = '../pkl_data/' + user + '.pkl'
  userpkl = open(pkl_filename, 'wb')
  cPickle.dump(clean_data, userpkl)
  userpkl.close()

alluserspkl = open('all_usersnames_031216.pkl', 'wb')
cPickle.dump(all_usersnames, alluserspkl)

print "Number of users = %d" %user_count
print "Len of all_usersnames = %d" %len(all_usersnames)