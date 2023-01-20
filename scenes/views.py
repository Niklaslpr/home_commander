from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

import scenes.helper as helper
from devices.helper import get_device_data_from_deconz
from groups.api_calls_deconz import DECONZ_GROUPS_URL
from main.views import get_data_from_input
from scenes.models import Scene
from scenes.api_calls_deconz import create_scene

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
        print('JabadabaDU', data)
        test = create_scene("140", {"name": "keinBockMehr"})

        if data["action"] == "create":
            if "attributes" in data.keys():
                if "name" in data["attributes"]:
                    response = helper.create_scene_in_deconz(data["attributes"]["name"])
                    if response is not None and isinstance(response, dict):
                        print(response)
                        new_scene = Scene(scene_id=response["response"][0]["success"]["id"].__str__(),
                                          name=data["attributes"]["name"])
                        new_scene.save()
                        print("HIER KOMMT DATA", data)
                        if "icon" in data["features"].keys():
                            new_scene.icon = data["features"]["icon"]
                        if "users" in data["features"].keys():
                            for entry in data["features"]["users"]:
                                if isinstance(entry, dict):
                                    if "operation" in entry.keys() and "username" in entry.keys() and entry[
                                        "operation"] == "add":
                                        new_scene.users.add(User.objects.get(username__exact=entry["username"]))
                                    elif "operation" in entry.keys() and "username" in entry.keys() and entry[
                                        "operation"] == "remove":
                                        new_scene.users.remove(User.objects.get(username__exact=entry["username"]))

                        new_scene.save()

                        return JsonResponse(response)
                    else:
                        return JsonResponse({"error": "could not create scene"})  # TODO
                else:
                    return JsonResponse({"error": "no name specified"})
            else:
                return JsonResponse({"error": "no attributes specified"})
        elif data["action"] == "update":
            if "attributes" in data.keys():
                request_data = {
                    "name": data["attributes"]["name"] if "name" in data["attributes"].keys() else None
                }

                if "lights" in data["attributes"].keys() and isinstance(data["attributes"]["lights"], list):
                    request_data["lights"] = data["attributes"]["lights"]

                if "scene_id" in data.keys() and (
                        isinstance(data["scene_id"], int) or isinstance(data["scene_id"], str) and data[
                    "scene_id"].isnumeric()):
                    response = helper.update_scene_deconz(int(data["scene_id"]), **request_data)
                    
                    return JsonResponse(response)
                else:
                    return JsonResponse({"error": "no scene id specified or wrong data type"})
            elif "features" in data.keys():
                pass
            elif "states" in data.keys():
                if "scene_id" in data.keys() and (
                        isinstance(data["scene_id"], int) or isinstance(data["scene_id"], str) and data[
                    "scene_id"].isnumeric()):
                    if "all" in data["states"].keys() and data["states"]["all"] == "store_current_states":
                        response = helper.update_scene_state_deconz(int(data["scene_id"]))
                        return JsonResponse(response)
                    elif "on" in data["states"].keys() and data["states"]["on"].__str__() == "y":
                        response = helper.activate_scene(data["scene_id"])
                        return JsonResponse(response)
                    else:
                        return JsonResponse({"error": "unknown scene states key"})
                else:
                    return JsonResponse({"error": "no scene id specified or wrong data type"})
            else:
                return JsonResponse({"error": "no attributes or features specified"})
        elif data["action"] == "delete":
            if "scene_id" in data.keys() and (
                    isinstance(data["scene_id"], int) or isinstance(data["scene_id"], str) and data[
                "scene_id"].isnumeric()):
                response = helper.delete_scene_deconz(int(data["scene_id"]), request.user.get_username())
                return JsonResponse(response)
            else:
                return JsonResponse({"error": "no scene id specified or wrong data type"})
        else:
            return JsonResponse({"error": "unknown action"})
