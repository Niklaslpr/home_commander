import requests
from main.views import DECONZ_URL, API_KEY

DECONZ_GROUPS_URL = DECONZ_URL + "/api/" + API_KEY + "/groups"


def putState(state, groupID):
    data = '{"on":' + state + '}'
    url = DECONZ_GROUPS_URL + '/' + groupID + '/action'
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
    return p.status_code


def get_all_groups():
    response = requests.get(url=DECONZ_GROUPS_URL)
    response = response.json()

    return response


def get_group_attributes(id):
    response = requests.get(url=DECONZ_GROUPS_URL + "/" + id)
    response = response.json()

    return response

def deleteGroup(groupId):
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
    
