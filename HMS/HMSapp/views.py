from django.shortcuts import render
from .models import Booking
# Create your views here.

def display_table(request):
    bookings = Booking.objects.values('room', 'billing', 'currentdate', 'numberofdays', 'hasrated', 'isbooked')
    return render(request, 'table_template.html', {'bookings': bookings})
