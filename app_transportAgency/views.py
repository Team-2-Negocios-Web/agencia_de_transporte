from django.shortcuts import render
from datetime import *
import datetime as dt
from .models import *

def travels(request):

    time_today = datetime.now()
    travels = TripScheduling.objects.filter(date_trip=time_today)
    

    for t in travels:

        #hora de la ruta
        time_route = t.routes.schedule.route_schedule 

        #calcular la hora aproximada del viaje
        t1 = dt.datetime.strptime(str(time_route), '%H:%M:%S')
        t2 = dt.datetime.strptime(str(time(hour=t.routes.route_time)), '%H:%M:%S') 
        time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')

        tiempo_aproximado = (t1 - time_zero + t2).time()
        print(tiempo_aproximado)

        if time_route <= time_today.time() and t.state == "1" :
            t.state  = "2"
            t.save()
        elif tiempo_aproximado <= time_today.time() and t.state == "2":
            t.state  = "3"
            t.save()

    travels = TripScheduling.objects.filter(date_trip=time_today)
    ctx = {'travels': travels}
    return render(request, 'transportAgency/travels.html', ctx)