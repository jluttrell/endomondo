import gzip
import numpy as np
import operator
from collections import defaultdict
import pickle
import time

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

pkl_file = open('user20_hr_ids.pkl', 'rb')
userids = pickle.load(pkl_file)

filename = "../../Data/endomondo1.txt.gz"

f = open('20workouts_withhr.txt', 'w')

print "Working..."
i = 0

for l in readGz(filename):
  if i % 100000 == 0:
    print time.strftime("%Y-%m-%d %H:%M:%S"),
    print "\tIteration %d" %i

  userid = l['user_id']
  if userid in userids:
    f.write(str(l))
    f.write('\n')
  i += 1

f.close()