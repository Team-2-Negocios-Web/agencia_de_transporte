from django.urls import path
from . import views

app_name = 'transportAgency'

urlpatterns = [
    path('', views.travels, name="travels_view"),
    path('ticket/', views.route, name="ticket_view"),
    path('ticket/ajax', views.ticket, name="ajax_view"),
    path('ticket/client', views.cliente, name="client_view"),
    path('buses/', views.list_buses, name="list_buses"),
    path('income/', views.income, name="income_view"),
    path('about/', views.about, name="about"),
    path('travels/', views.cancel_trip, name="cancel_trip"),
    path('details/', views.details_ticket, name="details_ticket"),
    path('customer/', views.customer, name="customer"),
    path('customer_crud/<int:id>/edit_customer/', views.edit_customer, name='edit_customer'),
    path('customer_crud/<int:id>/delete_customer/', views.delete_customer, name='delete_customer'),
    path('routes/', views.register_route, name="register_route"),
    path('city/', views.register_city, name="register_city"),
    path('bus_crud/', views.bus_crud, name="bus_crud"),
    path('bus_crud/<int:id>/eliminar/', views.eliminar_bus, name='eliminar_bus'),
    path('bus_crud/<int:id>/editar/', views.editar_bus, name='editar_bus'),
]
 
