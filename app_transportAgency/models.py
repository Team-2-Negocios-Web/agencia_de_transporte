from django.db import models
from datetime import *
from django.contrib.auth.models import User


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    phone      = models.CharField(max_length=50)
    email      = models.CharField(max_length=50)
    user       = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.pk}'
    

class Seating(models.Model):
    name_seating = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.name_seating} {self.pk}'

class Bus(models.Model): 
    name_bus = models.CharField(max_length=50)
    seating  = models.ManyToManyField(Seating)

    def __str__(self):
        return f'{self.name_bus}'
    
    class Meta:
        verbose_name_plural = 'Buses'

class City(models.Model):
    name_city = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name_city

    class Meta:
        verbose_name_plural = 'Cities'
    
    
    
class Schedule(models.Model):
    route_schedule = models.TimeField()

    def __str__(self):
        return f'{self.route_schedule}'

class Route(models.Model):
    origin     = models.ForeignKey(City, related_name="origin_city", on_delete=models.CASCADE)
    destiny    = models.ForeignKey(City, related_name="destiny_city", on_delete=models.CASCADE)
    route_time = models.IntegerField()
    precio     = models.FloatField()
    schedule   = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null=True)
    bus        = models.ForeignKey(Bus, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'Origen: {self.origin} - Destino: {self.destiny} | Destino: {self.schedule}'

class TripScheduling(models.Model):
    # ==> id: 27
    STATE = {
       ('1', 'A tiempo'),
       ('2', 'En viaje'),
       ('3', 'Finalizado'),
       ('4', 'Cancelado'),
   }
    date_trip   = models.DateField(auto_now_add=True)
    state       = models.CharField(max_length=1, choices=STATE)
    routes      = models.ForeignKey(Route,  on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(blank=True, null=True) 


    def __str__(self):
        return f' Origen: {self.routes.origin} - Destino: {self.routes.destiny} | Estado: {self.state}'



class Ticket(models.Model):
    creation_date      = models.DateTimeField(auto_now_add=True,blank=True, null=True )
    client             = models.ForeignKey(Client,related_name="cliente_ticket", on_delete=models.CASCADE, blank=True, null=True)
    companion          = models.ForeignKey(Client,related_name="companion_tciket", on_delete=models.CASCADE, blank=True, null=True)
    ticket_reservation = models.DateField(blank=True, null=True)
    ticket_available   = models.IntegerField(default=16, blank=True, null=True)
    ticket_quantity    = models.IntegerField(blank=True, null=True) # 3
    total_price        = models.FloatField()
    routes             = models.ForeignKey(Route,on_delete=models.CASCADE, null=True, blank=True)
    trips              = models.ForeignKey(TripScheduling, on_delete=models.CASCADE, null=True, blank=True) #27 ==>
    bus                = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)
    seating            = models.ForeignKey(Seating,on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Fecha de reservacion : {self.ticket_reservation}  {self.pk} '



