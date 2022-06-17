from gc import get_objects
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views import generic
from .models import Room
from .forms import RoomForm
from django.shortcuts import HttpResponsePermanentRedirect
# Create your views here.


class RoomListView(generic.ListView):
    model = Room
    template_name = 'rooms/homelist.html'
    context_object_name = 'rooms'


class RoomCreateView(generic.CreateView):
    form_class = RoomForm
    template_name = 'rooms/roomcreate.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            room = form.save()
            room.save()
            return HttpResponsePermanentRedirect(reverse('room_detail', kwargs={'slug': room.roomnumber_url}))


class RoomDetailView(generic.DetailView):
    model = Room
    slug_field = 'roomnumber_url'
    context_object_name = 'room'
    template_name = 'rooms/roomdetail.html'

    
    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        room = self.get_object()
        bookings = room.booking_set.all()
        if bookings:
            context['bookings'] = bookings
            return context
        return context


class RoomDeleteView(generic.DeleteView):
    model = Room
    slug_field = 'roomnumber_url'
    context_object_name = 'room'
    success_url = reverse_lazy('room_list')
    template_name = 'rooms/room_confirm_delete.html'

    
class RoomUpdateView(generic.UpdateView):
    model = Room
    fields = ('roomtype', 'roomnumber', 'roomstatus', 'roomcapacity', 'roombed', 'roombath', 'roomdimension', 'roomextras', 'is_available')
    slug_field = 'roomnumber_url'
    context_object_name = 'room'
    template_name = 'rooms/roomupdate.html'
