from django.urls import path
from . import views

app_name = 'transportAgency'

urlpatterns = [
    path('', views.travels, name="travels_view" ),
    path('ticket/', views.route, name="ticket_view" ),
    path('ticket/ajax', views.ticket, name="ajax_view" ),
    path('income/', views.income, name="income_view"),
]