from django.contrib import admin
# 👇 1. Add this line import notification model
from .models import Notification, Beds, Bed_Reservation

# 👇 2. Add this line to add the notification
admin.site.register(Notification)
admin.site.register(Beds)
admin.site.register(Bed_Reservation)