from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

import groups.helper as helper
from groups.api_calls_deconz import createGroup
from groups.api_calls_deconz import putState
from main.views import get_data_from_input
from .models import Group


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

        response = helper.get_group_data_from_deconz(id, request.user.get_username())

        print(data)

        return JsonResponse(response)


def modify_group(request):
    if request.method == "POST":
        data = get_data_from_input(request)

        if data["action"] == "create":
            if "attributes" in data.keys():
                if "name" in data["attributes"]:
                    response = helper.create_group_in_deconz(data["attributes"]["name"])
                    if response is not None and isinstance(response, dict) and "status_code" in response.keys() and \
                            response["status_code"].__str__() == "200":
                        new_group = Group(name="")  # TODO: how to get ID?
                        new_group.save()

                        return JsonResponse(response)
                    else:
                        return JsonResponse({"error": "could not create device"})  # TODO
                else:
                    return JsonResponse({"error": "no name specified"})
            else:
                return JsonResponse({"error": "no attributes specified"})
        elif data["action"] == "update":
            if "attributes" in data.keys():
                request_data = {
                    "name": data["attributes"]["name"] if "name" in data["attributes"].keys() else None,
                    "lights": data["attributes"]["lights"] if "lights" in data["attributes"].keys() and isinstance(
                        data["attributes"]["lights"], list) else None,
                    "hidden": data["attributes"]["hidden"] if "hidden" in data["attributes"].keys() else None,
                    "light_sequence": data["attributes"]["light_sequence"] if "light_sequence" in data[
                        "attributes"].keys() and isinstance(data["attributes"]["light_sequence"], list) else None,
                    "multi_device_ids": data["attributes"]["multi_device_ids"] if "multi_device_ids" in data[
                        "attributes"].keys() and isinstance(data["attributes"]["multi_device_ids"], list) else None,
                }

                if "group_id" in data.keys() and (
                        isinstance(data["group_id"], int) or isinstance(data["group_id"], str) and data[
                    "group_id"].isnumeric()):
                    response = helper.update_group_deconz(int(data["device_id"]), **request_data)
                    return JsonResponse(response)
                else:
                    return JsonResponse({"error": "no device id specified or wrong data type"})
            else:
                return JsonResponse({"error": "no attributes specified"})
        elif data["action"] == "delete":
            pass
        else:
            return JsonResponse({"error": "unknown action"})
