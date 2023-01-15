import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from groups.api_calls_deconz import DECONZ_GROUPS_URL
from main.views import TEST
from main.views import get_data_from_input
import scenes.helper as helper
from devices.helper import get_device_data_from_deconz

DECONZ_SCENES_URL = DECONZ_GROUPS_URL + "<ID>" + "/scenes"


@login_required
def scenes(response):
    return render(response, "scenes/scenes.html", {})


def kits(request, kit_name):
    data = get_data_from_input(request)

    request_get_data = {}
    for entry in request.GET:
        request_get_data[entry.replace("-", "_")] = request.GET[entry]

    return render(request, "scenes/" + kit_name + ".html", request_get_data)


def get_all_scene_data(request):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = helper.get_all_scene_data_from_deconz(request.user.get_username())
        response = {"scenes": response, "devices": get_device_data_from_deconz(-1, request.user.get_username())}

        return JsonResponse(response)


@login_required
@xframe_options_sameorigin
def get_scene_data(request, id):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = request.get(url="DECONZ_DEVICE_LIGHTS_URL" + "/" + id)  # TODO
        response = response.json()

        print(data)

        return JsonResponse(response)


def modify_scene(request):
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
