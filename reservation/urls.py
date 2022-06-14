from django.urls import path
from .views import BookingCreateView, BookingDetailView, BookingListView, TodayBookingListView


urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'),
    path('today/', TodayBookingListView.as_view(), name='booking_today'),
    path('<slug>/add/', BookingCreateView.as_view(), name='booking_create'),
    path('<pk>/', BookingDetailView.as_view(), name='booking_detail'),
]
