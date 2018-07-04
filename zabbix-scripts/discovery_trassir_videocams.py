#!/usr/bin/python3.5

import sys
import re
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

server = str(sys.argv[1])
password = ""
link="https://" + server + ":8080/objects/?password=" + password
r = requests.get(link,verify=False)
d = []
m = (r.text.split('/*')[0])
n = (json.loads(m))
print('{\n"data": [')
for i in n:
    if i.get('class') == 'Channel':
        d.append('\t{\n\t\t"{#NAME}": ' + '"' + (re.sub(r'\n','',i.get('name'))) + '"\n\t},')
d[-1] = re.sub(r',','',d[-1])
for i in d:
    print(i)

print(']\n}')

