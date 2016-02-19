import os.path
import time
import pickle
import numpy as np
import gzip
from datetime import datetime
import time

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

#returns number of workouts that have heartrate data
def numHRWorkouts(workouts):
  hr_count = 0
  for w in workouts:
    if w['heart_rate_max']:
      hr_count += 1
  return hr_count

#returns number of days b/t first and last workout
def spanOfDates(sorted_dates):
  delta = sorted_dates[-1] - sorted_dates[0]
  return delta.days

if __name__ == '__main__':
  print "Starting @ ",
  print time.strftime("%Y-%m-%d %H:%M:%S")

  pkl_file = open('../pickle_files/user_has_hr.pkl', 'rb')
  user_has_hr = pickle.load(pkl_file)
  pkl_file = open('../pickle_files/user_count.pkl', 'rb')
  user_count = pickle.load(pkl_file)

  thresh = 10
  users = [x for x in user_has_hr.keys() if user_count[x] > thresh]

  user_count = 0
  total_num_hr = 0
  num_of_workouts = []
  per_w_hr = []
  all_frequencies = []

  for u in users[0:100]:
    if(user_count == 0):
      "On user: 1, ",
      sys.stdout.flush()
    elif(user_count % 10 == 0):
      print user_count,
      sys.stdout.flush()

    filepath = dir_home + u + '.txt.gz'

    #check if user file exists
    if not os.path.isfile(filepath):
      continue

    user_count += 1

    workouts = getUserWorkouts(filepath)

    if len(workouts) < 100:
      continue

    num_of_workouts.append(len(workouts))

    dates = [datetime.strptime(w['start_time'], "%Y-%m-%dT%H:%M:%S.000Z") for w in workouts]
    dates.sort()
    
    num_hr = numHRWorkouts(workouts)
    total_num_hr += num_hr
    per_hr = 1.0*num_hr/len(workouts)
    per_w_hr.append(per_hr) 

  avg_num_workouts = np.average(num_of_workouts)
  std_num_workouts = np.std(num_of_workouts)
  max_num_workouts = max(num_of_workouts)
  min_num_workouts = min(num_of_workouts)

  overall_per_w_hr = 1.0*total_num_hr/sum(num_of_workouts)
  avg_w_hr = np.average(per_w_hr)
  std_w_hr = np.std(per_w_hr)

  print "\n\n-----STATS-----"
  print "Number of users = %d" %(user_count)
  print "Workouts per user: avg = %d, std dev = %d" %(avg_num_workouts, std_num_workouts)
  print "Max workouts = %d, min workouts = %d" %(max_num_workouts, min_num_workouts)
  print "Percent of all workouts w/ hr data: %f" %(overall_per_w_hr)
  print "Average %" + " of user workouts w/ hr data: %f" %(avg_w_hr)
  print "Std dev %" + " of user workouts w/ hr data: %f" %(std_w_hr)

  print "Done @ ",
  print time.strftime("%Y-%m-%d %H:%M:%S")