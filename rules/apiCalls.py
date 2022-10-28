import requests

def createSchedule(time, groupID):

    print(time)
    data = '{"command": { "address": "/api/546117A96A/groups/1/action", "method": "PUT", "body": { "on" : true}}, "time" : "' + time + '"}'
    url = 'http://192.168.178.49/api/546117A96A/schedules'
    p = requests.post(url, data=data)
    print(p.status_code)
    print(p.content)


