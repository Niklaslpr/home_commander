import requests


def putstate1(state):
    data = '{"on":' + state + '}'
    p = requests.put('http://192.168.178.49/api/546117A96A/lights/4/state', data = data)
    print(p.status_code)
    print(p.content)


def putstate(state, lightID):
    data = '{"on":' + state + '}'
    url = 'http://192.168.178.49/api/546117A96A/lights/' + lightID + '/state'
    p = requests.put(url, data=data)
    print(p.status_code)
    print(p.content)


def putbri(bri):
    print(bri)
    data = '{"bri":' + bri + '}'
    p = requests.put('http://192.168.178.49/api/546117A96A/lights/2/state', data=data)
    print(p.status_code)
    print(p.content)


def puthue(hue, sat):
    print(hue)
    print(sat)
    data = '{"hue":' + hue + ', "sat":' + sat + '}'
    p = requests.put('http://192.168.178.49/api/546117A96A/lights/2/state', data=data)
    print(p.status_code)
    print(p.content)

