from django.contrib import admin
from .models import Room, RoomExtra, RoomType#, RoomImage

# Register your models here.

admin.site.register(Room)
admin.site.register(RoomExtra)
admin.site.register(RoomType)
#admin.site.register(RoomImage)