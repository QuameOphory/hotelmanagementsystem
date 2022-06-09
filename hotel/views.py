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
            return HttpResponsePermanentRedirect(self.get_success_url())
        return False


class RoomDetailView(generic.DetailView):
    model = Room
    template_name = 'rooms/roomdetail.html'


