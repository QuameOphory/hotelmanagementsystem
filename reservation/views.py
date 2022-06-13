from django.shortcuts import render
from django.views import generic
from .models import Booking

# Create your views here.

class BookingCreateView(generic.CreateView):
    model = Booking
    
