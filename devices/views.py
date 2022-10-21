from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from devices.apiCalls import putstate1
from devices.apiCalls import putstate
from devices.apiCalls import putbri
from devices.apiCalls import puthue



@login_required
def devices(response):
    if response.method == 'POST':
        putstate1(response.POST['state'])
    return render(response, "devices.html", {})

@login_required
def turnonoff(response):
    if response.method == 'POST':
        putstate(response.POST['state'], response.POST['lightID'])
    return render(response, "devices.html", {})

@login_required
def setbri(response):
    if response.method == 'POST':
        putbri(response.POST['bri'])
    return render(response, "devices.html", {})

@login_required
def sethue(response):
    if response.method == 'POST':
        puthue(response.POST['hue'], response.POST['sat'])
    return render(response, "devices.html", {})