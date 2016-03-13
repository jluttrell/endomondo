import time
import cPickle as pickle
import numpy as np
from datetime import datetime
import sys

dir_home = '../pkl_data/'
suffix = '.pkl'

latest_date = datetime()

buckets = [30,60,90,120,150,180]
number_buckets = len(buckets)
total_count = np.zeros(number_buckets)
bucket_vote = np.zeros(number_buckets)

def calculate(dates):
  v_delta = np.zeros(number_buckets)
  t_delta = np.zeros(number_buckets)

  for i in range(len(dates-1)):
    gap = (dates[i+1] - dates[i]).days

    for b in buckets:
      if gap < b:
        t_delta += 1
        v_delta += 1

#returns list of all user workouts from pkl file
def getWorkoutsFromPickle(pkl_filename):
  pkl_file = open(pkl_filename, 'rb')
  w = pickle.load(pkl_file)
  return w

pkl_file = open('../pickle_files/all_usersnames_031216.pkl')
users = pickle.load(pkl_file)

for u in user:
  filepath = dir_home + u + suffix
  wo = getWorkoutsFromPickle(filepath)
  dates = [datetime.strptime(w['start_time'], "%Y-%m-%dT%H:%M:%S.000Z") for w in workouts]
  dates.sort()

  vote_delta, total_delta = calculate(dates)