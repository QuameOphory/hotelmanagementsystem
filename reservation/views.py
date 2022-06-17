from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Booking
from .forms import BookingForm
from hotel.models import Room
from django.http.response import Http404
from datetime import date, datetime, timedelta
import pytz
from django.db.models import Q

# Create your views here.

class BookingCreateView(generic.CreateView):
    form_class = BookingForm
    template_name = 'reservations/bookingcreate.html'

    def get(self, request, *args, **kwargs):
        form = self.get_form_class()
        form = form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            url = kwargs.get('slug')
            room = Room.objects.get(roomnumber_url=url)
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
                return HttpResponseRedirect(reverse('booking_list'))
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
    model = Room

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(
            Q(booking__bookingconfirm=True) |
            Q(booking__bookingstatus='Checkedin')
        )
        qs = qs.exclude(
            booking__bookingto__gt=datetime.now()
        )
        return qs


class SearchRoomListView(generic.ListView):
    template_name = 'rooms/homelist.html'
    context_object_name = 'rooms'
    model = Room

    def get_queryset(self):
        try:
            datefrom = self.request.GET['fromdate']
            datefrom = datetime.now() if datefrom == '' else datefrom
            if isinstance(datefrom, str):
                split_date = str(datefrom).split('-')
            yy, mm, dd = split_date[0], split_date[1], split_date[2]
            datefrom = datetime(int(yy), int(mm), int(dd), 0, 0, 0)
        except KeyError as ke:
            datefrom = datetime.now()
        else:
            try:
                nights = self.request.GET['nights']
                nights = 1 if nights == '' else int(nights)
            except KeyError:
                nights = 1
            rt = datefrom + timedelta(days=nights)
            qs = super().get_queryset()
            qs = qs.exclude(
                Q(booking__bookingstatus='Checkedin')
            )
            qs = qs.exclude(
                Q(booking__bookingfrom__lt=datefrom), 
                Q(booking__bookingconfirm=True), 
                Q(booking__bookingTo__gt=datefrom)
            )
            qs = qs.exclude(
                Q(booking__bookingfrom__gt=datefrom),
                Q(booking__bookingfrom__lt=rt),
                Q(booking__bookingconfirm=True)
            )
            return qs
