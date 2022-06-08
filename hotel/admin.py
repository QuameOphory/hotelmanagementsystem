from django.contrib import admin
from .models import Room, RoomExtra, RoomType

# Register your models here.

admin.site.register(Room)
admin.site.register(RoomExtra)
admin.site.register(RoomType)