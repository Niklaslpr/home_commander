from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rules.apiCalls import createSchedule

@login_required
def rules(response):
    return render(response, "rules.html", {})

@login_required
def createschedule(response):
    if response.method == 'POST':
        createSchedule(response.POST['time'], response.POST['groupID'])
    return render(response, "rules.html", {})