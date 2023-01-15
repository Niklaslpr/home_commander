import json

import requests

from main.views import DECONZ_URL, API_KEY

DECONZ_GROUPS_URL = DECONZ_URL + "/api/" + API_KEY + "/groups"


def putState(state, groupID):
    data = '{"on":' + state + '}'
    url = 'http://192.168.178.49/api/546117A96A/groups/' + groupID + '/action'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def createGroup(groupName):
    data = '{"name": "' + groupName + '" }'
    url = 'http://192.168.178.49/api/546117A96A/groups'
    p = requests.post(url, data=data)
    print(p.status_code)
    print(p.content)
    return p.status_code


def create_group(request_data):
    if isinstance(request_data, dict) and request_data != {}:
        response = requests.post(url=DECONZ_GROUPS_URL, data=request_data)
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


def update_group_attributes(group_id, request_data):
    if isinstance(request_data, dict) and request_data != {}:
        response = requests.put(url=DECONZ_GROUPS_URL + group_id.__str__(), data=json.dumps(request_data))
    else:
        response = None

    return response
