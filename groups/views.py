from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from groups.apiCalls import putState
from groups.apiCalls import createGroup


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