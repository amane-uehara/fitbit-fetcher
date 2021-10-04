import os
import sys
import json

def daily_base_item_list():
  return [
    'activityCalories',
    'caloriesBMR',
    'calories',
    'elevation',
    'floors',
    'minutesFairlyActive',
    'minutesLightlyActive',
    'minutesSedentary',
    'minutesVeryActive',
    'steps'
  ]


def main(args):
  if len(args) != 2 :
    print('USAGE :: python3 minute_kpi.py /path/to/raw_root_dir yyyymmdd')
    return

  raw_root = args[0]
  if not os.path.exists(raw_root) :
    print('invalid raw_root_path: ' + raw_root)
    return

  yyyymmdd = args[1]
  if int(yyyymmdd) < 10000000 or 30000000 < int(yyyymmdd) :
    print('invalid yyyymmdd: ' + yyyymmdd)
    return

  item_dict = {'day' : yyyymmdd}
  for item in daily_base_item_list():
    filename = os.path.join(raw_root, item + '_1m', yyyymmdd + '.json')
    data = read_json_file(filename)
    item_dict[item] = int(data['activities-' + item][0]['value'])

  filename = os.path.join(raw_root, 'distance_1m', yyyymmdd + '.json')
  data = read_json_file(filename)
  item_dict['distance'] = round(float(data['activities-distance'][0]['value']) * 1609.344) # mile to meter

  filename = os.path.join(raw_root, 'heart_1m', yyyymmdd + '.json')
  data = read_json_file(filename)
  for d in data['activities-heart'][0]['value']['heartRateZones']:
    zone = d['name'].replace(' ','')
    for metric in ['caloriesOut', 'max', 'min', 'minutes']:
      key = ('heart_' + zone + '_' + metric).lower()
      item_dict[key] = int(d[metric])

  filename = os.path.join(raw_root, 'sleep_1m', yyyymmdd + '.json')
  data = read_json_file(filename)

  for total in ['totalSleepRecords', 'totalTimeInBed', 'totalMinutesAsleep']:
    item_dict['sleep_' + total] = int(data['summary'][total])

  for stage in ['deep', 'light', 'rem', 'wake']:
    if 'stages' in data['summary']:
      item_dict['sleep_' + stage] = int(data['summary']['stages'][stage])
    else:
      item_dict['sleep_' + stage] = ''

  print(json.dumps(item_dict, separators=(',', ':')))


def read_json_file(filename):
  if not os.path.isfile(filename):
    sys.exit('Error: file:`' + filename + '` not found')

  raw_file = open(filename, 'r')
  data = json.load(raw_file)
  raw_file.close()
  return data


if __name__ == '__main__':
  main(sys.argv[1:])
