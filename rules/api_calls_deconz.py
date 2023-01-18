import requests
import json
from datetime import datetime, timedelta
from main.views import DECONZ_URL, API_KEY, DECONZ_GROUPS_URL, DECONZ_DEVICE_LIGHTS_URL
DECONZ_SCHEDULE_URL = DECONZ_URL + "/api/" + API_KEY + "/schedules"


def createSchedule(time, groupID):

    print(time)
    data = '{"command": { "address": "/api/546117A96A/groups/1/action", "method": "PUT", "body": { "on" : true}}, "time" : "' + time + '"}'
    url = 'http://192.168.178.49/api/546117A96A/schedules'
    p = requests.post(url, data=data)
    print(p.status_code)
    print(p.content)

def createRule(rule_name, rule_group, rule_time, rule_days):
    print("Infos: ", rule_name, rule_group, rule_time, rule_days)
    
    # First: Create Scene "on" for Group
    data = '{"name" : "on"}'
    url = DECONZ_GROUPS_URL + '/' + rule_group + '/scenes'
    response = requests.post(url, data = data)
    print(response.status_code)
    print(response.content)
    if response.status_code == '200':
        response = response.json()
        response = response[0]
        scene_id = response["success"]["id"]
    else:
         scene_id = '1'
    print("second:")
    # Second: Modify Scene --> State of Lights in Group to {"on": true, "hue": 8738, "sat": 158}
    response = requests.get(DECONZ_GROUPS_URL + '/' + rule_group)
    group_lights = response.json()["lights"]
    for element in group_lights:
        data = '{"bri": 254, "on": true, "xy": [0.46, 0.48], "transitiontime": 10}'
        url  = DECONZ_GROUPS_URL + '/' + rule_group + '/scenes/' + scene_id + '/lights/' + element + '/state'
        response = requests.put(url, data = data)
        print(response.status_code)
        print(response.content)
    
    
    # Third: create schedule --> call scene
            #TODO rule_days to Bitmap
            
    rule_date = datetime.today() + timedelta(days=1)
    rule_date = rule_date.strftime('%Y-%m-%d')
    
    data = '{"name": "' + rule_name + '", "command": {"address": "' + '/api/' + API_KEY + '/groups/' + rule_group + '/scenes/' + scene_id + '/recall", "method": "PUT", "body": {} },"autodelete": false,"localtime": "' + rule_date + 'T' + rule_time + ':00"}'
    print(data)
    url = DECONZ_SCHEDULE_URL
    response = requests.post(url, data = data)
    print(response.status_code)
    print(response.content)
    
    
    
   
    
    return ("true")


def deleteRule(rule_id):
    print("ACHTUNG LÖSCHEN:",  
