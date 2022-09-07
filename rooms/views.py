from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def rooms(response):
    return render(response, "rooms.html", {})