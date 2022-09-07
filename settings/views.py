from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def settings(response):
    return render(response, "settings.html", {})