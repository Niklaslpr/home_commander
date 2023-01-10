from django.shortcuts import render
import requests
import socket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin

TEST = True # @Niklas set it to False
onRasp = False # True, if Code is running on Raspberry Pi

RASPI_IP = socket.gethostbyname(socket.gethostname())

if not onRasp:
    DECONZ_URL = "http://" + '192.168.178.49' + ':8080'
else:
    DECONZ_URL = "http://" + RASPI_IP + ':8080'

API_KEY = "973FC5C763"
DECONZ_DEVICE_LIGHTS_URL = DECONZ_URL + "/api/" + API_KEY + "/lights"  # TODO: settings file
DECONZ_DEVICE_SENSORS_URL = DECONZ_URL + "/api/" + API_KEY + "/sensors"
DECONZ_GROUPS_URL = DECONZ_URL + "/api/" + API_KEY + "/groups"


def get_data_from_input(data_input):
    return {entry.split("=")[0]: entry.split("=")[1] for entry in
            data_input.read().decode("utf-8").split("&")} if data_input.read().decode("utf-8") != "" else {}


@login_required
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

@login_required
def createFavoriteGroup(request):
    if request.method == 'POST':
        z = 0
        x = requests.get(DECONZ_GROUPS_URL)
        grouplist = x.json()
        for key in grouplist:
            tmp = grouplist[key]
            groupname = tmp["name"]
            if groupname == 'favorites_' + request.user.get_username():
                favoritesGroupID = tmp["id"]
                z += 1

        if z == 0:
            groupname = "favorites_" + request.user.get_username()
            data = '{"name": "' + groupname + '"}'
            x = requests.post(DECONZ_GROUPS_URL, data=data)
            tmp = x.json()
            tmp = tmp[0]
            tmp = tmp["success"]
            favoritesGroupID = tmp["id"]

        print("Favorite Group-ID = " + favoritesGroupID)
        x = requests.get(DECONZ_GROUPS_URL + "/" + favoritesGroupID)
        tmp = x.json()
        lightslist = tmp["lights"]
        print(lightslist)
    return HttpResponse(", ".join(lightslist))


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
