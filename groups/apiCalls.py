import requests

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