import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from devices.apiCalls import putbri
from devices.apiCalls import puthue
from devices.apiCalls import putstate
from devices.apiCalls import putstate1
from devices.apiCalls import startscan

DECONZ_URL = "http://192.168.178.49"
API_KEY = "546117A96A"
DECONZ_DEVICE_LIGHTS_URL = DECONZ_URL + "/api/" + API_KEY + "/lights"  # TODO: settings file
DECONZ_DEVICE_SENSORS_URL = DECONZ_URL + "/api/" + API_KEY + "/sensors"
TEST = True  # @Niklas set it to False


def get_data_from_input(data_input):
    return {entry.split("=")[0]: entry.split("=")[1] for entry in
            data_input.read().decode("utf-8").split("&")} if data_input.read().decode("utf-8") != "" else {}


@login_required
def devices(request):
    if request.method == 'POST':
        putstate1(request.POST['state'])
    return render(request, "devices.html", {})


@login_required
def turnonoff(request):
    if request.method == 'POST':
        putstate(request.POST['state'], request.POST['lightID'])
    return render(request, "devices.html", {})


@login_required
def setbri(request):
    if request.method == 'POST':
        putbri(request.POST['bri'])
    return render(request, "devices.html", {})


@login_required
def sethue(request):
    if request.method == 'POST':
        puthue(request.POST['hue'], request.POST['sat'])
    return render(request, "devices.html", {})


@login_required
def startsearch(request):
    if request.method == 'POST':
        newdict = startscan()
        if not newdict:
            return HttpResponse('none')
        else:
            return JsonResponse(newdict)
    # data = {'1':{'manufacturername': 'Philips', 'name': 'Light'}, '2':{'manufacturername': 'Philips2', 'name': 'Light2'}}

    # return render(request, "devices.html", {'test': 'test'}) #nur Änderung zurückgeben


def setbri(response):
    if response.method == 'POST':
        putbri(response.POST['bri'])
    return render(response, "devices.html", {})


def sethue(response):
    if response.method == 'POST':
        puthue(response.POST['hue'], response.POST['sat'])
    return render(response, "devices.html", {})


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
