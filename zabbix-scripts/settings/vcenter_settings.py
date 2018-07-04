#!/usr/bin/python3.5
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

url = ""
login = ""
password = ""
url_ds = "https://vcenter/rest/vcenter/datastore"

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_id():
    r = requests.post(url,headers={'Content-Type':'application/json', 'Accept':'application/json', 'vmware-use-header-authn':'test', 'vmware-api-session-id':'null'}, auth=(login,password),verify=False)

