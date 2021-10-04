import os
import sys
import json
from lib_parse_json import *

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

  item_dict = {}
  for item in detail_base_item_list():
    item_dict[item] = parse_item(raw_root, item, '1m', yyyymmdd)
  item_dict['calories'] = parse_item(raw_root, 'calories', '1m', yyyymmdd)
  item_dict['sleep'] = parse_sleep(raw_root, '1m', yyyymmdd)

  #print(json.dumps(item_dict))
  joined_dict = item_join(item_dict, '1m')
  simplified_dict = simplify(joined_dict, '1m', yyyymmdd)
  print(json.dumps(simplified_dict, separators=(',', ':')))


if __name__ == '__main__':
  main(sys.argv[1:])
