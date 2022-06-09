from django.urls import path
from .views import RoomListView, RoomCreateView, RoomDetailView

urlpatterns = [
    path('', RoomListView.as_view(), name='room_home'),
    path('add/', RoomCreateView.as_view(), name='room_create'),
    path('<roomnumber>/', RoomDetailView.as_view(), name='room_detail'),
]
