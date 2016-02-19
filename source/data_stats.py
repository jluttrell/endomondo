import gzip
import os

def users():
  for userid in users:
    fname = '../data/' + userid + '.txt.gz'

    if os.file.isfile(fname):
      user_count += 1
    else:

def main():
  pkl_file = open('../pickle_files/user_has_hr.pkl', 'rb')
  user_has_hr = pickle.load(pkl_file)
  pkl_file = open('../pickle_files/user_count.pkl', 'rb')
  usertocount = pickle.load(pkl_file)

  thresh = 20
  users = [x for x in user_has_hr.keys() if usertocount[x] > thresh]
  user_count = 0

if __name__ == '__main__':
  main()