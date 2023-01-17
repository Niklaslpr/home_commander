import re

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from main.views import DECONZ_URL, API_KEY, TEST
from main.views import get_data_from_input
from rules.api_calls_deconz import createSchedule

DECONZ_SCHEDULE_URL = DECONZ_URL + "/api/" + API_KEY + "/schedules"

UTC_ISO_DATE = 0
UTC_ISO_TIME = 1
UTC_ISO_WEEKDAYS = 2
UTC_ISO_TIMER = 3
UTC_ISO_RECURRING_TIMER = 4
UTC_ISO_RANDOMIZED_TIME = 5


def convert_weekday_bitmap(weekday_bitmap):
    weekday_bitmap = str(weekday_bitmap)
    possibleWeekdays = {1: 'Mo', 2: 'Di', 3: 'Mi', 4: 'Do', 5: 'Fr', 6: 'Sa',
                        7: 'So'}
    weekday_list = []
    print(weekday_bitmap)
    for i,c in enumerate(weekday_bitmap):
        print(weekday_bitmap[i])
        if weekday_bitmap[i] == '1':
            weekday_list.append(' ' + possibleWeekdays.get(i+1))
    return weekday_list


def get_info_from_utc_iso_8601_2004_string(utc_iso_8601_2004_string, info):
    if info not in [UTC_ISO_DATE, UTC_ISO_TIME, UTC_ISO_WEEKDAYS, UTC_ISO_TIMER, UTC_ISO_RECURRING_TIMER,
                    UTC_ISO_RANDOMIZED_TIME]:
        return None

    if info == UTC_ISO_DATE and re.search(r"^\d{4}-\d{2}-\d{2}T.*$", utc_iso_8601_2004_string) is not None:
        return utc_iso_8601_2004_string.split("T")[0]
    elif info == UTC_ISO_TIME and re.search(r"^.*[^P]T\d{2}:\d{2}:\d{2}(A.*)?$", utc_iso_8601_2004_string) is not None:
        return re.split(r"A\d{2}:\d{2}:\d{2}", utc_iso_8601_2004_string.split("T")[-1])[0]
    elif info == UTC_ISO_WEEKDAYS and re.search(r"^W\d{1,3}/.*$", utc_iso_8601_2004_string) is not None:
        return convert_weekday_bitmap(bin(int(utc_iso_8601_2004_string.split("/")[0][1:]))[2:])
    elif info == UTC_ISO_TIMER and re.search(r"^.*PT\d{2}:\d{2}:\d{2}(A.*)?$", utc_iso_8601_2004_string) is not None:
        return re.split(r"A\d{2}:\d{2}:\d{2}", utc_iso_8601_2004_string.split("T")[-1])[0]
    elif info == UTC_ISO_RECURRING_TIMER and re.search(r"^R(\d{1,2})?/PT.*$", utc_iso_8601_2004_string) is not None:
        return utc_iso_8601_2004_string.split("/")[0].replace("R", "")
    elif info == UTC_ISO_RANDOMIZED_TIME and re.search(r"^.*A\d{2}:\d{2}:\d{2}$", utc_iso_8601_2004_string) is not None:
        return utc_iso_8601_2004_string.split("A")[-1]

    return None


@login_required
def rules(response):
    return render(response, "rules/rules.html", {})


@login_required
def createschedule(response):
    if response.method == 'POST':
        createSchedule(response.POST['time'], response.POST['groupID'])
    return render(response, "rules/rules.html", {})



                  
def kits(request, kit_name):
    data = get_data_from_input(request)

    print("thats my data:", data)
    print("and thats my get", request.GET)
    print("TOLLLLLLLLLLLLLLLLL")
    request_get_data = {}
    for entry in request.GET:
        print("ah thats bullshit", entry)
        request_get_data[entry.replace("-", "_")] = request.GET[entry]

    print("krraaaakkeke", request_get_data)

    return render(request, "rules/" +  kit_name + ".html", request_get_data)


