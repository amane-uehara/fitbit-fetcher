# -*- coding: utf-8 -*-
import sys
import os
import datetime
import fitbit
from ast import literal_eval
import requests

def main(args):
  # ---------- PARSE ARGS ----------
  if len(args) != 5 :
    print("USAGE :: python3 fetch_json_files.py /path/to/save_dir yyyymmdd client_id client_secret /path/to/token.txt" )
    return

  save_root = args[0]
  if not os.path.exists(save_root) :
    print("invalid save_root_path: " + save_root)
    return

  yyyymmdd  = args[1]
  if int(yyyymmdd) < 10000000 or 30000000 < int(yyyymmdd) :
    print("invalid yyyymmdd: " + yyyymmdd)
    return
  yyyy_mm_dd = yyyymmdd[0:4] + '-' + yyyymmdd[4:6] + '-' + yyyymmdd[6:8]

  client_id     = args[2]
  client_secret = args[3]

  token_file    = args[4]
  if not os.path.exists(token_file) :
    print("token file <<<" + token_file + ">>> not found")
    return

  # ---------- INITIALIZE FITBIT ----------
  tokens = open(token_file).read()
  token_dict = literal_eval(tokens)
  access_token = token_dict['access_token']
  refresh_token = token_dict['refresh_token']

  client = fitbit.Fitbit(
    client_id
    , client_secret
    , access_token = access_token
    , refresh_token = refresh_token
    , refresh_cb = updateToken
  )

  # ---------- INTRA_TIME_SERIES ----------
  intra_time_series_list = [
    {'resource': 'activities/heart'               , 'detail_level': '1sec', 'save_path': save_root + '/heart_1s'                 },

    {'resource': 'activities/heart'               , 'detail_level': '1min', 'save_path': save_root + '/heart_1m'                 },
    {'resource': 'activities/calories'            , 'detail_level': '1min', 'save_path': save_root + '/calories_1m'              },
    {'resource': 'activities/caloriesBMR'         , 'detail_level': '1min', 'save_path': save_root + '/caloriesBMR_1m'           },
    {'resource': 'activities/steps'               , 'detail_level': '1min', 'save_path': save_root + '/steps_1m'                 },
    {'resource': 'activities/distance'            , 'detail_level': '1min', 'save_path': save_root + '/distance_1m'              },
    {'resource': 'activities/floors'              , 'detail_level': '1min', 'save_path': save_root + '/floors_1m'                },
    {'resource': 'activities/elevation'           , 'detail_level': '1min', 'save_path': save_root + '/elevation_1m'             },
    {'resource': 'activities/minutesSedentary'    , 'detail_level': '1min', 'save_path': save_root + '/minutesSedentary_1m'      },
    {'resource': 'activities/minutesLightlyActive', 'detail_level': '1min', 'save_path': save_root + '/minutesLightlyActive_1m'  },
    {'resource': 'activities/minutesFairlyActive' , 'detail_level': '1min', 'save_path': save_root + '/minutesFairlyActive_1m'   },
    {'resource': 'activities/minutesVeryActive'   , 'detail_level': '1min', 'save_path': save_root + '/minutesVeryActive_1m'     },
    {'resource': 'activities/activityCalories'    , 'detail_level': '1min', 'save_path': save_root + '/activityCalories_1m'      },

    {'resource': 'activities/heart'               , 'detail_level': '15min', 'save_path': save_root + '/heart_15m'               },
    {'resource': 'activities/calories'            , 'detail_level': '15min', 'save_path': save_root + '/calories_15m'            },
    {'resource': 'activities/caloriesBMR'         , 'detail_level': '15min', 'save_path': save_root + '/caloriesBMR_15m'         },
    {'resource': 'activities/steps'               , 'detail_level': '15min', 'save_path': save_root + '/steps_15m'               },
    {'resource': 'activities/distance'            , 'detail_level': '15min', 'save_path': save_root + '/distance_15m'            },
    {'resource': 'activities/floors'              , 'detail_level': '15min', 'save_path': save_root + '/floors_15m'              },
    {'resource': 'activities/elevation'           , 'detail_level': '15min', 'save_path': save_root + '/elevation_15m'           },
    {'resource': 'activities/minutesSedentary'    , 'detail_level': '15min', 'save_path': save_root + '/minutesSedentary_15m'    },
    {'resource': 'activities/minutesLightlyActive', 'detail_level': '15min', 'save_path': save_root + '/minutesLightlyActive_15m'},
    {'resource': 'activities/minutesFairlyActive' , 'detail_level': '15min', 'save_path': save_root + '/minutesFairlyActive_15m' },
    {'resource': 'activities/minutesVeryActive'   , 'detail_level': '15min', 'save_path': save_root + '/minutesVeryActive_15m'   },
    {'resource': 'activities/activityCalories'    , 'detail_level': '15min', 'save_path': save_root + '/activityCalories_15m'    }
  ]

  for item in intra_time_series_list:
    if not os.path.exists(item['save_path']) :
      os.makedirs(item['save_path'])

    json_data = client.intraday_time_series(item['resource'], base_date=yyyy_mm_dd, detail_level=item['detail_level'])
    json_filename = item['save_path'] + '/' + yyyymmdd + '.json'
    f = open(json_filename, 'w')
    f.write(str(json_data))
    f.close()

  # ---------- SLEEP MIN ----------
  save_path_sleep_min = save_root + '/sleep_1m'
  if not os.path.exists(save_path_sleep_min) :
    os.makedirs(save_path_sleep_min)

  json_data = client.sleep(date=yyyy_mm_dd)
  f = open(save_path_sleep_min + '/' + yyyymmdd + '.json', 'w')
  f.write(str(json_data))
  f.close()

  # ---------- SLEEP DAY ----------
  save_path_sleep_day = save_root + '/sleep_1d'
  if not os.path.exists(save_path_sleep_day) :
    os.makedirs(save_path_sleep_day)

  headers = {"Authorization": "Bearer " + access_token}
  url = "https://api.fitbit.com/1.2/user/-/sleep/date/" + yyyy_mm_dd  + "/" + yyyy_mm_dd + ".json"
  response = requests.get(url, headers=headers)

  if "Too" in str(response.json()):
    print("fetch sleep_day failed")

  else:
    f = open(save_path_sleep_day + '/' + yyyymmdd + '.json', 'w')
    f.write(str(response.json()))
    f.close()




def updateToken(token):
  f = open(token_file, 'w')
  f.write(str(token))
  f.close()
  return

if __name__ == '__main__':
  main(sys.argv[1:])
