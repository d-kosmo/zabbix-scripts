#!/usr/bin/python3.5

import sys
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url_auth = '/api/login'
url_device = '/api/s/default/stat/device'
url_online = '/api/s/default/stat/sta/'
url_users = '/api/s/default/list/user/'
auth = "{'username':'','password':''}"


name = sys.argv[1]
item = sys.argv[2]

s = requests.Session()
s.post(url_auth,data=auth,verify=False)

r = s.get(url_device,verify=False)
l = json.loads(r.text).get('data')

if item == 'network':
    for i in l:
        if i.get('name') == name:
            print(i.get('uplink'))
else:
    for i in l:
        if i.get('name') == name:
            print(i.get(item))

s.close()
