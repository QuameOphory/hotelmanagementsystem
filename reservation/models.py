from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room
from uuid import uuid4
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from number_generator import generate_number_with_date
from datetime import timedelta, datetime
from django.db.models.signals import post_save, post_delete

def generateBookingNumber():
    # TODO: for every day, booking numbers must start
    bookings = Booking.objects.all().order_by('-created_at')
    return generate_number_with_date('B', bookings)

# Create your models here.
class Booking(models.Model):
    """Model definition for Booking."""
    # TODO: add validations for past dates
    bookingnumber = models.CharField(_("Booking Number"), max_length=120, default=generateBookingNumber)
    # TODO: change user model  to client model
    bookingby = models.ForeignKey(User, verbose_name=_("Client"), on_delete=models.CASCADE)
    bookingroom = models.ForeignKey(Room, verbose_name=_("Room"), on_delete=models.CASCADE)
    bookingfrom = models.DateTimeField(_("From"), default=timezone.now)
    bookingnights = models.PositiveIntegerField(_("Number of Nights"), default=1)
    bookingconfirm = models.BooleanField(_("Booking Confirmed"), null=True, blank=True)
    bookingis_valid = models.BooleanField(_("Is Valid"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    bookingcontent = models.TextField(_("Comment"), blank=True, null=True, help_text='Add any extra Information here')

    @property
    def bookingto(self):
        return self.bookingfrom + timedelta(days=self.bookingnights)

    @property
    def is_active(self):
        if timezone.now() >= self.bookingto:
            return False
        return True

    @property
    def release_room(self):
        pass

    class Meta:
        """Meta definition for Booking."""

        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        """Unicode representation of Booking."""
        return str(self.bookingfrom)

    def get_absolute_url(self):
        return reverse("booking_detail", kwargs={"pk": self.pk})

def booking_post_delete(sender, instance, *args, **kwargs):
    instance.bookingroom.roomstatus = 'dv'
    instance.bookingroom.is_available = True
    instance.bookingroom.save()

post_delete.connect(booking_post_delete, sender=Booking)

def booking_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.bookingroom.roomstatus = 'co'
        instance.bookingroom.is_available = False
        instance.bookingroom.save()

post_save.connect(booking_post_save, sender=Booking)
