from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404, request, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import *
import datetime as dt
from .models import *
from django.db.models import Q, F, Count, Sum


@login_required()
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

    

@login_required()
def route(request):
    trips = Route.objects.all()
    clients = Client.objects.all()

    return render(request, 'transportAgency/ticket.html', {
        'trips' : trips,
        'clients': clients,
    })

@login_required()
def ticket(request):

    if request.is_ajax() and request.method == "GET":
        #import pdb; pdb.set_trace()
        time_today = datetime.now()

        #conseguir el id de la ruta
        id_route = int(request.GET.get('route'))
        ticket_reservation = request.GET.get('ticket_reservation')
        route = Route.objects.filter(pk=id_route).first()

        quantity_ticket = Ticket.objects.values().filter(routes=id_route, ticket_reservation=ticket_reservation).annotate(passenger=Count('client')).order_by()
        
        cont = 0
        for qt in quantity_ticket:
            cont += 1

        precio = route.precio
    
        return JsonResponse({'precio': precio, 'tickets': cont})
        
    elif request.is_ajax() and request.method == "POST":
        #route=76&client=1&quantity=2&client0=1&client1=1&ticket_reservation
        #import pdb; pdb.set_trace()
        today = datetime.now().date()
        action = request.POST.get('action')

        if action == "confirm" :

            time_today = datetime.now()

            id_trip   = int(request.POST.get('route'))
            id_client = int(request.POST.get(f'client')) 
            quantity  = int(request.POST.get('quantity'))
            ticket_reservation = request.POST.get('ticket_reservation')
            convert_reservation_to_date = datetime.strptime(ticket_reservation, '%Y-%m-%d').date()

        
            route   = Route.objects.get(pk=id_trip)
            client = Client.objects.get(pk=id_client)

            trip = TripScheduling.objects.filter(date_trip=convert_reservation_to_date, routes=route).first()

            if convert_reservation_to_date < today:
                print("No puedes escoger una fecha menor que esta")
                return JsonResponse({'error' : "No puedes escoger una fecha menor que esta"})

            if trip:
                if not trip.state == "1":
                    return JsonResponse({'error': "No esta disponible",}) 
            

            html = f'''
                <p>Empleado: {request.user.client}</p>
                <p>Nombre del Cliente: {client}</p>
                <p> Ruta: {route}</p>
                <p>Cantidad de tickets: {quantity}</p>
                <p>Precio: {route.precio}</p>
                <p>Precio Total: {route.precio * quantity}</p>

            '''

            return JsonResponse({'code': html})
        else:
            #import pdb; pdb.set_trace()
            
            id_trip   = int(request.POST.get('route'))
            id_client = int(request.POST.get(f'client')) 
            quantity  = int(request.POST.get('quantity'))
            ticket_reservation = request.POST.get('ticket_reservation')
            convert_reservation_to_date = datetime.strptime(ticket_reservation, '%Y-%m-%d').date()

            route   = Route.objects.get(pk=id_trip)
            client = Client.objects.get(pk=id_client)   

            print(id_trip)                
            print(route.bus)

            employee = Client.objects.get(pk=request.user.client.pk)     
            
            if convert_reservation_to_date < today:
                
                return JsonResponse({'error' : "No puedes escoger una fecha menor que esta"})
            else: 
            # Crear el ticket

                #Traemos los tickets de esa fecha para ver si hay cupos
                date_reservation = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route).last()
                
                #Si no existe un ticketm creamos un ticket que va contener la ruta y la fecha de la reservacion
                if not date_reservation:

                    tickets = Ticket (ticket_reservation=convert_reservation_to_date,total_price = 0,routes=route)
                    tickets.save()
                
                #Volver actuarlizar la informacion de ticket
                date_reservation = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route).last()
                count_seating = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route).count()

                if count_seating > 16:
                    return JsonResponse({'error': "Ya no hay cupos"})
                else:
                    # se crea el ticket del cliente principal
                    if date_reservation:

                        #se crea el ticket para los acompañantes
                        if quantity > 1:

                                repeating_client = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route,client=client)
                                if repeating_client.exists():
                                    return HttpResponse("Este cliente ya tiene un asiento asignado para este viaje")

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
                                            employee           = employee,
                                            total_price        = route.precio * quantity,
                                            ticket_quantity    = quantity,
                                            ticket_reservation = convert_reservation_to_date,
                                            routes             = route ,
                                            bus                = route.bus,
                                                                            
                                        )
                                        tickets.save()
                                        tickets = Ticket.objects.all().last()
                                        tickets.seating.add(seat)
                                        tickets.save()
                                        break

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
                                            client_register = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route,client=client)
                                            
                                            if not client_register:
                                                tickets = Ticket.objects.all().last()
                                                tickets.seating.add(seat)
                                                tickets.save()
                                                break;
                                            else:
                                                tickets = Ticket.objects.all().last()
                                                tickets.seating.add(seat)
                                                tickets.companion.add(acomp)
                                                tickets.save()
                                                break 
                        else:

                            repeating_client = Ticket.objects.filter(ticket_reservation=convert_reservation_to_date,routes=route,client=client)
                            if repeating_client.exists():
                                return HttpResponse("Este cliente ya tiene un asiento asignado para este viaje")

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
                                        employee           = employee,
                                        total_price        = route.precio,
                                        ticket_quantity    = quantity,
                                        ticket_reservation = convert_reservation_to_date,
                                        routes             = route ,
                                        bus                = route.bus,
                                                                        
                                    )
                                    tickets.save()
                                    
                                    tickets = Ticket.objects.all().last()
                                    tickets.seating.add(seat)
                                    tickets.save()
                                    break
                return render(request, 'transportAgency/ticket.html')

