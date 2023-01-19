import re
from datetime import datetime
from django.shortcuts import render
import urllib.parse
import requests
import socket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from activities.models import LogEntry

TEST = False  # @Niklas set it to False
onRasp = True  # True, if Code is running on Raspberry Pi

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
    # print("data_input", urllib.parse.unquote(data_input.read().decode("utf-8")))
    # print("is that magic", chr(int("0x5B", 16)))

    # test_string = data_input.read().decode("utf-8")
    # print("testString", test_string)
    # for x in data_input.read().decode("utf-8").split("&"):
    #     print("x", x)
    raw_data = urllib.parse.unquote(data_input.body.decode("utf-8"))

    print("raw data", raw_data)

    data = {}

    if raw_data != "":
        for entry in raw_data.split("&"):
            if re.search(r"^\w+\[\w+]=\w+$", entry):
                print("it goes here", entry)
                parent = entry.split("[")[0]
                child = entry.split("[")[1].split("]")[0]
                value = entry.split("[")[1].split("]")[1][1:]

                print("parent", parent)
                print("child", child)
                print("value", value)

                if parent not in data.keys():
                    data[parent] = {}
                data[parent][child] = value
            else:
                print("nope here", entry)
                data[entry.split("=")[0]] = entry.split("=")[1]

    return data


@login_required
def home(response):
    print("Hallo Logs")
    last_entries = LogEntry.objects.order_by('-timestamp')[:3]
    
    
    logs = {}
    x = 0
    while x < 3:
        logs['timestamp'+str(x)] = str(last_entries[x].timestamp.strftime("%d.%m.%Y, %H:%M"))
        logs['message'+str(x)] = last_entries[x].message
        
        
        x = x+1    
    print(logs) 
   
    return render(response, "main/home.html", logs)


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

            dict_tmp = {"temp": temp_tmp, "code": code_tmp}
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
