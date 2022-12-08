from django.shortcuts import render
import requests
import socket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from main.apiCalls import putbri
from main.apiCalls import puthue
from main.apiCalls import putstate
from main.apiCalls import putstate1
from main.apiCalls import startscan
from main.apiCalls import createSchedule
from main.apiCalls import putgroupstate
from main.apiCalls import createGroup
from django.views.decorators.clickjacking import xframe_options_sameorigin


TEST = True # @Niklas set it to False

def home(response):
    return render(response, "main/home.html", {})

def weather(request):
    if request.method == "GET":

        if not TEST:
            response_tmp = requests.get(url="https://api.openweathermap.org/data/2.5/weather?lat=51.244327040560144&lon=6.794709913902105&appid=0f40bf985000b41f806f413e6adcb377")
            response_tmp = response_tmp.json()
            main_tmp = response_tmp["main"]
            temp_tmp = round(main_tmp["temp"] - 273.15)
            weather_tmp = response_tmp["weather"]
            code_tmp = weather_tmp[0]
            code_tmp = code_tmp["id"]

            dict_tmp = {"temp" : temp_tmp, "code": code_tmp}
        else:
            dict_tmp = {"temp": 9, "code": 511}
        return JsonResponse(dict_tmp)


RASPI_IP = socket.gethostbyname(socket.gethostname())
DECONZ_URL = "http://" + RASPI_IP + ':8080'

# DECONZ_URL = "http://172.20.10.4:8080"
API_KEY = "973FC5C763"
DECONZ_DEVICE_LIGHTS_URL = DECONZ_URL + "/api/" + API_KEY + "/lights"  # TODO: settings file
DECONZ_DEVICE_SENSORS_URL = DECONZ_URL + "/api/" + API_KEY + "/sensors"



def get_data_from_input(data_input):
    return {entry.split("=")[0]: entry.split("=")[1] for entry in
            data_input.read().decode("utf-8").split("&")} if data_input.read().decode("utf-8") != "" else {}


@login_required
def devices(request):
    if request.method == 'POST':
        putstate1(request.POST['state'])
    return render(request, "devices/devices.html", {})


@login_required
def turnonoff(request):
    if request.method == 'POST':
        putstate(request.POST['state'], request.POST['lightID'])
    return render(request, "devices/devices.html", {})


@login_required
def startsearch(request):
    if request.method == 'POST':
        newdict = startscan()
        if not newdict:
            return HttpResponse('none')
        else:
            return JsonResponse(newdict)


def setbri(response):
    if response.method == 'POST':
        putbri(response.POST['bri'], response.POST['deviceId'])
    return render(response, "devices/devices.html", {})


def sethue(response):
    if response.method == 'POST':
        puthue(response.POST['hue'], response.POST['sat'], response.POST['deviceId'])
    return render(response, "devices/devices.html", {})


def kits(request, kit_name):
    data = get_data_from_input(request)

    return render(request, 'devices/' + kit_name + ".html",
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
def activities(response):
    return render(response, "activities/activities.html", {})


@login_required
def rooms(response):
    return render(response, "rooms/rooms.html", {})


@login_required
def scenes(response):
    return render(response, "scenes/scenes.html", {})


@login_required
def options(response):
    return render(response, "options/options.html", {})


@login_required
def rules(response):
    return render(response, "rules/rules.html", {})

@login_required
def createschedule(response):
    if response.method == 'POST':
        createSchedule(response.POST['time'], response.POST['groupID'])
    return render(response, "rules/rules.html", {})


@login_required
def groups(response):
    return render(response, "groups/groups.html", {})


@login_required
def grouponoff(response):
    if response.method == 'POST':
        putgroupstate(response.POST['state'], response.POST['groupID'])
    return render(response, "groups/groups.html", {})


@login_required
def creategroup(response):
    if response.method == 'POST':
        newgroup = createGroup(response.POST['groupName'])
    return HttpResponse(newgroup)