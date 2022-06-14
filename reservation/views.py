from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Booking
from .forms import BookingForm
from hotel.models import Room
from django.http.response import Http404, HttpResponse

# Create your views here.

class BookingCreateView(generic.CreateView):
    form_class = BookingForm
    template_name = 'reservations/bookingcreate.html'

    def get(self, request, *args, **kwargs):
        form = self.get_form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            url = kwargs.get('slug')
            # print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            # print(url)
            # print('\nkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            room = Room.objects.get(roomnumber_url=url)
            # print('--------------------------')
            # print(room.roomnumber)
            # print('--------------------------')
        except KeyError as ke:
            print(f'"{url}" not found')
            return Http404()
        except Exception as e:
            print('Room not found')
            return Http404()
        else:
            if form.is_valid():
                booking = form.save(commit=False)
                booking.bookingroom = room
                booking.save()
                # return reverse('booking_detail', kwargs={"id": booking.id, "slug": booking.bookingroom.roomnumber_url})
                return HttpResponseRedirect(reverse('booking_list'))


class BookingDetailView(generic.DetailView):
    model = Booking
    template_name = 'reservations/bookingdetail.html'

class BookingListView(generic.ListView):
    model = Booking
    template_name = 'reservations/bookinglist.html'