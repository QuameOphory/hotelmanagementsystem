from django.contrib import admin
from .models import Room, RoomExtra, RoomType, RoomImage

# Register your models here.

# admin.site.register(Room)
admin.site.register(RoomExtra)
admin.site.register(RoomType)
admin.site.register(RoomImage)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    '''Admin View for Room'''

    list_display = ('roomnumber', 'roomtype', 'roomcapacity', 'roomdimension', 'created_at', 'is_available', 'roomstatus')
    list_filter = ('roomnumber',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('roomnumber',)
    # date_hierarchy = ''
    ordering = ('roomnumber',)
    prepopulated_fields = {'roomnumber_url': ['roomnumber']}