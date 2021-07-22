from django.db import models
from datetime import *


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    phone      = models.CharField(max_length=50)
    email      = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Seating(models.Model):
    name_seating = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.name_seating}'

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
    
    

class SeatAssignment(models.Model):
    bus     = models.ForeignKey(Bus,on_delete=models.CASCADE, blank=True, null=True)
    seating = models.OneToOneField(Seating,on_delete=models.CASCADE, blank=True, null=True)
    client  = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.bus} {self.seating} | {self.client}'
    
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
    STATE = {
       ('1', 'A tiempo'),
       ('2', 'en viaje'),
       ('3', 'finalizado'),
       ('4', 'cancelado'),
   }
    date_trip = models.DateField(auto_now_add=True)
    state     = models.CharField(max_length=1, choices=STATE)
    routes    = models.ForeignKey(Route,  on_delete=models.PROTECT, blank=True, null=True)


    def __str__(self):
        return f' Estado: {self.state} | Cita: {self.date_trip}'


class Ticket(models.Model):
    creation_date      = models.DateTimeField(auto_now_add=True,blank=True, null=True )
    client             = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    ticket_reservation = models.DateTimeField()
    ticket_available   = models.IntegerField(default=16)
    ticket_quantity    = models.IntegerField() # 3
    total_price        = models.FloatField()
    routes             = models.ForeignKey(Route,on_delete=models.CASCADE, null=True, blank=True)
    bus                = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def available_tickets(self):
        count_tickets = SeatAssignment__set.count()
        return self.ticket_available - count_tickets