def get_all_rule_data(request):
    if request.method == "GET":
        data = get_data_from_input(request)

        if not TEST:
            response_tmp = requests.get(url=DECONZ_SCHEDULE_URL)
            response_tmp = response_tmp.json()
            print("UFFFFFFFFFFFFFFFFFFFFFFFFFFF")
            print(response_tmp)
        else:
            response_tmp = {
                "1": {
                    "autodelete": False,
                    "command": {
                        "address": "/api/8918fbad2100nag17ca1/groups/2/action",
                        "method": "PUT",
                        "body": {"on": False}
                    },
                    "description": "Turns all lights off",
                    "etag": "4e100d1c4e3497154a77bc0865c89030",
                    "name": "turn all off",
                    "status": "enabled",
                    "time": "2013-07-30T20:10:00"
                },
                "2": {
                    "autodelete": False,
                    "command": {
                        "address": "/api/AD4F14F244/groups/4/scenes/1/recall",
                        "body": {},
                        "method": "PUT"
                    },
                    "description": "",
                    "etag": "4e100d1c4e3497154a77bc0865c89030",
                    "name": "call scene",
                    "status": "enabled",
                    "time": "W120/T10:00:00"
                }
            }

        response = []
        for key, value in response_tmp.items():
            print("oh yes here we go")
            if "localtime" in value.keys():    
                if value["localtime"][0] == "W":
                    i = value["localtime"].index("/")
                    weekdays = value["localtime"][1:i]
                    weekdays_bin = format(int(weekdays), '07b')
                    weekdays = convert_weekday_bitmap(weekdays_bin)
                    if weekdays == [' Mo', ' Di', ' Mi', ' Do', ' Fr', ' Sa', ' So']:
                        weekdays = 'Jeden Tag'
                      
                    
                else:
                    weekdays = value["localtime"][0:10] 
                   
                
            response += [{"id": key,
                          "name": value["name"] if "name" in value.keys() else "unknown rule name",
                          "description": value["description"] if "description" in value.keys() else "",
                          "localtime": value["localtime"][-8:-3] if "localtime" in value.keys() else None,
                          "active": True if "status" in value.keys() and value["status"] == "enabled" else False,
                          "weekdays": weekdays if "localtime" in value.keys() else None,
                    
                          
                          
                          "date": get_info_from_utc_iso_8601_2004_string(value["time"],
                                                                         UTC_ISO_DATE) if "time" in value.keys() else None,
                          "time": get_info_from_utc_iso_8601_2004_string(value["time"],
                                                                         UTC_ISO_TIME) if "time" in value.keys() else None,
                          # "weekdays": get_info_from_utc_iso_8601_2004_string(value["time"],
                                                                             # UTC_ISO_WEEKDAYS) if "time" in value.keys() else None,
                          "timer": get_info_from_utc_iso_8601_2004_string(value["time"],
                                                                          UTC_ISO_TIMER) if "time" in value.keys() else None,
                          "recurrent_timer": get_info_from_utc_iso_8601_2004_string(value["time"],
                                                                                    UTC_ISO_RECURRING_TIMER) if "time" in value.keys() else None,
                          "randomized_time": get_info_from_utc_iso_8601_2004_string(value["time"],
                                                                                    UTC_ISO_RANDOMIZED_TIME) if "time" in value.keys() else None,
                          # "has_color": value["hascolor"] if "hascolor" in value.keys() else False,
                          # "name": value["name"] if "name" in value.keys() else "unknown device name",
                          # "type": value["type"] if "type" in value.keys() else "unknown device type",
                          # "reachable": value["state"]["reachable"] if "state" in value.keys() and "reachable" in value[
                          #     "state"].keys() else False,
                          # "on": value["state"]["on"] if "state" in value.keys() and "on" in value[
                          #     "state"].keys() else False,
                          # "brightness": int(value["state"]["bri"] / 255 * 100) if "state" in value.keys() and "bri" in
                          #                                                         value["state"].keys() else 0,
                          # "hue": int(value["state"]["hue"] / 65535 * 360) if "state" in value.keys() and "hue" in value[
                          #     "state"].keys() else 0,
                          # "saturation": int(value["state"]["sat"] / 255 * 100) if "state" in value.keys() and "sat" in
                          #                                                         value["state"].keys() else 0
                          }]

        response = {"rules": response}

        return JsonResponse(response)


@login_required
@xframe_options_sameorigin
def get_rule_data(request, id):
    if request.method == "GET":
        data = get_data_from_input(request)

        response = request.get(url=DECONZ_SCHEDULE_URL + "/" + id)
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
