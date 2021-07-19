from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Seating(models.Model):
    name_seating = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.name_seating}'

class Bus(models.Model): 
    name_bus = models.CharField(max_length=50)
    seating = models.ManyToManyField(Seating)

    def __str__(self):
        return f'{self.name_bus}'
    
    class Meta:
        verbose_name_plural = 'Buses'
    

class SeatAssignment(models.Model):
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE, blank=True, null=True)
    seating = models.OneToOneField(Seating,on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.bus} {self.seating} | {self.client}'
    
class Schedule(models.Model):
    route_schedule = models.TimeField()
    def __str__(self):
        return f'{self.route_schedule}'

class Route(models.Model):
    origin = models.TextField()
    destiny = models.TextField()
    route_time = models.TimeField()
    precio = models.FloatField()
    schedule = models.ManyToManyField(Schedule)

    def __str__(self):
        return f'origen: {self.origin} - destino: {self.destiny} '

class TripScheduling(models.Model):
    STATE = {
       ('1', 'A tiempo'),
       ('2', 'en viaje'),
       ('3', 'finalizado'),
       ('4', 'cancelado'),
   }
    date_trip = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=1, choices=STATE, default='1')
    routes = models.ForeignKey(Route,  on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return f' Estado: {self.state} | Cita: {self.date_trip}'

class Ticket(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True,blank=True, null=True )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    ticket_reservation = models.DateTimeField()
    ticket_available = models.IntegerField(default=16)
    ticket_quantity = models.IntegerField() # 3
    total_price = models.FloatField()
    routes = models.ForeignKey(Route,on_delete=models.CASCADE, null=True, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)


