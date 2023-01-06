import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from groups.api_calls_deconz import createGroup
from groups.api_calls_deconz import putState
from main.views import get_data_from_input, DECONZ_URL, API_KEY, TEST
from devices.views import DECONZ_DEVICE_LIGHTS_URL, DECONZ_DEVICE_SENSORS_URL

import groups.helper as helper


@login_required
def groups(response):
    return render(response, "groups.html", {})


@login_required
def grouponoff(response):
    if response.method == 'POST':
        putState(response.POST['state'], response.POST['groupID'])
    return render(response, "groups.html", {})


@login_required
def creategroup(response):
    if response.method == 'POST':
        newgroup = createGroup(response.POST['groupName'])
    return HttpResponse(newgroup)


def kits(request, kit_name):
    data = get_data_from_input(request)

    print("thats my data:", data)
    print("and thats my get", request.GET)

    request_get_data = {}
    for entry in request.GET:
        print("ah thats bullshit", entry)
        request_get_data[entry.replace("-", "_")] = request.GET[entry]

    print("krraaaakkeke", request_get_data)

    return render(request, kit_name + ".html", request_get_data)


def get_all_group_data(request):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = helper.get_group_data_from_deconz(-1, request.user.get_username())
        response = {"groupsCollection": response}

        return JsonResponse(response)


@login_required
@xframe_options_sameorigin
def get_group_data(request, id):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = request.get(url=DECONZ_GROUPS_URL + "/" + id)
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
