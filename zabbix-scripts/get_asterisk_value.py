#!/usr/bin/python3

import sys
import re
import json
from settings.settings_asterisk import connect, connect_calls

if len(sys.argv) == 2:
    server = sys.argv[1]
    test_connection = connect('core show help',server)
    if type(test_connection) is list:
        print(test_connection[1])
        sys.exit()
    else:
        print(1)
else:
    target = sys.argv[1]
    item = sys.argv[2]
    server = sys.argv[3]

    test_connection = connect('core show help',server)

    if type(test_connection) is list and item != 'active calls':
        print(test_connection[1])
        sys.exit()

    if item == 'status':
        target = target.split(',')
        targets = []
        for i in target:
            status = connect('sip show peer ' + i,server)
            status = re.sub(' +',' ',status).split('\n')
            del status[0:2]
            del status[-3:]
            status = dict((i.split(':')[0].replace(' ',''),i.split(':')[1]) for i in status)
            if re.search(' OK ',status['Status']):
                targets.append(1)
            else:
                targets.append(0)
        if 0 in targets:
            print(0)
        else:
            print(1)

    elif item == 'active calls':
        calls = connect_calls('core show channels concise',server)
        calls = re.findall('\nSIP/' + target,calls)
        print(len(calls))

    elif item == 'registration':
        status = connect('sip show registry',server)
        status = re.sub(' +',' ',status).split('\n')
        del status[0]
        del status[-3:]
        num = len(status)
        count = 1 
        for i in status:
            if i.split(' ')[2] == target:
                if i.split(' ')[4] == 'Registered':
                    print(1)
                    break
                else:
                    print(0)
                    break
            elif i.split(' ')[2] != target and count == num:
                print(0)
            count = count + 1
