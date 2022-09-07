from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def rules(response):
    return render(response, "rules.html", {})