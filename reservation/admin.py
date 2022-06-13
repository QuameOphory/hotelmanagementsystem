from django.contrib import admin
from .models import Booking

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    '''Admin View for Booking'''

    list_display = ('bookingnumber', 'bookingby', 'bookingfrom', 'get_bookingto', 'is_active')
    list_filter = ('bookingby', 'bookingfrom',)
    search_fields = ('bookingnumber',)
    ordering = ('bookingfrom',)

    def get_bookingto(self, instance):
        bookingto = instance.bookingto
        return bookingto