#!/usr/bin/python3.5

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url_auth = ""
url = "/api/s/default/stat/device"
data = "{'username':'','password':''}"

s = requests.Session()
s.post(url_auth,data=data,verify=False)
r = s.get(url,verify=False)
l = json.loads(r.text).get('data')

num = len(l)
count = 0

print('{ "data":[')
if num != 0:
    for i in l:
        print('{ "{#UNIFI}":"' + i.get('name') + '",')
        print(' "{#IP}":"' + i.get('ip') + '",')
        print(' "{#MAC}":"' + i.get('mac') + '"}')
        count = count + 1
        if count == num:
            print(']}')
        else:
            print(',')
else:
    print(']}')

s.close()

