import requests
import time


def putstate1(state):
    data = '{"on":' + state + '}'
    p = requests.put('http://172.20.10.4:8080/api/973FC5C763/lights/4/state', data = data)
    print(p.status_code)
    print(p.content)


def putstate(state, lightID):
    data = '{"on":' + state + '}'
    url = 'http://172.20.10.4:8080/api/973FC5C763/lights/' + lightID + '/state'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def putbri(bri, id):
    print(bri)
    data = '{"bri":' + bri + '}'
    url = 'http://172.20.10.4:8080/api/973FC5C763/lights/' + id + '/state'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def puthue(hue, sat, id):
    print(hue)
    print(sat)
    print(id)
    data = '{"hue":' + hue + ', "sat":' + sat + '}'
    url = 'http://172.20.10.4:8080/api/973FC5C763/lights/' + id + '/state'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)

def startscan():

    # Aktuelle Liste der Geräte ausgeben
    url = 'http://172.20.10.4:8080/api/973FC5C763/lights'
    p = requests.get(url)
    print(p.status_code)
    dict = p.json()
    print(dict)

    for key in dict:
        if not key == '1':
            value = dict[key]
            print('ID: ' + key + ', Value: ' + value['manufacturername'] + ', ' + value['name'])

    # Suche starten
    url = 'http://172.20.10.4:8080/api/973FC5C763/sensors'        #findet Neue Lampe
    p = requests.post(url)
    print(p.status_code)
    print(p.content)

    # Nach 300 Sekunden neue Liste mit der alten vergleiche und neue Geräte ausgeben
    time.sleep(180)
    url = 'http://172.20.10.4:8080/api/973FC5C763/lights'
    p = requests.get(url)
    print(p.status_code)
    dict2 = p.json()
    print(dict)
    print('Gefundene Geräte:')
    newdevicedict = {}

    for key in dict2:
        if not key in dict:         #print only new Lights
            value = dict2[key]
            print('ID: ' + key + ', Value: ' + value['manufacturername']  + ', ' + value['name'])
            newdevicedict[key] = {'manufacturername': value['manufacturername'], 'name': value['name']}

    return newdevicedict

