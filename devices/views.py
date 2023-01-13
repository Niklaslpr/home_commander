import requests
import socket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

import devices.helper as helper
from devices.api_calls_deconz import putbri
from devices.api_calls_deconz import puthue
from devices.api_calls_deconz import putstate
from devices.api_calls_deconz import putstate1
from devices.api_calls_deconz import startscan
from main.views import get_data_from_input
from main.views import DECONZ_GROUPS_URL, DECONZ_DEVICE_LIGHTS_URL, DECONZ_DEVICE_SENSORS_URL


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

    return render(request, "devices/" + kit_name + ".html",
                  {
                      "id": request.GET["device-id"].__str__(),
                      "name": request.GET["device-name"].__str__(),
                      "has_color": True.__str__()
                  })


def get_all_device_data(request):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = helper.get_device_data_from_deconz(-1, request.user.get_username())
        response = {"devices": response}

        return JsonResponse(response)


@login_required
@xframe_options_sameorigin
def get_device_data(request, id):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = helper.get_device_data_from_deconz(id, request.user.get_username())

        print(data)

        return JsonResponse(response)


def modify_device(request):
    if request.method == "POST":
        data = get_data_from_input(request)
        # data = {}
        # print("wasn das", request.body.decode("utf-8"))
        print("here it comes", data)
        print("here it goes", request.POST.get("action", ""))

        if data["action"] == "create":
            pass
        elif data["action"] == "update":
            print("is it working?", data)

            if "type" in data.keys() and data["type"] == "light":
                if "state" in data.keys():
                    request_data = {
                        "alert": data["state"]["alert"] if "alert" in data["state"].keys() else None,
                        "brightness": data["state"]["brightness"] if "brightness" in data[
                            "state"].keys() else None,
                        "color_loop_speed": data["state"]["color_loop_speed"] if "color_loop_speed" in data[
                            "state"].keys() else None,
                        "ct": data["state"]["ct"] if "ct" in data["state"].keys() else None,
                        "effect": data["state"]["effect"] if "effect" in data["state"].keys() else None,
                        "hue": data["state"]["hue"] if "hue" in data["state"].keys() else None,
                        "on": data["state"]["on"] if "on" in data["state"].keys() else None,
                        "saturation": data["state"]["saturation"] if "saturation" in data[
                            "state"].keys() else None,
                        "transition_time": data["state"]["transition_time"] if "transition_time" in data[
                            "state"].keys() else None,
                        "x": data["state"]["xy"][0] if "xy" in data["state"].keys() and isinstance(
                            data["state"]["xy"], list) else None,
                        "y": data["state"]["xy"][1] if "xy" in data["state"].keys() and isinstance(
                            data["state"]["xy"], list) else None
                    }

                    if "device_id" in data.keys() and (isinstance(data["device_id"], int) or isinstance(data["device_id"], str) and data["device_id"].isnumeric()):
                        print("Affenarsch", request_data)
                        response = helper.update_light_state_deconz(int(data["device_id"]), **request_data)
                        print('Hier bin ich type:')
                        print(response)
                        return JsonResponse(response)
                    else:
                        return JsonResponse({"error": "no device id specified or wrong data type"})
                else:
                    return JsonResponse({"error": "no state specified"})
            elif "type" in data.keys() and data["type"] == "sensor":
                pass
            else:
                # error
                return JsonResponse({"error": "no type specified or unknown type"})
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
