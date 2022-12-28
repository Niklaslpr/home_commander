import requests
import time
import socket

onRasp = False # True, if Code is running on Raspberry Pi

RASPI_IP = socket.gethostbyname(socket.gethostname())

if not onRasp:
    DECONZ_URL = "http://" + '192.168.178.49' + ':8080'
else:
    DECONZ_URL = "http://" + RASPI_IP + ':8080'

# DECONZ_URL = "http://172.20.10.4:8080"
API_KEY = "973FC5C763"
DECONZ_DEVICE_LIGHTS_URL = DECONZ_URL + "/api/" + API_KEY + "/lights"  # TODO: settings file
DECONZ_DEVICE_SENSORS_URL = DECONZ_URL + "/api/" + API_KEY + "/sensors"


def putstate1(state):
    data = '{"on":' + state + '}'
    url = DECONZ_DEVICE_LIGHTS_URL + '/4/state'
    p = requests.put(url, data = data)
    print(p.status_code)
    print(p.content)


def putstate(state, lightID):
    data = '{"on":' + state + '}'
    url = DECONZ_DEVICE_LIGHTS_URL + '/' + lightID + '/state'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def putbri(bri, id):
    print(bri)
    data = '{"bri":' + bri + '}'
    url = DECONZ_DEVICE_LIGHTS_URL + '/' + id + '/state'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def puthue(hue, sat, id):
    print(hue)
    print(sat)
    print(id)
    data = '{"hue":' + hue + ', "sat":' + sat + '}'
    url = DECONZ_DEVICE_LIGHTS_URL + '/' + id + '/state'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)

def startscan():
    # Aktuelle Liste der Geräte ausgeben
    url = DECONZ_DEVICE_LIGHTS_URL
    p = requests.get(url)
    dict = p.json()
    for key in dict:
        if not key == '1':
            value = dict[key]
            print('ID: ' + key + ', Value: ' + value['manufacturername'] + ', ' + value['name'])
    # Suche starten
    url = DECONZ_DEVICE_SENSORS_URL        #findet Neue Lampe
    p = requests.post(url)
    # Nach 300 Sekunden neue Liste mit der alten vergleiche und neue Geräte ausgeben
    time.sleep(180)
    url = DECONZ_DEVICE_LIGHTS_URL
    p = requests.get(url)
    dict2 = p.json()
    newdevicedict = {}
    for key in dict2:
        if not key in dict:         #print only new Lights
            value = dict2[key]
            newdevicedict[key] = {'manufacturername': value['manufacturername'], 'name': value['name']}

    return newdevicedict


def createSchedule(time, groupID):

    print(time)
    data = '{"command": { "address": "/api/546117A96A/groups/1/action", "method": "PUT", "body": { "on" : true}}, "time" : "' + time + '"}'
    url = 'http://192.168.178.49/api/546117A96A/schedules'
    p = requests.post(url, data=data)
    print(p.status_code)
    print(p.content)


def putgroupstate(state, groupID):
    data = '{"on":' + state + '}'
    url = 'http://192.168.178.49/api/546117A96A/groups/' + groupID + '/action'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def createGroup(groupName):
    data = '{"name": "' + groupName + '" }'
    url = 'http://192.168.178.49:8080/api/973FC5C763/groups'
    p = requests.post(url, data=data)
    print(p.status_code)
    print(p.content)
    return p.status_code