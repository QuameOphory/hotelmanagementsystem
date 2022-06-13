from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room
from uuid import uuid4
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from number_generator import generate_number_with_date
from datetime import timedelta, datetime

def generateBookingNumber():
    bookings = Booking.objects.all().order_by('-created_at')
    return generate_number_with_date('B', bookings)

# Create your models here.
class Booking(models.Model):
    """Model definition for Booking."""
    bookingnumber = models.CharField(_("Booking Number"), max_length=120, default=generateBookingNumber)
    # TODO: change user model  to client model
    bookingby = models.ForeignKey(User, verbose_name=_("Client"), on_delete=models.CASCADE)
    bookingroom = models.ForeignKey(Room, verbose_name=_("Room"), on_delete=models.CASCADE)
    bookingfrom = models.DateTimeField(_("From"), default=timezone.now)
    bookingnights = models.PositiveIntegerField(_("Number of Nights"), default=1)
    bookingconfirm = models.BooleanField(_("Booking Confirmed"), null=True, blank=True)
    # is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    bookingcontent = models.TextField(_("Comment"))

    @property
    def bookingto(self):
        return self.bookingfrom + timedelta(days=self.bookingnights)

    @property
    def is_active(self):
        if timezone.now() >= self.bookingto:
            return False
        return True

    class Meta:
        """Meta definition for Booking."""

        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        """Unicode representation of Booking."""
        pass

    def get_absolute_url(self):
        return reverse("booking_detail", kwargs={"pk": self.pk})