#!/usr/bin/python3.5

import json
import subprocess
import ldap3
import up_zabbix_api as api

server = ldap3.Server()
user = ""
password = ""
cn = ""
servers = []
hosts_lower = []
live = []

conn = ldap3.Connection(server,user=user,password=password)
conn.bind()
conn.search(cn,"(&(objectCategory=computer)(OperatingSystem=*Server 201*)(!(cn=*test*))(!(cn=*wfc_0*)))",attributes=["cn"])
token = api.zabb_token(api.zabb_url,api.zabb_user,api.zabb_password)
hosts = api.zabb_host(api.zabb_url,token,parametr='host')
exception = []

for host in hosts:
    hosts_lower.append(host.lower())

for i in conn.response:
    g = i['dn'].split(',')
    if set(g).isdisjoint(set(exception)):
        servers.append(str(i['attributes']['cn']).lower())
    else:
        pass

servers = set(servers) - set(hosts_lower)

for server in servers:
    prog = subprocess.call(['/usr/sbin/fping', '-i', '50', '-r', '0', str(server)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if prog == 0:
        live.append('{ "{#SRV_NAME}": "' + str(server) + '" }')
    else:
        pass

print('{"data":\n' + str(live).replace("'","") + '\n}')

