import imp
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    
    class Meta:
        model = Room
        fields = ('roomtype', 'roomnumber', 'roomcapacity', 'roombed', 'roombath', 'roomdimension', 'roomextras',)
    
