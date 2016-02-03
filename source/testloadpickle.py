import pickle

pkl_file = open('user_count.pkl', 'rb')
user_count = pickle.load(pkl_file)

pkl_file = open('user_to_workout.pkl', 'rb')
user_to_workout = pickle.load(pkl_file)

pkl_file = open('user_has_hr.pkl', 'rb')
user_has_hr = pickle.load(pkl_file)

print len(user_count)
print len(user_to_workout)
print len(user_has_hr)