from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from activities.models import LogEntry
from datetime import datetime
import pytz

@login_required
def settings(request):
    username = request.user.get_username()
    email = request.user.email

    return render(request, "options.html", {'username':username, 'email':email})

def get_all_users(request):
    if request.method == 'POST':
        all_users = list(User.objects.values())
        tmpdict = {}
        tmp = 0
        for x in all_users:
            if x['last_login'] is None:
                last_login = 'Noch nicht angemeldet'
            else:
                last_login = x['last_login'].astimezone(pytz.timezone('Europe/Berlin')).strftime('%d.%m.%Y %H:%M:%S')
            tmpstr = x['username'] + ', ' + str(last_login)
            tmpdict[tmp] = tmpstr
            tmp += 1
    return JsonResponse(tmpdict)

def delete_user(request):
    if request.method == 'POST':
        username = request.POST['user']
        if username == 'admin':
            print(username + ' kann nicht gelöscht werden')
        else:
            u = User.objects.get(username = username)
            u.delete()
            print(username + " wurde gelöscht")
            new_log_entry = LogEntry(message="User " + username + " wurde gelöscht")
            new_log_entry.save()
            
            # TODO: delete Favorite-Group in deCONZ
            
    return HttpResponse('erfolgreich')
