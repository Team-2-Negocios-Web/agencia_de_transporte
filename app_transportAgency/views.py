from django.shortcuts import render
from django.contrib.auth.decorators import login_required

 
def home(request):
    return render(request, 'transportAgency/home.html')

def progviajes(request):
    return render(request, 'transportAgency/progviajes.html')