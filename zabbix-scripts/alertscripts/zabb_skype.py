#!/usr/bin/python3

import requests
import json
import sys

client_id = ''
client_secret = ''

user_id = sys.argv[1]
message_1 = sys.argv[2]
message_2 = sys.argv[3]
param = sys.argv[4]

message = "<b>" + message_1 + "</b><br/>" + message_2.replace("OK","<b>OK</b>").replace("PROBLEM","<b>PROBLEM</b>")

def get_access_token(client_id, client_secret):
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://api.botframework.com/.default',
        'grant_type': 'client_credentials'
        }
    r = requests.post("https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token", data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        response = json.loads(r.text)
        return response['access_token']
    except:
        return False

def send_message(user_id, token, message):
    if param == 'private':
        url = 'https://apis.skype.com/v2/conversations/8:' + user_id + '/activities'
    else:
        url = 'https://apis.skype.com/v2/conversations/19:' + user_id + '/activities'
    headers = dict(Authorization='Bearer ' + token)
    data = json.dumps(dict(message=dict(content=message))).encode()
    requests.post(url, headers=headers, data=data)

token = get_access_token(client_id, client_secret)

send_message(user_id, token, message)

