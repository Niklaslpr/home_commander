from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

import groups.helper as helper
from groups.api_calls_deconz import createGroup
from groups.api_calls_deconz import putState
from main.views import get_data_from_input


@login_required
def rooms(response):
    return render(response, "rooms/rooms.html", {})


@login_required
def grouponoff(response):
    if response.method == 'POST':
        putState(response.POST['state'], response.POST['groupID'])
    return render(response, "rooms.html", {})


@login_required
def creategroup(response):
    if response.method == 'POST':
        newgroup = createGroup(response.POST['groupName'])
    return HttpResponse(newgroup)


def kits(request, kit_name):
    data = get_data_from_input(request)

    request_get_data = {}
    for entry in request.GET:
        request_get_data[entry.replace("-", "_")] = request.GET[entry]

    return render(request, kit_name + ".html", request_get_data)


def get_all_room_data(request):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = helper.get_room_data_from_deconz(-1, request.user.get_username())
        response = {"rooms": response}

        return JsonResponse(response)


@login_required
@xframe_options_sameorigin
def get_room_data(request, id):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = helper.get_room_data_from_deconz(id, request.user.get_username())

        print(data)

        return JsonResponse(response)


def modify_room(request):
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
