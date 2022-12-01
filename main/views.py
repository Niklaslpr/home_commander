from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse

TEST = False

def home(response):
    return render(response, "main/home.html", {})

def weather(request):
    if request.method == "GET":

        if not TEST:
            response_tmp = requests.get(url="https://api.openweathermap.org/data/2.5/weather?lat=51.244327040560144&lon=6.794709913902105&appid=0f40bf985000b41f806f413e6adcb377")
            response_tmp = response_tmp.json()
            main_tmp = response_tmp["main"]
            temp_tmp = round(main_tmp["temp"] - 273.15)
            weather_tmp = response_tmp["weather"]
            code_tmp = weather_tmp[0]
            code_tmp = code_tmp["id"]

            dict_tmp = {"temp" : temp_tmp, "code": code_tmp}
        else:
            dict_tmp = {"temp": 9, "code": 511}
        return JsonResponse(dict_tmp)