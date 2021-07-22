from django.shortcuts import render
from datetime import *
import datetime as dt
from .models import *
from django.db.models import Q



def travels(request):
    # fecha local del sistema
    time_today = datetime.now()

    #consulta del model Programacion de viajes
    travels = TripScheduling.objects.filter(date_trip=time_today) # fecha y hora local

    # Años, mes , dia y hora de la fecha local
    year = time_today.year
    month =time_today.month
    day = time_today.day
    hour = time_today.hour
    minute = time_today.minute

   
    
    #Si la varieble travels tiene datos verificar y cambiar estados segun la fecha y hora
    if travels :
        for t in travels:

            #hora de la ruta
            time_route = t.routes.schedule.route_schedule 

            #calcular la hora aproximada del viaje
            t1 = dt.datetime.strptime(str(time_route), '%H:%M:%S')
            t2 = dt.datetime.strptime(str(time(hour=t.routes.route_time)), '%H:%M:%S') 
            time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
            tiempo_aproximado = (t1 - time_zero + t2).time()

            #Calculo entre horas y fechas para poder saber el estado de las rutas 
            t3 = dt.datetime(year, month, day) + dt.timedelta(hours=tiempo_aproximado.hour, minutes=tiempo_aproximado.minute, seconds=0)
            t4 = dt.datetime(year, month, day) + dt.timedelta(hours=hour, minutes=minute, seconds=0)

            # Si la hora de la ruta es menor que la hora actual, entonces cambiamos a viaje ya que nuestra hora local es principal para este caso
            if time_route <= time_today.time() and t.state == "1" :
                t.state  = "2"
                t.save()
                
            # Si t4(hora actual) es mayor t3(tiempo aproximado de la rutaa) entonces cambiar el estado a Finalizado    
            elif t4 >= t3 and t.state == "2":
                t.state  = "3"
                t.save()
                
        
        #Hacemos consulta
        travels = TripScheduling.objects.filter(Q(date_trip=time_today) | Q(state="2")).order_by('routes')
        ctx = {'travels': travels}
        return render(request, 'transportAgency/travels.html', ctx)
    else:
        #Si ya es el dia siguiente y no se ha programado los viajes entonces hacemos lo siguiente

        #Consulta para obtener todas nuestras rutas
        routes = Route.objects.all()
        

        for route in routes:

            #instancia para obtener el id de las rutas
            route_id = Route.objects.get(pk=route.pk)

            #Creamos nuestras rutas y guardamos
            travels = TripScheduling(state="1", routes=route_id)
            travels.save()

        travels = TripScheduling.objects.filter(Q(date_trip=time_today) | Q(state="2")).order_by('routes')
        ctx = {'travels': travels}
        return render(request, 'transportAgency/travels.html', ctx)

    


def ticket(request):
    routes = Route.objects.all()
    clients = Client.objects.all()

    return render(request, 'transportAgency/ticket.html', {
        'routes' : routes,
        'clients': clients,
    })
