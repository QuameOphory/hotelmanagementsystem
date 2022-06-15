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
    queryset = Booking.objects.filter(bookingfrom__range=(today_start_aware, today_end_aware), bookingconfirm=True)


# def searchView(request):
#     fromdate = request.get('date_from')
#     todate = request.get('to_date')

# def AvailableRoomsListView(request):
#     rooms = Room.objects.filter(roomstatus__icontains='v')
#     bookings = Booking.objects.filter(
#         Q(bookingstatus = 'Cancel') | Q(bookingstatus = 'Unattended') # same as ~Q(bookingstatus = 'Checkedin)
#     )
#     bookedroomlist = []
#     for booking in bookings:
#         if not booking.bookingconfirm:
#             bookedroomlist.append(booking.bookingroom)
#     context = {
#         'rooms': rooms,
#         'bookedroomlist': bookedroomlist
#     }
#     return render(request, 'rooms/homelist.html', context)



class AvailableRoomsListView(generic.ListView):
    queryset = Room.objects.filter(roomstatus__icontains='v')
    template_name = 'rooms/homelist.html'
    context_object_name = 'availablerooms'

    bookings = Booking.objects.filter(
        Q(bookingstatus = 'Cancel') | Q(bookingstatus = 'Unattended') # same as ~Q(bookingstatus = 'Checkedin)
    )
    bookedroomlist = []
    for booking in bookings:
        if all([booking.bookingconfirm is not None, booking.bookingconfirm is False]):
            bookedroomlist.append(booking.bookingroom)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookedroomlist'] = self.bookedroomlist
        return context
