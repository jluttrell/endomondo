import os.path
import time
import cPickle as pickle
import numpy as np
import gzip
from datetime import datetime
import sys

fromfile = False

if fromfile:
  dir_home = '../data/'
  suffix = '.txt.gz'
  weather_key = 'weather'
  sport_key = 'sport'
else:
  dir_home = '../pkl_data/'
  suffix = '.pkl'
  weather_key = 'weather_key'
  sport_key = 'sport_key'

def readGz(f):
  for l in gzip.open(f):
    try: #skips first line of files that aren't dicts
      yield eval(l)
    except:
      pass

#returns list of all user workouts from text file
def getWorkoutsFromText(text_filename):
  w = []
  for l in readGz(text_filename):
    w.append(l)
  return w

#returns list of all user workouts from pkl file
def getWorkoutsFromPickle(pkl_filename):
  pkl_file = open(pkl_filename, 'rb')
  w = pickle.load(pkl_file)
  return w

#returns number of workouts that have heartrate data
def numHRWorkouts(workouts):
  hr_count = 0
  for w in workouts:
    if w['heart_rate_max']:
      hr_count += 1
  return hr_count

def getFreq(dates):
  f = []
  for i in range(len(dates)-1):
    f.append( (dates[i+1]-dates[i]).days )
  return f

def getSportsAndWeathers(workouts):
  s = set()
  w = set()

  for wo in workouts:
    if wo[weather_key] != None:
      if fromfile:
        w.add(wo[weather_key]['type'])
      else:
        w.add(wo[weather_key])
    if wo[sport_key] != None:
      s.add(wo[sport_key])
  return s, w

if __name__ == '__main__':
  print "Starting @ ",
  print time.strftime("%Y-%m-%d %H:%M:%S")

  if fromfile:
    pkl_file = open('../pickle_files/user_has_hr.pkl', 'rb')
    user_has_hr = pickle.load(pkl_file)
    pkl_file = open('../pickle_files/user_count.pkl', 'rb')
    user_count = pickle.load(pkl_file)

    thresh = 10
    users = [x for x in user_has_hr.keys() if user_count[x] > thresh]
  else:
    pkl_file = open('../pickle_files/all_usersnames_031216.pkl')
    users = pickle.load(pkl_file)

  user_count = 0
  total_num_hr = 0
  num_of_workouts = []
  per_w_hr = []
  all_frequencies = []
  longest_freq = 0
  all_date_ranges = []
  all_sports = set()
  all_weathers = set()
  earliest_date = datetime.max
  latest_date = datetime.min

  print "On user:",
  sys.stdout.flush()

  for u in users:
    if(user_count % 100 == 0):
      print user_count,
      sys.stdout.flush()

    filepath = dir_home + u + suffix

    #check if user file exists
    if fromfile and not os.path.isfile(filepath):
      continue

    if fromfile:
      workouts = getWorkoutsFromText(filepath)
    else:
      workouts = getWorkoutsFromPickle(filepath)

    if fromfile and len(workouts) < 100:
      continue

    user_count += 1
    num_of_workouts.append(len(workouts))

    ### DATETIME STUFF
    dates = [datetime.strptime(w['start_time'], "%Y-%m-%dT%H:%M:%S.000Z") for w in workouts]
    dates.sort()
    
    if dates[0] < earliest_date:
      earliest_date = dates[0]

    if dates[-1] > latest_date:
      latest_date = dates[-1]

    date_range_days = (dates[-1] - dates[0]).days
    all_date_ranges.append(date_range_days)

    freq = getFreq(dates)
    all_frequencies.append(np.average(freq))
    maxfreq = max(freq)
    if maxfreq > longest_freq:
      longest_freq = maxfreq

    ### HEARTRATE STUFF
    num_hr = numHRWorkouts(workouts)
    total_num_hr += num_hr
    per_hr = 1.0*num_hr/len(workouts)
    per_w_hr.append(per_hr) 

    ### SPORT/WEATHER STUFF
    s,w = getSportsAndWeathers(workouts)
    all_sports.update(s)
    all_weathers.update(w)

  avg_num_workouts = np.average(num_of_workouts)
  std_num_workouts = np.std(num_of_workouts)
  max_num_workouts = max(num_of_workouts)
  min_num_workouts = min(num_of_workouts)

  overall_per_w_hr = 1.0*total_num_hr/sum(num_of_workouts)
  avg_w_hr = np.average(per_w_hr)
  std_w_hr = np.std(per_w_hr)

  avg_datespan = np.average(all_date_ranges)
  avg_avgfreq = np.average(all_frequencies)
  std_avgfreq = np.std(all_frequencies)
  max_avgfreq = max(all_frequencies)
  min_avgfreq = min(all_frequencies)

  print "\n\n-----STATS-----"
  print "Number of users = %d" %(user_count)
  print "Workouts per user: avg = %d, std dev = %d" %(avg_num_workouts, std_num_workouts)
  print "Max workouts = %d, min workouts = %d" %(max_num_workouts, min_num_workouts)
  print "Percent of all workouts w/ hr data: %f" %(overall_per_w_hr)
  print "Average %" + " of user workouts w/ hr data: %f" %(avg_w_hr)
  print "Std dev %" + " of user workouts w/ hr data: %f" %(std_w_hr)

  print "Dates range from %s to %s" %(str(earliest_date),str(latest_date))
  print "Average date span of user = %f (days)" %avg_datespan

  print 'Freq of use: avg = %f, std = %f, max = %f, min = %f' %(avg_avgfreq, std_avgfreq, max_avgfreq, min_avgfreq)
  print 'Longest gap between workouts = %d' %(longest_freq)
  print 'Number of different sports = %d' %len(all_sports)
  print 'Number of different weather types = %d' %len(all_weathers)

  print "Done @ ",
  print time.strftime("%Y-%m-%d %H:%M:%S")