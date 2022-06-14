from django.urls import path
from .views import BookingCreateView, BookingDetailView, BookingListView


urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'),
    path('<slug>/add/', BookingCreateView.as_view(), name='booking_create'),
    path('<pk>/', BookingDetailView.as_view(), name='booking_detail'),
]
