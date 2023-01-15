import time
import json
import requests

from main.views import DECONZ_URL, API_KEY

# TODO: URL
DECONZ_DEVICE_LIGHTS_URL = DECONZ_URL + "/api/" + API_KEY + "/lights"  # TODO: settings file
DECONZ_DEVICE_SENSORS_URL = DECONZ_URL + "/api/" + API_KEY + "/sensors"
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
        if not key in dict:  # print only new Lights
            value = dict2[key]
            print('ID: ' + key + ', Value: ' + value['manufacturername'] + ', ' + value['name'])
            newdevicedict[key] = {'manufacturername': value['manufacturername'], 'name': value['name']}

    return newdevicedict


def get_all_lights():
    response = requests.get(url=DECONZ_DEVICE_LIGHTS_URL)
    response = response.json()

    return response


def get_light_state(light_id):
    response = requests.get(url=DECONZ_DEVICE_LIGHTS_URL + "/" + light_id)
    response = response.json()

    return response


def update_light_state(light_id, request_data):
    if isinstance(request_data, dict) and request_data != {}:
        print('HAllo Hier ich binasdasjdajsd')
        print(type(request_data))
        print(request_data)
        response = requests.put(DECONZ_DEVICE_LIGHTS_URL + "/" + light_id + "/state", data=json.dumps(request_data))
        response = response.json() # TODO

        print("Update Light Status", response.status_code)
        print("Update Light Content", response.content)
        response = response.json()
    else:
        response = None

    return response
