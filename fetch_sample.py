# -*- coding: utf-8 -*-
import fitbit
from ast import literal_eval

client_id     = '******'
client_secret = '********************************'
token_file    = '/path/to/token.txt'
yyyy_mm_dd    = '2021-08-29'

tokens = open(token_file).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']

def updateToken(token):
  f = open(token_file, 'w')
  f.write(str(token))
  f.close()
  return

client = fitbit.Fitbit(client_id, client_secret, access_token = access_token, refresh_token = refresh_token, refresh_cb = updateToken)

# heart
heart_alldata = client.intraday_time_series('activities/heart', base_date=yyyy_mm_dd, detail_level='1sec')
heart = heart_alldata['activities-heart-intraday']['dataset']
print(heart)

# walk
steps_alldata = client.intraday_time_series('activities/steps', base_date=yyyy_mm_dd, detail_level='1min')
steps = steps_alldata['activities-steps-intraday']['dataset']
print(steps)

# sleep
sleep = client.sleep(date=yyyy_mm_dd)
print(sleep)
