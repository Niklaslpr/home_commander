import requests
import time
import socket
from main.views import get_data_from_input
from main.views import DECONZ_URL, API_KEY, TEST, DECONZ_DEVICE_LIGHTS_URL, DECONZ_DEVICE_SENSORS_URL, DECONZ_GROUPS_URL


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
    # Nach 180 Sekunden neue Liste mit der alten vergleiche und neue Geräte ausgeben
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

