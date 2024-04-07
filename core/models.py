from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class Notification(models.Model):
    TYPE_CHOICES = (
        ('reservation', 'Reservation'),
        ('appointment_booking', 'Appointment Booking'),
        ('admin_notification', 'Admin Notification'),
    )
    message = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    def __str__(self):
        return self.message
    
class Beds(models.Model):
    ROOM_NO = (
        ("Room no 1", "Room no 1"),
        ("Room no 2", "Room no 2"),
        ("Room no 3", "Room no 3"),
        ("Room no 4", "Room no 4"),
        ("Room no 5", "Room no 5"),
    )
    room_no = models.CharField(max_length=50, choices=ROOM_NO, default="")
    bed_no = models.CharField(max_length=50, default="")
    description = models.TextField(db_index=True, default="")
    reservation = models.OneToOneField("Bed_Reservation", on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.bed_no


class Bed_Reservation(models.Model):
    STATUS_TYPE = (
        ("Reserve", "Reserve"),
        ("Pending", "Pending"),
        ("Available", "Available"),
        ("Decline", "Decline"),
    
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    bed = models.ForeignKey(Beds, on_delete=models.CASCADE, default="")
    tell_us_why = models.TextField(db_index=True, default="")
    status = models.CharField(max_length=100, choices=STATUS_TYPE, db_index=True)
    reservation_date = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reservation_date}"
    



class Appointment(models.Model):
    STATUS_TYPE = (
        ("Ok", "Ok"),
        ("Pending", "Pending"),
        ("Decline", "Decline"),
    
    )
    full_name = models.CharField(max_length=100, db_index=True, default="")
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, related_name="Patient", null=True)
    doctor_user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, related_name = "doctor")
    reason = models.TextField(db_index=True, default="")
    status = models.CharField(max_length=100, choices=STATUS_TYPE, db_index=True)
    phone_no = models.BigIntegerField(db_index=True)
    scheduled_day = models.DateField(db_index=True)


class Contact(models.Model):
    STATUS_TYPE = (
        ("Solved", "Solved"),
        ("Declined", "Declined"),
    
        ("Pending", "Pending"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    full_name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(db_index=True)
    phone_no = models.CharField(max_length=15, db_index=True)  # Changed to CharField to support leading zeros
    subject = models.CharField(max_length=100, db_index=True)
    message = models.TextField(db_index=True)
    status = models.CharField(max_length=100, choices=STATUS_TYPE, db_index=True)
    contact_ticket = models.CharField(max_length=16, db_index=True)
    solution = models.TextField(db_index=True,null=True)