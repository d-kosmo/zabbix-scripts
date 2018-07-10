#!/usr/bin/python3.5

import sys
import json
import requests
from settings import vcenter_settings as vs

ids = vs.get_id()
url = '/rest/vcenter/datastore'
space = sys.argv[1]
key = sys.argv[2]

r = requests.get(url,headers={'Accept':'application/json','vmware-api-session-id':ids},verify=False)
for i in r.json().get('value'):
    if i.get('name') == space:
        if key == 'used':
            print(int(i.get('capacity'))-int(i.get('free_space')))
        else:
            print(i.get(key))
