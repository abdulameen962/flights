import imp
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import *
# Create your views here.
def index(request):
    return render(request, "flights/index.html",{
        "flights": flight.objects.all()
    })
    
def Flight(request, flight_id):
    flightn = flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html",{
        "flight": flightn,
        "passengers": flightn.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flightn).all(),
    })
    
def book(request, flight_id):
    if request.method == "POST":
        flightn = flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flightn)
        return HttpResponseRedirect(reverse("flights:flight", args=(flightn.id,)))