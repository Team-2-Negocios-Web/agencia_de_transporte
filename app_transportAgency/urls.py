from django.urls import path
from . import views

app_name = 'transportAgency'

urlpatterns = [
    path('', views.home, name='home'),
    path('progviajes/', views.progviajes, name='progviajes')
]