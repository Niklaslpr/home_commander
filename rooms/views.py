import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from rooms.api_calls_deconz import createGroup, updateGroup
from rooms.api_calls_deconz import putState
from rooms.api_calls_deconz import putHue, putBri
from rooms.api_calls_deconz import deleteGroup
from main.views import get_data_from_input, DECONZ_URL, API_KEY, TEST
import rooms.helper as helper
from groups.models import Group
from main.views import ICON_PATH

@login_required
def rooms(response):
    return render(response, "rooms.html", {})


@login_required
def grouponoff(response):
    if response.method == 'POST':
        putState(response.POST['state'], response.POST['groupID'])
    return render(response, "groups.html", {})

@login_required
def groupsethue(response):
    if response.method == 'POST':
        putHue(response.POST["hue"], response.POST["sat"], response.POST["groupId"])
    return HttpResponse("true")


@login_required
def groupsetbri(response):
    if response.method == 'POST':
        putBri(response.POST["bri"], response.POST["groupId"])
    return HttpResponse("true")

@login_required
def creategroup(response):
    if response.method == 'POST':
        newgroup = createGroup(response.POST['groupName'], response.POST['selectedDevices'])
        print("HIER", newgroup)
        new_group = Group(group_id=newgroup[0]["success"]["id"].__str__(),
                                    name=response.POST["groupName"],
                                    is_room=False)
        new_group.icon = response.POST["selectedIcon"]
        new_group.save()
    return HttpResponse(newgroup)

@login_required
def updategroup(response):
    if response.method == 'POST':
        
        group_id = response.POST['groupId']
        group_name = response.POST['groupName']
        group_devices = response.POST['selectedDevices']
        group_icon = response.POST['selectedIcon']
        updategroup = updateGroup(response.POST['groupName'], response.POST['selectedDevices'], response.POST['groupId'])
        
        group = Group.objects.get(group_id__exact=group_id.__str__())
        group.icon = group_icon
        group.save()
        
    return HttpResponse(updategroup)

@login_required
def deletegroup(response):
    if response.method == 'POST':
        deleteGroup(response.POST['groupId'], response.POST['groupName'])
    return HttpResponse("True")

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
        for entry in response:
            group = Group.objects.get(group_id__exact=entry['id'].__str__())
            entry["icon"] = ICON_PATH + group.icon
        response = {"groupsCollection": response}
        print("HIIIIIIER", response)
        return JsonResponse(response)


@login_required
@xframe_options_sameorigin
def get_group_data(request, id):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = helper.get_group_data_from_deconz(id, request.user.username)

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
