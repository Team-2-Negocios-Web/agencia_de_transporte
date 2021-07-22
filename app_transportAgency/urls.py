from django.urls import path
from . import views

app_name = 'transportAgency'

urlpatterns = [
    path('', views.travels, name="travels_view" ),
    path('ticket/', views.ticket, name="ticket_view" ),
]