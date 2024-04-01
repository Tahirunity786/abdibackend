from django.db import models
from django.contrib.auth import get_user_model

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
    

class Bed_Reservation(models.Model):
    STATUS_TYPE = (
        ("Reserve", "Reserve"),
        ("Available", "Available"),
    
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    reservation_date = models.DateField(db_index=True)
    de_reservation_date = models.DateField(db_index=True)
    status = models.CharField(max_length=100, choices=STATUS_TYPE, db_index=True)

    def __str__(self):
        return f"{self.user.username} - {self.reservation_date}"
    
class Rooms(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index=True)
    room_no = models.IntegerField(db_index=True)
    beds = models.ManyToManyField(Bed_Reservation, db_index=True)
    date_created = models.DateTimeField(auto_now_add = True)


class Appointment(models.Model):
    STATUS_TYPE = (
        ("Ok", "Ok"),
        ("Decline", "Decline"),
    
    )
    Departments = (
    ('emergency', 'Emergency Department'),
    ('internal_medicine', 'Internal Medicine'),
    ('surgery', 'Surgery'),
    ('obstetrics_gynecology', 'Obstetrics and Gynecology'),
    ('pediatrics', 'Pediatrics'),
    ('radiology', 'Radiology'),
    ('pathology', 'Pathology'),
    ('anesthesiology', 'Anesthesiology'),
    ('intensive_care', 'Intensive Care Unit (ICU)'),
    ('oncology', 'Oncology'),
    ('psychiatry', 'Psychiatry'),
    ('physical_therapy', 'Physical Therapy and Rehabilitation'),
    ('pharmacy', 'Pharmacy'),
    # Add more departments as needed
)

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, related_name="Patient", null=True)
    doctor_user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, related_name = "doctor")
    name = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=100, choices=STATUS_TYPE, db_index=True)
    departments = models.CharField(max_length=200, choices=Departments, db_index=True)
    phone_no = models.IntegerField(db_index=True)
    scheduled_day = models.DateField(db_index=True)


class Contact(models.Model):
    STATUS_TYPE = (
        ("Solved", "Solved"),
        ("Unsolved", "Unsolved"),
    
    )
    full_name = models.CharField(max_length=100, db_index = True)
    email = models.EmailField(db_index=True)
    phone_no = models.IntegerField(db_index=True)
    subject = models.CharField(max_length=100, db_index = True)

    message = models.TextField(db_index=True)

    status = models.CharField(max_length=100, choices=STATUS_TYPE, db_index=True)

    contact_ticket = models.CharField(max_length=100, db_index = True, default="")