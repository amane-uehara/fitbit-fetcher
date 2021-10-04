import os
import sys
import json

def detail_base_item_list():
  return [
    'distance',
    'elevation',
    'floors',
    'heart',
    'minutesFairlyActive',
    'minutesLightlyActive',
    'minutesSedentary',
    'minutesVeryActive',
    'steps'
  ]


def read_json_file(filename):
  if not os.path.isfile(filename):
    sys.exit('Error: file:`' + filename + '` not found')

  raw_file = open(filename, 'r')
  data = json.load(raw_file)
  raw_file.close()
  return data


def parse_item(raw_root, item, grad, yyyymmdd):
  filename = os.path.join(raw_root, item + '_' + grad, yyyymmdd + '.json')
  data = read_json_file(filename)
  tmp = data['activities-' + item + '-intraday']['dataset']

  result = {}
  for d in tmp:
    hhmm = d['time'].replace(':', '')[0:4]
    result[hhmm] = d
    del result[hhmm]['time']

  return result


def parse_sleep(raw_root, grad, yyyymmdd):
  filename = os.path.join(raw_root, 'sleep_' + grad, yyyymmdd + '.json')
  data = read_json_file(filename)
  tmp = []
  sleep = data['sleep']
  for part in sleep:
    tmp = tmp + part['minuteData']

  result = {}
  for d in tmp:
    hhmm = d['dateTime'].replace(':', '')[0:4]
    result[hhmm] = d
    del result[hhmm]['dateTime']

  return result


def hhmm_list(grad):
  result = []

  if grad == '1m':
    for h in range(24):
      for m in range(60):
        result.append('%02d%02d' % (h,m))

  elif grad == '15m':
    for h in range(24):
      for m15 in range(4):
        result.append('%02d%02d' % (h,m15*15))

  return result


def item_join(item_dict, grad):
  result ={}
  for hhmm in hhmm_list(grad):
    tmp = {}
    for key in item_dict.keys():
      if hhmm in item_dict[key].keys():
        tmp[key] = item_dict[key][hhmm]
      else:
        tmp[key] = {}
    result[hhmm] = tmp

  return result


def simplify(joined_dict, grad, yyyymmdd):
  item_list = detail_base_item_list()
  item_list.append('sleep')
  item_list.remove('distance')

  result = []
  for hhmm in hhmm_list(grad):
    d = joined_dict[hhmm]
    tmp = {}
    tmp['dt'] = yyyymmdd + hhmm + '00'

    for item in item_list:
      tmp[item] = int(d[item]['value']) if ('value' in d[item].keys()) else ''

    tmp['distance']       = float(d['distance']['value']) if ('value' in d['distance'].keys()) else ''
    tmp['calories_level'] = int(  d['calories']['level']) if ('level' in d['calories'].keys()) else ''
    tmp['calories_mets' ] = int(  d['calories']['mets' ]) if ('mets'  in d['calories'].keys()) else ''
    tmp['calories_value'] = float(d['calories']['value']) if ('value' in d['calories'].keys()) else ''

    # mile to meter
    tmp['distance']       = round(tmp['distance'] * 1609.344, 4)
    tmp['calories_value'] = round(tmp['calories_value'], 4)

    result.append(tmp)

  return result
