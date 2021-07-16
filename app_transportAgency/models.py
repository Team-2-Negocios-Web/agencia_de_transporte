from django.db import models

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
# 2, 4, 5, 7, 
class Seating(models.Model):
    name_seating = models.CharField(max_length=3)

class Bus(models.Model): 
    name_bus = models.CharField(max_length=50)
    seatings = models.IntegerField(default=48)
    name_seating = models.ManyToManyField(Seating)

    def __str__(self):
        return f'{self.name_bus} - cupos: {self.seating}'

class Schedule(models.Model):
    route_schedule = models.DateTimeField()

class Route(models.Model):
    origin = models.TextField()
    destiny = models.TextField()
    route_time = models.TimeField()
    precio = models.FloatField()
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f'{self.origin} - {self.destiny}'


class TripScheduling(models.Model):
    STATE = {
       ('1', 'A tiempo'),
       ('2', 'en viaje'),
       ('3', 'finalizado'),
       ('4', 'cancelado'),
   }
    date_trip = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=1, choices=STATE, default='1')
    routes = models.ManyToManyField(Route)


class Ticket(models.Model):
    date_ticket = models.DateTimeField(auto_now_add=True)
    available = models.IntegerField()
    ticket_quantity = models.IntegerField() # 3
    total_price = models.FloatField()
    routes = models.ForeignKey(Route,on_delete=models.CASCADE, null=True, blank=True)
    seating = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)
   