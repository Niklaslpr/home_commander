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


def get_all_groups():
    response = requests.get(url=DECONZ_GROUPS_URL)
    response = response.json()

    return response


def get_group_attributes(id):
    response = requests.get(url=DECONZ_GROUPS_URL + "/" + id)
    response = response.json()

    return response
