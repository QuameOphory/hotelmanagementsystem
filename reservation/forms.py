from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    """Form definition for Booking."""

    class Meta:
        """Meta definition for Bookingform."""

        model = Booking
        fields = ('bookingby', 'bookingfrom', 'bookingnights', 'bookingcontent')
