from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room
from uuid import uuid4
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Booking(models.Model):
    """Model definition for Booking."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    bookingnumber = models.CharField(_("Booking Number"), max_length=120)
    # TODO: change user to clients
    bookingby = models.ForeignKey(User, verbose_name=_("Client"), on_delete=models.CASCADE)
    bookingroom = models.ForeignKey(Room, verbose_name=_("Room"), on_delete=models.CASCADE)
    bookingfrom = models.DateTimeField(_("From"), default=timezone.now)
    bookingto = models.DateTimeField(_("To"), default=timezone.now)
    bookingconfirm = models.BooleanField(_("Booking Confirmed"), default=False)


    class Meta:
        """Meta definition for Booking."""

        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        """Unicode representation of Booking."""
        pass