@login_required()
def bus_crud(request):
    
    if request.method == "POST":
        nombre = request.POST.get('name-bus')
        bus = Bus(name_bus=nombre)
        bus.save()

        bus = Bus.objects.all().last()
        seats = Seating.objects.all()
        for s in seats:
            bus.seating.add(s)
            bus.save()

    buses = Bus.objects.all() 
    return render(request, 'transportAgency/addbus.html', {'buses' : buses,})

@login_required()
def eliminar_bus(request, id):
    Bus.objects.get(pk=id).delete()
    return redirect(reverse('transportAgency:bus_crud'))

@login_required()
def editar_bus(request, id):
    bus = get_object_or_404(Bus, pk=id)

    if request.method == 'POST':
        nombre = request.POST.get('name-bus')
        bus.name_bus = nombre
        bus.save()
        
    return render(request, 'transportagency/addbus.html', {
            'data': bus,
            'buses': Bus.objects.all()
        }, )

@login_required()
def income(request):

    if request.is_ajax() and request.method == "POST":

        date_from = request.POST.get('date-from')
        date_to   = request.POST.get('date-to')
        incomes   = Ticket.objects.values('ticket_reservation').filter(ticket_reservation__range=(date_from,date_to)).annotate(price=Sum('total_price')).order_by()

        return JsonResponse({'incomes': list(incomes)})
    
    return render(request, 'transportAgency/income.html')

@login_required()
def cliente(request):
    if request.is_ajax() and request.method == 'POST':
        dni = request.POST.get('dni')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')


        dni_exists = Client.objects.filter(dni=dni)
        if dni_exists:
            return JsonResponse({'msj': f'El numero de identidad de {dni} ya existe'})
        client = Client(dni=dni,first_name = first_name, last_name = last_name, phone = phone, email = email)
        client.save()
        return JsonResponse({'msj': 'Se ha guardado el cliente con éxito'})   
    return render(request, 'transportAgency/ticket.html')


@login_required()
def edit_customer(request, id):
    customer = get_object_or_404(Client, pk=id)
    if request.method == 'POST':
        dni = request.POST.get('dni')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        customer.dni = dni
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        customer.email = email
        customer.save()
        
        return HttpResponseRedirect('/transportAgency/customer/')
       

    return render(request, 'transportagency/customer.html',  {'c': customer, 'customers': Client.objects.all()})


@login_required()
def delete_customer(request, id):
    Client.objects.get(pk=id).delete()
    return HttpResponseRedirect('/transportAgency/customer/')



