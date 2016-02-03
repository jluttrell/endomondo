###curl -sL -A "uname -sp" http://jmcauley.ucsd.edu/data/endomondo1.txt.gz | zcat | head -n 1000 > test.txt

import gzip
import numpy as np
import operator
from collections import defaultdict
import pickle
import time

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

user_count = defaultdict(int)
user_to_workout = defaultdict(list)
user_has_hr = defaultdict(bool)

#for l in readGz("endomondo1.txt.gz"):
filename = "../../Data/endomondo1.txt.gz"

print "Working..."
i = 0

for l in readGz(filename):
  if i % 100000 == 0:
    print time.strftime("%Y-%m-%d %H:%M:%S"),
    print "\tIteration %d" %i

  userid = l['user_id']
  workoutid = l['workout_id']

  if l['Distance'] != '-' and float(l['Distance'].split(' ')[0].replace(',','')) >= .1:
    user_count[userid] += 1
    user_to_workout[userid].append(workoutid)
    if "hr" in l:
      user_has_hr[userid] = True
  i += 1

### Pickle shit ###
#pkl_file = open('data.pkl', 'rb')

usercount = open('user_count.pkl', 'wb')
userworkout = open('user_to_workout.pkl', 'wb')
userhashr = open('user_has_hr.pkl', 'wb')

pickle.dump(user_count, usercount)
pickle.dump(user_to_workout, userworkout)
pickle.dump(user_has_hr, userhashr)

print "\n\nNumber of users = %d" %len(user_count)

print "Max user count = %d" %max(user_count.values())
print "mean user count = %f" %np.mean(np.asarray(user_count.values()))

for num_workouts in range(10,150,10):
  print "Number of users with more than %d workouts = %d" %(num_workouts,sum(i > num_workouts for i in user_count.values()))

print "Number of heart rate data = %d" %sum(user_has_hr.values())