import requests
import json
from datetime import datetime, timedelta
from activities.models import LogEntry
from main.views import DECONZ_URL, API_KEY, DECONZ_GROUPS_URL, DECONZ_DEVICE_LIGHTS_URL
DECONZ_SCHEDULE_URL = DECONZ_URL + "/api/" + API_KEY + "/schedules"


def createSchedule(time, groupID):

    print(time)
    data = '{"command": { "address": "/api/546117A96A/groups/1/action", "method": "PUT", "body": { "on" : true}}, "time" : "' + time + '"}'
    url = 'http://192.168.178.49/api/546117A96A/schedules'
    p = requests.post(url, data=data)
    print(p.status_code)
    print(p.content)

def createRule(rule_name, rule_group, rule_time, rule_days, repeat_rule):
    # First: Create Scene "on" for Group
    data = '{"name" : "on"}'
    url = DECONZ_GROUPS_URL + '/' + rule_group + '/scenes'
    response = requests.post(url, data = data)
    if response.status_code == '200':
        response = response.json()
        response = response[0]
        scene_id = response["success"]["id"]
    else:
         scene_id = '1'
    # Second: Modify Scene --> State of Lights in Group to {"on": true, "hue": 8738, "sat": 158}
    response = requests.get(DECONZ_GROUPS_URL + '/' + rule_group)
    group_lights = response.json()["lights"]
    for element in group_lights:
        data = '{"bri": 254, "on": true, "xy": [0.46, 0.48], "transitiontime": 10}'
        url  = DECONZ_GROUPS_URL + '/' + rule_group + '/scenes/' + scene_id + '/lights/' + element + '/state'
        response = requests.put(url, data = data)
    # Third: create schedule --> call scene
    if repeat_rule == 'false':        
        real_time = datetime.now().strftime('%H:%M')
        rule_date = datetime.today() + timedelta(days=1)
        if real_time < rule_time:  
            rule_date = datetime.today()
        rule_date = rule_date.strftime('%Y-%m-%d')
    elif repeat_rule == 'true':
        rule_days_bit = int(rule_days, 2)
        rule_date = 'W' + str(rule_days_bit) + '/'

    data = '{"name": "' + rule_name + '", "command": {"address": "' + '/api/' + API_KEY + '/groups/' + rule_group + '/scenes/' + scene_id + '/recall", "method": "PUT", "body": {} },"autodelete": false,"localtime": "' + rule_date + 'T' + rule_time + ':00"}'
    url = DECONZ_SCHEDULE_URL
    response = requests.post(url, data = data)
    new_log_entry = LogEntry(message="Regel " + rule_name + " wurde erstellt")
    new_log_entry.save()
    return ("true")

def updateRule(rule_name, rule_group, rule_time, rule_days, repeat_rule, rule_id):
    print("Regel ändern", rule_name, rule_group, rule_time, rule_days, repeat_rule, rule_id)
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
    
    if repeat_rule == 'false':        
        real_time = datetime.now().strftime('%H:%M')
        if real_time > rule_time:
            rule_date = datetime.today() + timedelta(days=1)
        elif real_time < rule_time:  
            rule_date = datetime.today()
        
        rule_date = rule_date.strftime('%Y-%m-%d')
        print(rule_date)
    elif repeat_rule == 'true':
        print("Regel wiederholen", rule_days)
        rule_days_bit = int(rule_days, 2)
        rule_date = 'W' + str(rule_days_bit) + '/'
        print(rule_date)
    
    data = '{"name": "' + rule_name + '", "command": {"address": "' + '/api/' + API_KEY + '/groups/' + rule_group + '/scenes/' + scene_id + '/recall", "method": "PUT", "body": {} },"autodelete": false, "status": "enabled","localtime": "' + rule_date + 'T' + rule_time + ':00"}'
    print(data)
    url = DECONZ_SCHEDULE_URL + '/' + rule_id
    response = requests.put(url, data = data)
    print(response.status_code)
    print(response.content)
    new_log_entry = LogEntry(message="Regel " + rule_name + " wurde geändert")
    new_log_entry.save()
    
    return ("true")

def deleteRule(rule_id, rule_name):
    response = requests.delete(DECONZ_SCHEDULE_URL + '/' + rule_id)
    print(response.status_code)
    print(response.content)
    new_log_entry = LogEntry(message="Regel " + rule_name + " wurde gelöscht")
    new_log_entry.save()
    return response.content
    
