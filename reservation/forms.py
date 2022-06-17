import time
from django import forms
from .models import Booking
# from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date
import pytz

utc = pytz.UTC

class BookingForm(forms.ModelForm):
    """Form definition for Booking."""

    class Meta:
        """Meta definition for Bookingform."""

        model = Booking
        fields = ('bookingby', 'bookingfrom', 'bookingnights', 'bookingcontent')

    def clean_bookingfrom(self, *args, **kwargs):
        bookingdate = self.cleaned_data.get('bookingfrom')
        d = date(bookingdate.year, bookingdate.month, bookingdate.day)
        if date.today() > d:
            raise forms.ValidationError(_("You can't book for days in the past."))
        return bookingdate

    def clean_bookingby(self, *args, **kwargs):
        bookingby = self.cleaned_data.get('bookingby')
        bookings = Booking.objects.all()
        for booking in bookings:
            if all([booking.bookingby == bookingby, booking.is_active]):
                raise forms.ValidationError('This user has already made a booking')
        return bookingby