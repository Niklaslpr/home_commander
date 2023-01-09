import requests
import socket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from devices.apiCalls import putbri
from devices.apiCalls import puthue
from devices.apiCalls import putstate

from devices.apiCalls import startscan

from main.views import get_data_from_input
from main.views import DECONZ_URL, API_KEY, TEST, DECONZ_DEVICE_LIGHTS_URL, DECONZ_DEVICE_SENSORS_URL, DECONZ_GROUPS_URL

@login_required
def devices(request):
    return render(request, "devices.html", {})



@login_required
def turnonoff(request):
    if request.method == 'POST':
        putstate(request.POST['state'], request.POST['lightID'])
    return render(request, "devices.html", {})


@login_required
def setbri(response):
    if response.method == 'POST':
        putbri(response.POST['bri'], response.POST['deviceId'])
    return render(response, "devices.html", {})


@login_required
def sethue(response):
    if response.method == 'POST':
        puthue(response.POST['hue'], response.POST['sat'], response.POST['deviceId'])
    return render(response, "devices.html", {})


@login_required
def startsearch(request):
    if request.method == 'POST':
        newdict = startscan()
        if not newdict:
            return HttpResponse('none')
        else:
            return JsonResponse(newdict)


def kits(request, kit_name):
    data = get_data_from_input(request)

    return render(request, kit_name + ".html",
                  {
                      "id": request.GET["device-id"].__str__(),
                      "name": request.GET["device-name"].__str__(),
                      "has_color": True.__str__()
                  })


def get_all_device_data(request):
    if request.method == "GET":
        data = get_data_from_input(request)

        if not TEST:
            response_tmp = requests.get(url=DECONZ_DEVICE_LIGHTS_URL)
            response_tmp = response_tmp.json()
        else:
            response_tmp = {
                "1": {
                    "etag": "026bcfe544ad76c7534e5ca8ed39047c",
                    "hascolor": True,
                    "manufacturer": "dresden elektronik",
                    "modelid": "FLS-PP3",
                    "name": "Light 1",
                    "pointsymbol": {},
                    "state": {
                        "alert": "none",
                        "bri": 111,
                        "colormode": "ct",
                        "ct": 307,
                        "effect": "none",
                        "hue": 7998,
                        "on": True,
                        "reachable": True,
                        "sat": 172,
                        "xy": [0.421253, 0.39921]
                    },
                    "swversion": "020C.201000A0",
                    "type": "Extended color light",
                    "uniqueid": "00:21:2E:FF:FF:00:73:9F-0A"
                },

                "2": {
                    "etag": "026bcfe544ad76c7534e5ca8ed39047c",
                    "hascolor": False,
                    "manufacturer": "dresden elektronik",
                    "modelid": "FLS-PP3 White",
                    "name": "Light 2",
                    "pointsymbol": {},
                    "state": {
                        "alert": "none",
                        "bri": 1,
                        "effect": "none",
                        "on": False,
                        "reachable": True
                    },
                    "swversion": "020C.201000A0",
                    "type": "Dimmable light",
                    "uniqueid": "00:21:2E:FF:FF:00:73:9F-0B"
                },
                "3": {
                    "config": {
                        "alert": "none",
                        "battery": 0,
                        "delay": 0,
                        "ledindication": False,
                        "on": True,
                        "reachable": True,
                        "sensitivity": 0,
                        "sensitivitymax": 2,
                        "usertest": False
                    },
                    "etag": "18eaf99409636a25c2cdc7197087ba6d",
                    "lastseen": "2022-12-08T11:36Z",
                    "manufacturername": "Philips",
                    "modelid": "SML001",
                    "name": "Presence 11",
                    "state": {
                        "lastupdated": "2022-12-08T11:37:01.292",
                        "presence": True
                    },
                    "swversion": "6.1.1.27575",
                    "type": "ZHAPresence",
                    "uniqueid": "00:17:88:01:08:65:17:d7-02-0406"
                },
                "4": {
                    "config": {
                        "battery": 99,
                        "group": "20000",
                        "on": True,
                        "reachable": True
                    },
                    "etag": "dec924cd3ce57d285b1e46c6b733b1e4",
                    "lastseen": "2022-12-08T11:41Z",
                    "manufacturername": "Signify Netherlands B.V.",
                    "mode": 1,
                    "modelid": "RWL022",
                    "name": "Switch 2",
                    "state": {
                        "buttonevent": 1002,
                        "eventduration": 1,
                        "lastupdated": "2022-12-08T11:42:08.422"
                    },
                    "swversion": "2.44.0_hBB3C188",
                    "type": "ZHASwitch",
                    "uniqueid": "00:17:88:01:0b:72:7b:0b-01-fc00"
                }
            }

        response = []
        for key, value in response_tmp.items():
            response += [{"id": key,
                          "has_color": value["hascolor"] if "hascolor" in value.keys() else False,
                          "name": value["name"] if "name" in value.keys() else "unknown device name",
                          "type": value["type"] if "type" in value.keys() else "unknown device type",
                          "reachable": value["state"]["reachable"] if "state" in value.keys() and "reachable" in value[
                              "state"].keys() else False,
                          "on": value["state"]["on"] if "state" in value.keys() and "on" in value[
                              "state"].keys() else False,
                          "brightness": int(value["state"]["bri"] / 255 * 100) if "state" in value.keys() and "bri" in
                                                                                  value["state"].keys() else 0,
                          "hue": int(value["state"]["hue"] / 65535 * 360) if "state" in value.keys() and "hue" in value[
                              "state"].keys() else 0,
                          "saturation": int(value["state"]["sat"] / 255 * 100) if "state" in value.keys() and "sat" in
                                                                                  value["state"].keys() else 0
                          }]

        response = {"devices": response}

        return JsonResponse(response)


