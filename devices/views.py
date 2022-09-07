from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def devices(response):
    return render(response, "devices.html", {})