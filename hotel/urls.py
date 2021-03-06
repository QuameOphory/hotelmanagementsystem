from django.urls import path, include
from .views import RoomListView, RoomCreateView, RoomDeleteView, RoomDetailView, RoomUpdateView
from reservation.views import AvailableRoomsListView, SearchRoomListView
urlpatterns = [
    path("search/", SearchRoomListView.as_view(), name="room_search"),
    path('all/', RoomListView.as_view(), name='room_list'),
    path('available/', AvailableRoomsListView.as_view(), name='room_available'),
    path('add/', RoomCreateView.as_view(), name='room_create'),
    path('<slug>/booking/', include('reservation.urls')),
    path('<slug>/', RoomDetailView.as_view(), name='room_detail'),
    path('<slug>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('<slug>/edit/', RoomUpdateView.as_view(), name='room_update'),
]
