import json

import requests

from main.views import DECONZ_URL, API_KEY
from activities.models import LogEntry

DECONZ_GROUPS_URL = DECONZ_URL + "/api/" + API_KEY + "/groups"


def putState(state, groupID):
    data = '{"on":' + state + '}'
    url = DECONZ_GROUPS_URL + '/' + groupID + '/action'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)

def putHue(hue, sat, groupId):
    data = '{"hue":' + hue + ', "sat":' + sat + '}'
    url = DECONZ_GROUPS_URL + '/' + groupId + '/action'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)

def putBri(bri, groupId):
    data = '{"bri":' + bri + '}'
    url = DECONZ_GROUPS_URL + '/' + groupId + '/action'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def createGroup(groupName, selectedDevices):
    data = '{"name": "' + groupName + '" }'
    p = requests.post(DECONZ_GROUPS_URL, data=data)
    print(p.status_code)
    response = p.json()
    groupId = response[0]["success"]["id"]
    selectedDevices = selectedDevices.split(",")
    tmp = '['
    for x in selectedDevices:
        tmp = tmp + '"' + x + '", '
    tmp = tmp + ']'
    data = '{"lights": ' + tmp + '}"'
    url = DECONZ_GROUPS_URL + '/' + groupId
    r = requests.put(url, data=data)
    print(r.status_code)
    print(r.content)
    
    new_log_entry = LogEntry(message="Gruppe " + groupName + " wurde erstellt")
    new_log_entry.save()
    
    return p.status_code
    
def updateGroup(groupName, selectedDevices, groupId):
    selectedDevices = selectedDevices.split(",")
    
    if selectedDevices == ['']:
        tmp = '[]'
    else:    
        tmp = '['
        for x in selectedDevices:
            tmp = tmp + '"' + x + '", '
        tmp = tmp + ']'    
    data = '{"name": "' + groupName + '","lights": ' + tmp + '}"'
    print(data)
    url = DECONZ_GROUPS_URL + '/' + groupId
    r = requests.put(url, data=data)
    print("Ach du scheiße")
    print(r.status_code)
    print(r.content)
    new_log_entry = LogEntry(message="Gruppe " + groupName + " wurde geändert")
    new_log_entry.save()
    return r.status_code

def create_group(request_data):
    if isinstance(request_data, dict) and request_data != {}:
        response = requests.post(url=DECONZ_GROUPS_URL, data=request_data)
        response = response.json()
    else:
        response = None

    return response


def get_all_groups():
    response = requests.get(url=DECONZ_GROUPS_URL)
    response = response.json()

    return response


def get_group_attributes(group_id):
    response = requests.get(url=DECONZ_GROUPS_URL + "/" + group_id)
    response = response.json()

    return response

def deleteGroup(groupId, groupName):
    data = '{"on": true}'
    url = DECONZ_GROUPS_URL + '/' + groupId + '/action'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)
    url = DECONZ_GROUPS_URL + '/' + groupId
    p = requests.delete(url)
    print('Löschen:')
    print(p.status_code)
    print(p.content)
    new_log_entry = LogEntry(message="Gruppe " + groupName + " wurde gelöscht")
    new_log_entry.save()


def update_group_attributes(group_id, request_data):
    if isinstance(request_data, dict) and request_data != {}:
        response = requests.put(url=DECONZ_GROUPS_URL + group_id.__str__(), data=json.dumps(request_data))
    else:
        response = None

    return response
