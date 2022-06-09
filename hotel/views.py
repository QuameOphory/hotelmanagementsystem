from django.shortcuts import render
from django.views import generic
from .models import Room
# Create your views here.


class RoomListView(generic.ListView):
    model = Room