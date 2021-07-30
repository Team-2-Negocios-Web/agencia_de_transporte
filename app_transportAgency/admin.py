from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Seating)
admin.site.register(Bus)
admin.site.register(Schedule)
admin.site.register(Route)
admin.site.register(TripScheduling)
admin.site.register(Ticket)
admin.site.register(City)
