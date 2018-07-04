#!/usr/bin/python3.5

import threading
import up_zabbix_api as api
import subprocess
import json
import itertools as it

token = api.zabb_token(api.zabb_url,api.zabb_user,api.zabb_password)
path = '/tmp/discovery_routers.json'
r_id = api.zabb_group(api.zabb_url,token,'Routers')
host_id = api.zabb_host(api.zabb_url,token,r_id,'hostid')
exceptions = []
r_maybe = []
zabb_routers = []

def file_json(ip,path):
    file_js.write(json.dumps({'{#ROUTER_LANIP}':str(ip)},sort_keys=True, indent=4))
    file_js.write("\n,")

for host in host_id:
    b = api.zabb_interfaces(api.zabb_url,token,host,'routers','ip')
    zabb_routers.append(b)

for i in range(0,256):
    r_maybe.append('192.168.' + str(i) + '.1')

for i in range(0,128):
    for j in it.chain(range(0,16), range(90,100)):
        r_maybe.append('10.' + str(i) + '.' + str(j) +  '.1')

e = set(set(r_maybe) - set(zabb_routers) - set(exceptions))
e = list(e)
new_routers = []

def ping_ip(e,new_routers):
        for i in e:
            prog = subprocess.call(['/usr/sbin/fping', '-i', '50', '-r', '0', i], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if prog == 0:
            snmp = subprocess.call(['snmpget', '-c', 'community', '-v', '2c', i, 'sysDescr.0'],stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if snmp == 0:
                new_routers.append(i)

e1 = threading.Event()
e2 = threading.Event()
e3 = threading.Event()
e4 = threading.Event()
e5 = threading.Event()
e6 = threading.Event()
e7 = threading.Event()
e8 = threading.Event()
e9 = threading.Event()
e10 = threading.Event()

t1 = threading.Thread(target=ping_ip, args=(e[:360],new_routers))
t2 = threading.Thread(target=ping_ip, args=(e[360:720],new_routers))
t3 = threading.Thread(target=ping_ip, args=(e[720:1080],new_routers))
t4 = threading.Thread(target=ping_ip, args=(e[1080:1440],new_routers))
t5 = threading.Thread(target=ping_ip, args=(e[1440:1800],new_routers))
t6 = threading.Thread(target=ping_ip, args=(e[1800:2160],new_routers))
t7 = threading.Thread(target=ping_ip, args=(e[2160:2520],new_routers))
t8 = threading.Thread(target=ping_ip, args=(e[2520:2880],new_routers))
t9 = threading.Thread(target=ping_ip, args=(e[2880:3240],new_routers))
t10 = threading.Thread(target=ping_ip, args=(e[3240:3600],new_routers))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()

e1.set()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
t9.join()
t10.join()

file_js = open(path,'w')
file_js.write("{\n\x22data\x22:[\n")

for i in new_routers:
    file_json(i,path)

file_js.close()
file_js = open(path,'ab')
file_js.truncate(file_js.tell() - 1)
file_js.close()
file_js = open(path,'a')
file_js.write("\n]\n}")
file_js.close()
