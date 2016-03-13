import httplib
import simplejson as json
import time
import requests
import pickle
import gzip

tags = ['id','sport','duration','distance','weather','start_time','speed_max', \
        'speed_avg','heart_rate_zones','heart_rate_max','heart_rate_avg','altitude_min', \
        'altitude_max','ascent','descent','hydration','calories','points']

start_date = '2000-01-01'
end_date = '2016-01-01'

#save_dir = '/media/jluttrell/Seagate Expansion Drive/endo_data/'
save_dir = '../data/'

def getWorkoutIDs(userid, start_date, end_date):
  url = 'https://www.endomondo.com/rest/v1/users/' + userid + \
        '/workouts?before=' + end_date + 'T06%3A59%3A59.999Z&after=' + \
        start_date + 'T07%3A00%3A00.000Z'
  try:
    page = requests.get(url)
  except:
    print "EERROR: Request to get %s workouts failed" %(userid)

  try:
    data = json.loads(page.content)
  except:
    return []
    
  ids = [x['id'] for x in data]
  return ids

def wait(wt = 0.1):
  time.sleep(wt)

def extract(datum):
  clean = dict()
  for t in tags:
    if t in datum:
        clean[t] = datum[t]
    else:
      clean[t] = None
  return clean

def connect(url):
  c = httplib.HTTPSConnection(url)
  return c

def scrap(users, start_date, end_date):

  domain = "www.endomondo.com"
  #conn = httplib.HTTPSConnection(domain)
  conn = connect(domain)
  start = 690
  end = len(users)
  user_count = 0
  failures = 0
  failure_thresh = 5

  for userid in users[start:end]:
    user_count += 1
    print time.strftime("%Y-%m-%d %H:%M:%S"),
    #wait()
    workouts = getWorkoutIDs(userid, start_date, end_date)
    
    if len(workouts) == 0:
      print "%s has 0 workouts" %(userid)
      print "Waiting %d seconds..." %(60)
      wait(60)
      continue
    
    print "\t(%d/%d) user %s has %d workouts" %(user_count, (end-start), userid, len(workouts))
    first = True

    fd = gzip.open(save_dir + userid + '.txt.gz', 'w')

    for workoutid in workouts:
      target = '/rest/v1/users/' + str(userid) + '/workouts/' + str(workoutid)

      try:
        conn.request("GET", target)
        resp = conn.getresponse()
        j = json.loads(resp.read())
        failures = 0
      except:
        print time.strftime("%Y-%m-%d %H:%M:%S"),
        print "FAILED: (%d/%d) Unable to connect - user %s, workoutid %s" %(failures, failure_thresh, userid, workoutid)
        failures += 1
        w = failures*10
        print "Waiting %d seconds..." %(w)

        wait(w)
        conn = connect(domain)
        if failures > failure_thresh:
          failures = 0
          print "Unable to connect to %s" %(userid)
          print "Waiting %d seconds..." %(300)
          wait(300)
          conn = connect(domain)
          break
        else:
          continue

      clean_data = extract(j)
      
      if first:
        fd.write(userid + " ")
        fd.write(str(j['author']['gender']) + '\n')
        first = False

      fd.write(str(clean_data).encode('ascii'))
      fd.write('\n')

      wait()

    fd.close()

def main():
  print "Starting @ ", 
  print time.strftime("%Y-%m-%d %H:%M:%S")

  pkl_file = open('../pickle_files/user_has_hr.pkl', 'rb')
  user_has_hr = pickle.load(pkl_file)
  pkl_file = open('../pickle_files/user_count.pkl', 'rb')
  user_count = pickle.load(pkl_file)

  print "Date range from %s to %s" %(start_date, end_date)

  thresh = 20
  old_users = [x for x in user_has_hr.keys() if user_count[x] > thresh]

  thresh = 10
  new_users = [x for x in user_has_hr.keys() if user_count[x] > thresh]
  
  users = [x for x in new_users if x not in old_users]

  print "LETS BEGIN: ",
  print time.strftime("%Y-%m-%d %H:%M:%S")

  scrap(users, start_date, end_date)
  print time.strftime("%Y-%m-%d %H:%M:%S"),
  print " Done!"
  
if __name__ == '__main__':
  main()