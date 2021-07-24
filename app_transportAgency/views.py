from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from datetime import *
import datetime as dt
from .models import *
from django.db.models import Q, F



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
    trips = TripScheduling.objects.filter(state="3")


    clients = Client.objects.all()

    return render(request, 'transportAgency/ticket.html', {
        'trips' : trips,
        'clients': clients,
    })


def route(request):

    if request.is_ajax() and request.method == "GET":
        #import pdb; pdb.set_trace()

        id_route = request.GET.get('route')
        route = Route.objects.filter(pk=id_route).first()
        precio = route.precio
    
        return JsonResponse({'precio': precio,})
        
    elif request.method == "POST":
        #route=76&client=1&quantity=2&client0=1&client1=1&ticket_reservation
        #import pdb; pdb.set_trace()
        today = datetime.now().date()

        id_trip   = int(request.POST.get('route'))
        id_client = int(request.POST.get(f'client')) 
        quantity  = int(request.POST.get('quantity'))
        ticket_reservation = request.POST.get('ticket_reservation')
        convert_reservation_to_date = datetime.strptime(ticket_reservation, '%Y-%m-%d').date()


        route   = Route.objects.get(pk=id_trip)
        client = Client.objects.get(pk=id_client)        
        
        if convert_reservation_to_date < today:
            return HttpResponse("No puedes escoger una fecha menor que esta")
        else: 
        # Crear el ticket

            #Traemos los tickets de esa fecha para ver si hay cupos
            date_reservation = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route).last()
            
            
            if not date_reservation:
                instance_cliente = Client.objects.get(pk=4)
                tickets = Ticket (ticket_reservation=convert_reservation_to_date,client = instance_cliente,total_price = 0,routes=route)
                tickets.save()
                
            date_reservation = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route).last()
            count_seating = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route).count()

            if count_seating > 8:
                return HttpResponse("ya no hay cupos")
            else:
                if date_reservation:

                    repeating_client = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route,client=client)
                    if repeating_client.exists():
                        return HttpResponse("Este cliente ya tiene un asiento asignado")

                    seats = Seating.objects.all()
                    for s in seats[::-1]:
                
                        seat = Seating.objects.get(pk=s.pk)
                        exist_seat = Ticket.objects.filter(seating=seat,ticket_reservation=convert_reservation_to_date,routes=route)
                        if exist_seat.exists():
                            print("Este asiento en esta ruta ya esta ocupado")
                        else:
                            print(f"Este asiento no tiene cupo {date_reservation.seating}")
                            tickets = Ticket (
                                client             = client,
                                total_price        = route.precio,
                                ticket_quantity    = quantity,
                                ticket_reservation = convert_reservation_to_date,
                                routes             = route ,
                                bus                = route.bus,
                                seating            = seat # este no lo tenemos                                      
                            )
                            tickets.save()
                            break

                    if quantity > 1:
                            for i in range(quantity - 1):
                                acomp = int(request.POST.get(f'client{i}')) 
                                acomp = Client.objects.get(pk=acomp)
                                seats = Seating.objects.all()

                                repeating_client = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route,companion=acomp)
                                if repeating_client.exists():
                                    return HttpResponse("Este cliente ya tiene un asiento asignado")

                                for s in seats[::-1]:
                                    seat = Seating.objects.get(pk=s.pk)
                                    exist_seat = Ticket.objects.filter(seating=seat,ticket_reservation=convert_reservation_to_date,routes=route)
                                    if exist_seat.exists():
                                        print("Este asiento en esta ruta ya esta ocupado")
                                    else:
                                        print(f"Este asiento no tiene cupo {date_reservation.seating}")
                                        tickets = Ticket (
                                            client             = client,
                                            companion          = acomp,       
                                            total_price        = route.precio * quantity,
                                            ticket_quantity    = quantity,
                                            ticket_reservation = convert_reservation_to_date,
                                            routes             = route ,
                                            bus                = route.bus,
                                            seating            = seat # este no lo tenemos                                      
                                        )
                                        tickets.save()
                                        break 

            return render(request, 'transportAgency/ticket.html')



    
        
        
           
     