from django.shortcuts import render
from django.urls import is_valid_path
from django.views import generic
from .models import Booking
from .forms import BookingForm

# Create your views here.

class BookingCreateView(generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'reservations/bookinglist.html'