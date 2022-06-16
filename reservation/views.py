from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Booking
from .forms import BookingForm
from hotel.models import Room
from django.http.response import Http404
from datetime import date, datetime
import pytz
from django.db.models import Q

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
            # return Http404()
            else:
                return render(request, self.template_name, {'form': form})


class BookingDetailView(generic.DetailView):
    model = Booking
    context_object_name = 'booking'
    # TODO: design booking detail html page
    template_name = 'reservations/bookingdetail.html'

class BookingListView(generic.ListView):
    model = Booking
    context_object_name = 'bookings'
    # TODO: design booking detail html page
    template_name = 'reservations/bookinglist.html'


class TodayBookingListView(generic.ListView):
    utc = pytz.UTC
    # TODO: design today booking detail html page
    template_name = 'reservations/todaybookinglist.html'
    context_object_name = 'todaybookings'
    today_start = datetime(date.today().year, date.today().month, date.today().day)
    today_end = today_start = datetime(date.today().year, date.today().month, date.today().day, 23, 59, 59)
    today_start_aware = utc.localize(today_start)
    today_end_aware = utc.localize(today_end)
    queryset = Booking.objects.filter(bookingfrom__range=(today_start_aware, today_end_aware), bookingconfirm=True).select_related('bookingroom')


class AvailableRoomsListView(generic.ListView):
    template_name = 'rooms/homelist.html'
    context_object_name = 'rooms'
    queryset = Room.objects.filter(
        Q(booking__bookingconfirm=False),
        Q(booking__bookingstatus='Unattended') | Q(booking__bookingstatus='Cancel') |
        Q(booking=None)
    )
