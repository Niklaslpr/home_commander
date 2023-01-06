import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from groups.api_calls_deconz import DECONZ_GROUPS_URL
from main.views import TEST
from main.views import get_data_from_input

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

        if not TEST:
            response_groups = request.get(url=DECONZ_GROUPS_URL)

            response_tmp = {}
            for key, group in response_groups.items():
                response_scenes_tmp = requests.get(url=DECONZ_SCENES_URL.replace("<ID>", key))  # TODO
                response_scenes_tmp = response_scenes_tmp.json()
        else:
            response_groups = {
                "1": {
                    "devicemembership": [],
                    "etag": "ab5272cfe11339202929259af22252ae",
                    "hidden": False,
                    "name": "Living Room"
                },
                "2": {
                    "devicemembership": ["3"],
                    "etag": "030cf8c1c0025420f3a0659afab251f5",
                    "hidden": False,
                    "name": "Kitchen"
                }
            }

            response_tmp = {}
            for key, group in response_groups.items():
                if key == "1":
                    response_scenes_tmp = {
                        "1": {
                            "lights": ["1", "2"],
                            "name": "working"
                        },
                        "2": {
                            "lights": ["4", "6", "7", "5"],
                            "name": "reading"
                        }
                    }
                elif key == "2":
                    response_scenes_tmp = {
                        "3": {
                            "lights": ["2", "4", "7"],
                            "name": "holiday"
                        },
                        "4": {
                            "lights": ["3"],
                            "name": "BIERPAUSE"
                        },
                        "8": {
                            "lights": ["3", "2"],
                            "name": "sleeping"
                        }
                    }
                else:
                    response_scenes_tmp = {
                        "5": {
                            "lights": ["4", "6", "7", "5"],
                            "name": "work out"
                        },
                        "6": {
                            "lights": ["3"],
                            "name": "Party"
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

        response = {"scenes": response, "devices": ""}

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
