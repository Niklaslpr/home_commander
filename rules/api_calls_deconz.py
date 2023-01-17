import requests
import json
from main.views import DECONZ_URL, API_KEY, DECONZ_GROUPS_URL, DECONZ_DEVICE_LIGHTS_URL
DECONZ_SCHEDULE_URL = DECONZ_URL + "/api/" + API_KEY + "/schedules"

def createSchedule(time, groupID):

    print(time)
    data = '{"command": { "address": "/api/546117A96A/groups/1/action", "method": "PUT", "body": { "on" : true}}, "time" : "' + time + '"}'
    url = 'http://192.168.178.49/api/546117A96A/schedules'
    p = requests.post(url, data=data)
    print(p.status_code)
    print(p.content)

def createRule(rule_name, rule_device, rule_time, rule_days):
    print("Infos: ", rule_name, rule_device, rule_time, rule_days)
    if rule_device.split("_")[0] == "group":
        rule_device = rule_device.split("_")[1]     #TODO rule_days to Bitmap
        data = '{"name": "' + rule_name + '" , "command": {"address": "' + DECONZ_GROUPS_URL + '/' + rule_device + '/action", "method": "PUT", "body": { "on": true, "hue": 8738, "sat": 158 } },"autodelete": false ,"localtime": "2023-01-17T' + rule_time + ':00 "}'
    elif rule_device.split("_")[0] == "device":
        rule_device = rule_device.split("_")[1]
        data = '{"name": "' + rule_name + '" , "command": {"address" }}'
    
    print(data)
    
    
    url = DECONZ_SCHEDULE_URL
    response = requests.post(url, data = data)
    print(response.status_code)
    print(response.content)
    
    
    
   
    
    return ("true")

