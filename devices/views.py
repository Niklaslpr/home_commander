import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from devices.api_calls_deconz import putbri
from devices.api_calls_deconz import puthue
from devices.api_calls_deconz import putstate
from devices.api_calls_deconz import putstate1
from devices.api_calls_deconz import startscan

from main.views import get_data_from_input
from main.views import DECONZ_URL, API_KEY, TEST

import devices.helper as helper


DECONZ_DEVICE_LIGHTS_URL = DECONZ_URL + "/api/" + API_KEY + "/lights"  # TODO: settings file
DECONZ_DEVICE_SENSORS_URL = DECONZ_URL + "/api/" + API_KEY + "/sensors"


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
def setbri(request):
    if request.method == 'POST':
        putbri(request.POST['bri'])
    return render(request, "devices/devices.html", {})


@login_required
def sethue(request):
    if request.method == 'POST':
        puthue(request.POST['hue'], request.POST['sat'])
    return render(request, "devices/devices.html", {})


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
