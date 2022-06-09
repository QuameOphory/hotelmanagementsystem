from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid
# from roomDefaults import generateRoomNumber

def generateRoomNumber():
    try:
        appendix = 'R000'
        rooms = Room.objects.all().count() + 1
        return appendix + str(rooms)
    except Exception as e:
        print(f'an error occured \n{e}')


# Create your models here.

class RoomExtra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roomextra_name = models.CharField(_("Name of Extra"), max_length=50)
    roomextra_cost = models.DecimalField(_("Cost"), max_digits=5, decimal_places=2)
    roomextra_info1 = models.CharField(_("Room Extra Info"), max_length=50, blank=True, null=True)
    roomextra_info2 = models.CharField(_("Room Extra Info 2"), max_length=50, blank=True, null=True)
    roomextra_date1 = models.DateTimeField(_("Room Extra Date 1"), auto_now=False, auto_now_add=False, blank=True, null=True)
    roomextra_date2 = models.DateTimeField(_("Room Extra Date 2"), auto_now=False, auto_now_add=False, blank=True, null=True)
    roomextra_active = models.BooleanField(_("Is Active?"), default=True)
    

    class Meta:
        verbose_name = _("RoomExtra")
        verbose_name_plural = _("RoomExtras")

    def __str__(self):
        return self.roomextra_name

    def get_absolute_url(self):
        return reverse("RoomExtra_detail", kwargs={"pk": self.pk})


class RoomType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roomtype_name = models.CharField(_("Name"), max_length=50)
    roomtype_cost = models.DecimalField(_("Cost of Room/Night"), max_digits=5, decimal_places=2)
    roomtype_cost1 = models.DecimalField(_("Cost of Room/Night 1"), max_digits=5, decimal_places=2, blank=True, null=True)
    roomtype_info = models.CharField(_("RoomType Info 1"), max_length=50, blank=True, null=True)
    roomtype_active = models.BooleanField(_("Is Active?"), default=True)


    class Meta:
        verbose_name = _("RoomType")
        verbose_name_plural = _("RoomTypes")

    def __str__(self):
        return self.roomtype_name

    def get_absolute_url(self):
        return reverse("RoomType_detail", kwargs={"pk": self.pk})

ROOMSTATUS = [
    ('cv', 'Clean Vacant'),
    ('co', 'Clean Occupied'),
    ('dv', 'Dirty Vacant'),
    ('do', 'Dirty Occupied'),
    ('un', 'Unavailable')
]


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roomstatus = models.CharField(_("Room Status"), max_length=2, choices=ROOMSTATUS, default='dv')
    roomnumber = models.CharField(_("Room Number"), max_length=50, default=generateRoomNumber, db_index=True, unique=True)
    #limit_choices_to limits the availabe choices for this field/Will show only roomtypes with roomtype_active = True
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE, limit_choices_to={'roomtype_active': True}, related_name='rooms') 
    roomcapacity = models.PositiveIntegerField(_("Room Capacity")) #todo: set max value for room capacity
    roombed = models.PositiveIntegerField(_("Number of Beds"))
    roombath = models.PositiveIntegerField(_("Number of Bath"))
    roomdimension = models.DecimalField(_("Dimension (in Square Feet)"), max_digits=5, decimal_places=2)
    roomextras = models.ManyToManyField(RoomExtra, verbose_name=_("List of Extra Items"))
    roomdate = models.DateTimeField(_("Created At"), blank=True, null=True)

    #todo: add a model manager to handle getting rooms according to status
    
    
    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return self.roomnumber

    def get_absolute_url(self):
        return reverse("room_detail", kwargs={"roomnumber": self.roomnumber})


class RoomImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, verbose_name=_("Room"), on_delete=models.CASCADE, related_name='images')
    roomimage_main = models.ImageField(_("Main Room Image"), upload_to='photos/%Y/%m/%d/', max_length=None)
    roomimage_1 = models.ImageField(_("Room Image 1"), upload_to='photos/%Y/%m/%d/', max_length=None, blank=True, null=True)
    roomimage_2 = models.ImageField(_("Room Image 2"), upload_to='photos/%Y/%m/%d/', max_length=None, blank=True, null=True)
    roomimage_3 = models.ImageField(_("Room Image 3"), upload_to='photos/%Y/%m/%d/', max_length=None, blank=True, null=True)
    roomimage_4 = models.ImageField(_("Room Image 4"), upload_to='photos/%Y/%m/%d/', max_length=None, blank=True, null=True)
    roomimage_5 = models.ImageField(_("Room Image 5"), upload_to='photos/%Y/%m/%d/', max_length=None, blank=True, null=True)
    

    class Meta:
        verbose_name = _("RoomImage")
        verbose_name_plural = _("RoomImages")

    def __str__(self):
        return self.room.roomnumber

    def get_absolute_url(self):
        return reverse("RoomImage_detail", kwargs={"pk": self.pk})


