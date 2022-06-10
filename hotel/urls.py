from django.urls import path
from .views import RoomListView, RoomCreateView, RoomDetailView

urlpatterns = [
    path('', RoomListView.as_view(), name='room_list'),
    path('add/', RoomCreateView.as_view(), name='room_create'),
    path('<slug>/', RoomDetailView.as_view(), name='room_detail'),
]
