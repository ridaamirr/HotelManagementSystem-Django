from django.contrib import admin

# Register your models here.

from .models import Menu

admin.site.register(Menu)

from .models import Customer

admin.site.register(Customer)

from .models import Hotel

admin.site.register(Hotel)

from .models import Room

admin.site.register(Room)

from .models import Roomtype

admin.site.register(Roomtype)

from .models import Salesandoffers

admin.site.register(Salesandoffers)

from .models import Booking

admin.site.register(Booking)

from .models import Billing

admin.site.register(Billing)
