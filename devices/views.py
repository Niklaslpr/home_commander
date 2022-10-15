from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from devices.apiCalls import putstate1
from devices.apiCalls import putstate2
from devices.apiCalls import putbri
from devices.apiCalls import puthue

from django.views.decorators.clickjacking import xframe_options_sameorigin


@login_required
def devices(response):
    if response.method == 'POST':
        putstate1(response.POST['state'])
    return render(response, "devices.html", {})


def turnonoff(response):
    if response.method == 'POST':
        putstate2(response.POST['state'])
    return render(response, "devices.html", {})


def setbri(response):
    if response.method == 'POST':
        putbri(response.POST['bri'])
    return render(response, "devices.html", {})


def sethue(response):
    if response.method == 'POST':
        puthue(response.POST['hue'], response.POST['sat'])
    return render(response, "devices.html", {})


@login_required
@xframe_options_sameorigin
def get_device_data(request):
    if request.method == "POST":
        # print("TEST: ", request.readline())

        test = request.read()

        print(test.decode("utf-8"))

        test = test.decode("utf-8")

        if test.split("&")[-1] == "name=test123":
            return JsonResponse({"test": "xyz"})

        return JsonResponse({"test": "abcdef"})
