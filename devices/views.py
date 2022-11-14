from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import time
from devices.apiCalls import putstate1
from devices.apiCalls import putstate
from devices.apiCalls import putbri
from devices.apiCalls import puthue
from devices.apiCalls import startscan



@login_required
def devices(request):
    if request.method == 'POST':
        putstate1(request.POST['state'])
    return render(request, "devices.html", {})

@login_required
def turnonoff(request):
    if request.method == 'POST':
        putstate(request.POST['state'], request.POST['lightID'])
    return render(request, "devices.html", {})

@login_required
def setbri(request):
    if request.method == 'POST':
        putbri(request.POST['bri'])
    return render(request, "devices.html", {})

@login_required
def sethue(request):
    if request.method == 'POST':
        puthue(request.POST['hue'], request.POST['sat'])
    return render(request, "devices.html", {})


@login_required
def startsearch(request):
    if request.method == 'POST':
        newdict = startscan()
        if not newdict:
            return HttpResponse('none')
        else: return JsonResponse(newdict)
    # data = {'1':{'manufacturername': 'Philips', 'name': 'Light'}, '2':{'manufacturername': 'Philips2', 'name': 'Light2'}}

    # return render(request, "devices.html", {'test': 'test'}) #nur Änderung zurückgeben

