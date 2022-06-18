from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room
from uuid import uuid4
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from number_generator import generate_number_with_date
from datetime import timedelta, datetime, date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete, pre_save
import pytz

def generateBookingNumber():
    # TODO: for every day, booking numbers must start
    bookings = Booking.objects.all().order_by('-created_at')
    return generate_number_with_date('B', bookings)

BOOKINGSTATUS = [
    ('Cancel', 'Cancelled'), 
    ('Checkedin', 'Checked In'),
    ('Unattended', 'Unattended'),
    ('Expired', '')
]

utc = pytz.UTC
def validate_bookingfrom(value):
    if value < utc.localize(datetime.now()):
        raise ValidationError(_('You are trying to book a room with a past date.'))

# Create your models here.
class Booking(models.Model):
    """Model definition for Booking."""
    # TODO: add validations for past dates
    bookingnumber = models.CharField(_("Booking Number"), max_length=120, default=generateBookingNumber)
    # TODO: change user model  to client model
    bookingby = models.ForeignKey(User, verbose_name=_("Client"), on_delete=models.CASCADE, default=get_user_model())
    bookingroom = models.ForeignKey(Room, verbose_name=_("Room"), on_delete=models.CASCADE)
    # TODO: auto up
    bookingstatus = models.CharField(_("Status"), max_length=50, choices=BOOKINGSTATUS, default='Unattended')
    bookingfrom = models.DateTimeField(_("From"), default=timezone.now, validators=[validate_bookingfrom])
    bookingnights = models.PositiveIntegerField(_("Number of Nights"), default=1)
    bookingto = models.DateTimeField(_("To"), blank=True)
    bookingconfirm = models.BooleanField(_("Booking Confirmed"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    bookingcontent = models.TextField(_("Comment"), blank=True, null=True, help_text='Add any extra Information here')

    @property
    def is_active(self):
        if timezone.now() >= self.bookingto:
            return False
        return True

    @property
    def is_valid(self):
        if all([self.bookingstatus=='Checkedin', self.bookingfrom <= self.bookingTo]):
            return True
        return False


    class Meta:
        """Meta definition for Booking."""

        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-bookingfrom', 'bookingconfirm']

    def __str__(self):
        """Unicode representation of Booking."""
        return f'{self.bookingroom, self.bookingconfirm, self.bookingfrom}'

    def get_absolute_url(self):
        return reverse("booking_detail", kwargs={"pk": self.pk})

def booking_post_delete(sender, instance, *args, **kwargs):
    instance.bookingroom.roomstatus = 'dv'
    instance.bookingroom.is_available = True
    instance.bookingroom.save()

post_delete.connect(booking_post_delete, sender=Booking)

def booking_pre_save(sender, instance, *args, **kwargs):
    if instance.bookingto is None:
        instance.bookingto = instance.bookingfrom + timedelta(days=instance.bookingnights)

pre_save.connect(booking_pre_save, sender=Booking)

def booking_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.bookingroom.roomstatus = 'co'
        instance.bookingroom.is_available = False
        instance.bookingroom.save()

post_save.connect(booking_post_save, sender=Booking)


class CheckIn(models.Model):
    """Model definition for CheckIn."""

    # TODO: Define fields here
    checkinbooking = models.ForeignKey(Booking, verbose_name=_("Booking"), on_delete=models.CASCADE)
    class Meta:
        """Meta definition for CheckIn."""

        verbose_name = 'CheckIn'
        verbose_name_plural = 'CheckIns'

    def __str__(self):
        """Unicode representation of CheckIn."""
        pass

def checkin_post_save(sender, instance, created, *args, **kwargs):
    if created:
        booking = instance.checkinbooking
        booking.bookingstatus = 'Checkedin'
        booking.save()

post_save.connect(checkin_post_save, sender=CheckIn)

