from django.urls import path, include
from .views import RoomListView, RoomCreateView, RoomDeleteView, RoomDetailView, RoomUpdateView

urlpatterns = [
    path('', RoomListView.as_view(), name='room_list'),
    path('add/', RoomCreateView.as_view(), name='room_create'),
    path('<slug>/booking/', include('reservation.urls')),
    path('<slug>/', RoomDetailView.as_view(), name='room_detail'),
    path('<slug>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('<slug>/edit/', RoomUpdateView.as_view(), name='room_update'),
]
