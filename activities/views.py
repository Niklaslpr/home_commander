from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def activities(response):
    return render(response, "activities.html", {})
