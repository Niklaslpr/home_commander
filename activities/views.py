from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from activities.models import LogEntry
from datetime import datetime
from django.http import HttpResponse
from django.http import JsonResponse

@login_required
def activities(response):
    last_entries = LogEntry.objects.order_by('-timestamp')[:10]
    
    
    logs = {}
    x = 0
    while x < 10:
        logs['timestamp'+str(x)] = str(last_entries[x].timestamp.strftime("%d.%m.%Y, %H:%M"))
        logs['message'+str(x)] = last_entries[x].message
        
        
        x = x+1    
    print(logs) 
    
    return render(response, "activities.html", logs)

def load_logs(request):
    if request.method == 'POST':
        a = request.POST['a']
        b = request.POST['b']
        print(a, b)
        
        last_entries = LogEntry.objects.order_by('-timestamp')[10:20]
        logs = {}
        x = 0
        while x < 10:
            print('hallo',last_entries[x])
            logs['timestamp'+str(x)] = str(last_entries[x].timestamp.strftime("%d.%m.%Y, %H:%M"))
            logs['message'+str(x)] = last_entries[x].message
            x = x+1  
             
        print(logs)
    
        return JsonResponse(logs)
