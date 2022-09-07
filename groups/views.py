from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def groups(response):
    return render(response, "groups.html", {})