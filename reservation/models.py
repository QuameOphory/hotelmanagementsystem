from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room
from uuid import uuid4
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from number_generator import generate_number_with_date

def generateBookingNumber():
    bookings = Booking.objects.all().order_by('-created_at')
    return generate_number_with_date('B', bookings)

# Create your models here.
class Booking(models.Model):
    """Model definition for Booking."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    bookingnumber = models.CharField(_("Booking Number"), max_length=120, default=generateBookingNumber)
    # TODO: change user to clients
    bookingby = models.ForeignKey(User, verbose_name=_("Client"), on_delete=models.CASCADE)
    bookingroom = models.ForeignKey(Room, verbose_name=_("Room"), on_delete=models.CASCADE)
    bookingfrom = models.DateTimeField(_("From"), default=timezone.now)
    bookingto = models.DateTimeField(_("To"), default=timezone.now)
    bookingconfirm = models.BooleanField(_("Booking Confirmed"), null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    extra_content = models.TextField(_("Comment"))


    class Meta:
        """Meta definition for Booking."""

        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        """Unicode representation of Booking."""
        pass