@login_required()
def customer(request):
    
    if request.user.is_superuser:

        q = request.GET.get('q')

        if q:
            customers = Client.objects.filter(dni__startswith=q) 

        else:
            customers = Client.objects.all()


        return render(request, 'transportAgency/customer.html', {
                'customers': customers
            })
        
    else:
        return HttpResponse("sdjhkhsd")


@login_required()
def cancel_trip(request):

    if request.is_ajax() and request.method == "GET":

        id_trip = int(request.GET.get('id'))
        action = request.GET.get('action')
        trip = TripScheduling.objects.get(pk=id_trip)

        if action == "confirm-cancel":
            today = datetime.now()  
            convert_to_datetime = datetime(year=today.year, month=today.month, day=today.day, hour=trip.routes.schedule.route_schedule.hour)
            one_hour_left = convert_to_datetime - timedelta(hours=1)
            
            if today >= one_hour_left:
                print("ya no se puede cancelar")
                return JsonResponse({'error':'No se puede cancelar el viaje una hora antes'})

            html = f'''
                <p>Ruta:{trip}</p>
                <strong><p>Horario: {trip.routes.schedule}</p></strong>
                <br>
                <textarea id="description" class="form-control" placeholder="Ingrese el motivo"></textarea>
                <input id="id-trip" name="id-trip" value={trip.pk} class="form-control">
                <br>
            '''
            return JsonResponse({'html':html})

        else :
            today = datetime.now()  

            description =  request.GET.get('description')
            convert_to_datetime = datetime(year=today.year, month=today.month, day=today.day, hour=trip.routes.schedule.route_schedule.hour)
            one_hour_left = convert_to_datetime - timedelta(hours=1)
            
            if today >= one_hour_left:
                return JsonResponse({'msj':'Ya no se puede cancelar'})
            else:
                trip.state = "4"
                trip.description = description
                trip.save()
                return JsonResponse({'msj': f'Se cancelo el viaje de la ruta {trip}'})


    return render(request, 'transportAgency/travels.html')

@login_required()
def details_ticket(request):

    q = request.GET.get('q')

    if q:
        tickets = Ticket.objects.filter(ticket_reservation=q)
    else:
        tickets =  Ticket.objects.all().order_by('ticket_reservation')

    

    return render(request, 'transportAgency/detailsTicket.html', {
        'tickets' : tickets,
    })



@login_required()     
def about(request):
    return render(request, 'transportAgency/about.html')

@login_required()
def register_city(request):

    if request.is_ajax() and request.method == "POST":
        city = request.POST.get('city')

        cities = City.objects.filter(name_city= city).first()

        if cities:
            return JsonResponse({'error': 'ingrese la misma cuidad'})
        else :
            cities = City(name_city=city)
            cities.save()
            return JsonResponse({'success' : 'Se ingreso correctamente el nombre de la cuidad'})

    return render(request, 'transportAgency/routes.html')


@login_required()  
def register_route(request):

    if request.is_ajax() and request.method == "POST":

        origin = int(request.POST.get('origin'))
        destiny = int(request.POST.get('destiny'))
        price = float(request.POST.get('price'))
        route_time = int(request.POST.get('route-time'))
        schedule = int(request.POST.get('schedule'))
        bus = int(request.POST.get('bus'))


        origin_id = City.objects.get(pk=origin)
        destiny_id = City.objects.get(pk=destiny)
        schedule_id = Schedule.objects.get(pk=schedule)
        bus_id = Bus.objects.get(pk=bus)

        route_exists = Route.objects.filter(origin=origin_id, destiny=destiny_id, schedule=schedule_id).first()
                
        if route_exists:
            return JsonResponse({'error': "La ruta ya existe para ese horario"})
        else:
            route = Route(
                origin     = origin_id,
                destiny    = destiny_id, 
                route_time = route_time,
                precio     = price,  
                schedule   = schedule_id,             
                bus        = bus_id,
            )
            route.save()
            return JsonResponse({'success':'Se guardo la ruta existosamente'})
       
    routes = Route.objects.all()
    cities = City.objects.all()
    schedules = Schedule.objects.all()
    buses = Bus.objects.all()
    return render(request, 'transportAgency/routes.html', {
        'routes': routes,
        'cities': cities,
        'schedules': schedules,
        'buses': buses,
    })