@login_required
@xframe_options_sameorigin
def get_device_data(request, id):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = request.get(url=DECONZ_DEVICE_LIGHTS_URL + "/" + id)
        response = response.json()

        print(data)

        return JsonResponse(response)


def modify_device(request):
    if request.method == "POST":
        data = get_data_from_input(request)

        if data["action"] == "create":
            pass
        elif data["action"] == "update":
            pass
        elif data["action"] == "delete":
            pass
        else:
            return JsonResponse({"error": "unknown action"})

@login_required
def addDeviceToFavorites(request):
    if request.method == 'POST':
        deviceId = request.POST['deviceId']
        x = requests.get(DECONZ_GROUPS_URL)
        grouplist = x.json()
        for key in grouplist:
            tmp = grouplist[key]
            if tmp["name"] == 'favorites_' + request.user.get_username():
                favoritesGroupID = tmp["id"]
        x = requests.get(DECONZ_GROUPS_URL + "/" + favoritesGroupID)
        tmp = x.json()
        lightslist = tmp["lights"]
        lightslist.append(deviceId)
        data = '{ "lights": [ "' + '", "'.join(lightslist) + '" ] }'
        z = requests.put(DECONZ_GROUPS_URL + "/" + favoritesGroupID, data=data)
    return HttpResponse(z.json())

@login_required
def deleteDeviceFromFavorites(request):
    if request.method == 'POST':
        deviceId = request.POST['deviceId']

        x = requests.get(DECONZ_GROUPS_URL)
        grouplist = x.json()
        for key in grouplist:
            tmp = grouplist[key]
            groupname = tmp["name"]
            if groupname == 'favorites_' + request.user.get_username():
                favoritesGroupID = tmp["id"]

        x = requests.get(DECONZ_GROUPS_URL + "/" + favoritesGroupID)
        tmp = x.json()
        lightslist = tmp["lights"]
        lightslist.remove(deviceId)
        if not lightslist:
            z = requests.delete(DECONZ_GROUPS_URL + "/" + favoritesGroupID)
            groupname = "favorites_" + request.user.get_username()
            data = '{"name": "' + groupname + '"}'
            z = requests.post(DECONZ_GROUPS_URL, data=data)
        else:
            data = '{ "lights": [ "' + '", "'.join(lightslist) + '" ] }'
            z = requests.put(DECONZ_GROUPS_URL + "/" + favoritesGroupID, data=data)
        print(z.json())
    return HttpResponse(z.json())

@login_required
def isDeviceinFavorites(request):
    if request.method == 'POST':
        deviceId = request.POST['deviceId']

        x = requests.get(DECONZ_GROUPS_URL)
        grouplist = x.json()
        for key in grouplist:
            tmp = grouplist[key]
            groupname = tmp["name"]
            if groupname == 'favorites_' + request.user.get_username():
                favoritesGroupID = tmp["id"]

        x = requests.get(DECONZ_GROUPS_URL + "/" + favoritesGroupID)
        tmp = x.json()
        lightslist = tmp["lights"]
        if deviceId in lightslist:
            tmp = True
        else:
            tmp = False
    return HttpResponse(tmp)

@login_required
def deleteDevice(request):
    if request.method == 'POST':
        x = requests.delete(DECONZ_DEVICE_LIGHTS_URL + "/" + request.POST['deviceId'], data='{"reset": true}')
        print(x.json())
    return HttpResponse('True')