#!/usr/bin/python3.5

import threading
import up_zabbix_api as api
import subprocess
import socket

token = api.zabb_token(api.zabb_url,api.zabb_user,api.zabb_password)

hosts = api.zabb_host(api.zabb_url,token,parametr='hostid')
interfaces = api.zabb_interfaces(api.zabb_url,token,hosts,'type')

ip = []
ping = []
new = []
l = []
dns = []
nodns = []
count = 0

for i in interfaces:
    if i['dns'] == '':
        pass
    else:
        dns.append(i['dns'])
    if i['ip'] == '' or i['ip'] == '127.0.0.1':
        pass
    else:
        ip.append(i['ip'])

for i in range(0,255):
    l.append('192.168.1.' + str(i))
    l.append('192.168.10.' + str(i))
    l.append('192.168.11.' + str(i))

def ping_ip(l,ip,dns):
    for i in l:
        prog = subprocess.call(['/usr/sbin/fping', '-i', '50', '-r', '0', i], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if prog == 0:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a = s.connect_ex((i, 22))
            if a == 0:
                try:
                    name = socket.gethostbyaddr(i)[0]
                    ipi =  socket.gethostbyaddr(i)[2][0]
                    if name in dns or ipi in ip:
                        pass
                    else:
                        ping.append(name)
                except:
                    if i in ip:
                        pass
                    else:
                        nodns.append(i)

e1 = threading.Event()
e2 = threading.Event()
e3 = threading.Event()
e4 = threading.Event()
e5 = threading.Event()
e6 = threading.Event()
e7 = threading.Event()
e8 = threading.Event()

t1 = threading.Thread(target=ping_ip, args=(l[:100], ip, dns))
t2 = threading.Thread(target=ping_ip, args=(l[100:200], ip, dns))
t3 = threading.Thread(target=ping_ip, args=(l[200:300], ip, dns))
t4 = threading.Thread(target=ping_ip, args=(l[300:400], ip, dns))
t5 = threading.Thread(target=ping_ip, args=(l[400:500], ip, dns))
t6 = threading.Thread(target=ping_ip, args=(l[500:600], ip, dns))
t7 = threading.Thread(target=ping_ip, args=(l[600:700], ip, dns))
t8 = threading.Thread(target=ping_ip, args=(l[700:800], ip, dns))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()

e1.set()

t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()

num = len(ping)

with open('/tmp/discovery_linux.json','w') as f:
    f.write('{ "data":[')
    if num != 0:
        for i in ping:
            f.write('{ "{#LINUX}":"' + i + '"}')
            count = count + 1
            if count == num:
                f.write(']}')
            else:
                f.write(',')
    else:
        f.write(']}')

count = 0
with open('/tmp/discovery_linux_awk.json','w') as f:
    f.write('{ "new":{"hosts":[')
    if num != 0:
        for i in ping:
            f.write('"' + i + '"')
            count = count + 1
            if count == num:
                f.write(']}}')
            else:
                f.write(',')
    else:
        f.write(']}}')

num_2 = len(nodns)
count = 0
with open('/tmp/discovery_unknown_ssh.json','w') as f:
    f.write('{ "data":[')
    if num_2 != 0:
        for i in nodns:
            f.write('{ "{#SSH}":"' + i + '"}')
            count = count + 1
            if count == num_2:
                f.write(']}')
            else:
                f.write(',')
    else:
        f.write(']}')

