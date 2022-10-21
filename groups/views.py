from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from groups.apiCalls import putState


@login_required
def groups(response):
    return render(response, "groups.html", {})

@login_required
def grouponoff(response):
    if response.method == 'POST':
        putState(response.POST['state'], response.POST['groupID'])
    return render(response, "groups.html", {})