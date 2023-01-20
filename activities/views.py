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
    if request.method == 'GET':
        print(request.GET)
        a = request.GET['a']
        b = request.GET['b']
        print(a, b)
        
        last_entries = LogEntry.objects.order_by('-timestamp')[int(a):int(b)]
        logs = {}
        x = 0
        while x < 10:
            try:
                print('hallo',last_entries[x])
                logs['timestamp'+str(x)] = str(last_entries[x].timestamp.strftime("%d.%m.%Y, %H:%M"))
                logs['message'+str(x)] = last_entries[x].message
                x = x+1
                print(logs)
    
                
            except: 
                print("Keine weiteren Dinge")
                logs["timestamp0"] = "stop"
                x = 10
            
        return JsonResponse(logs)
        
