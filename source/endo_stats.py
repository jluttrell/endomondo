import os.path
import time
import pickle
import gzip
from datetime import datetime

dir_home = '../data/'

month_to_days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

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

#returns number of workouts that have heartrate data
def numHRWorkouts(workouts):
  hr_count = 0
  for w in workouts:
    if w['heart_rate_max']:
      hr_count += 1
  return hr_count

#returns number of days b/t first and last workout
def spanOfWorkout(sorted_dates):
  delta = sorted_dates[0] - sorted_dates[-1]
  return delta.days

def dateSpan(early, late):
  pass    

if __name__ == '__main__':
  pkl_file = open('../pickle_files/user_has_hr.pkl', 'rb')
  user_has_hr = pickle.load(pkl_file)
  pkl_file = open('../pickle_files/user_count.pkl', 'rb')
  user_count = pickle.load(pkl_file)

  thresh = 20
  users = [x for x in user_has_hr.keys() if user_count[x] > thresh]

  user_count = 0
  user_data = []

  for u in users[0:1]:
    filepath = dir_home + u + '.txt.gz'

    #check if user file exists
    if not os.path.isfile(filepath):
      continue

    workouts = getUserWorkouts(filepath)
    dates = [datetime.strptime(w['start_time'], "%Y-%m-%dT%H:%M:%S.000Z") for w in workouts]
    sorted(dates)

    user_count += 1