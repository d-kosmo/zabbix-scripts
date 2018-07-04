#!/usr/bin/python3
import re
import sys
from settings.settings_asterisk import connect

target = sys.argv[1]
server = sys.argv[2]

response = connect('sip show ' + target,server)
targets = re.sub(' +',' ',response)
targets = targets.split('\n')

del targets[0]
del targets[-3:]

t = []
for tar in targets:
    if tar.split(' ')[0].replace('/','').isdigit():
        pass
    else:
        if target == 'registry':
            t.append(tar.split(' ')[2])
        else:
            t.append(tar.split(' ')[0])

num = len(t)
count = 0

if target == 'peers':
    target = 'trunk'

print('{ "data":[')
if num != 0:
    for i in t:
        print('{ "{#SIP_' + target.upper() + '}":"' + i.replace('reser','reserve').split('/')[0] + '"}')
        count = count + 1
        if count == num:
            print(']}')
        else:
            print(',')
else:
    print(']}')

