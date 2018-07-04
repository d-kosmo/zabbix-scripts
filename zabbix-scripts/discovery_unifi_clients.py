#!/usr/bin/python3.5

import sys
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

wap = sys.argv[1]

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url_auth = '/api/login'
url = '/api/s/default/stat/sta/'
url_wap = ':8443/api/s/default/stat/device'
data = "{'username':'','password':''}"

s = requests.Session()
s.post(url_auth,data=data,verify=False)
r_wap = s.get(url_wap,verify=False)
l_wap = json.loads(r_wap.text).get('data')
r = s.get(url,verify=False)
l = json.loads(r.text).get('data')

for i in l_wap:
    if i.get('name') == wap:
        mac = i.get('mac')
count = 0
clients = []
print('{ "data":[')
for i in l:
    if i.get('ap_mac') == mac and i.get('essid') == '':
        clients.append('{ "{#CLIENT}":"' + str(i.get('hostname')) + '",  "{#CLIENT_MAC}":"' + i.get('mac') + '",  "{#CLIENT_IP}":"' + i.get('ip') + '"}')
num = len(clients)
if num == 0:
    print(']}')
else:
    for i in clients:
        print(i)
        count = count + 1
        if count == num:
            print(']}')
        else:
            print(',')

s.close()

