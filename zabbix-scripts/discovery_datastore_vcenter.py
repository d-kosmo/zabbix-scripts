#!/usr/bin/python3.5

import json
import requests
from settings import vcenter_settings as vs

ids = vs.get_id()

r = requests.get(vs.url_ds,headers={'Accept':'application/json','vmware-api-session-id':ids},verify=False)
print('{ "data":[')
a = (len(r.json().get('value')))
b = 0
for i in r.json().get('value'):
    print('{ "{#DATASTORE}":"' + i.get('name') + '"}')
    b = b + 1
    if b == a:
        print(']}')
    else:
        print(',')

