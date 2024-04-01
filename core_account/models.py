from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from core_account.manager import CustomUserManager
# Create your models here.
class User(AbstractUser):
    SPECIALITY = (
    ('cardiology', 'Cardiology'),
    ('dermatology', 'Dermatology'),
    ('endocrinology', 'Endocrinology'),
    ('gastroenterology', 'Gastroenterology'),
    ('hematology', 'Hematology'),
    ('neurology', 'Neurology'),
    ('ophthalmology', 'Ophthalmology'),
    ('orthopedics', 'Orthopedics'),
    ('otolaryngology', 'Otolaryngology (ENT)'),
    ('pediatrics', 'Pediatrics'),
    ('pulmonology', 'Pulmonology'),
    ('urology', 'Urology'),
    # Add more specialties as needed
)
    ACCOUNT_TYPE = (
        ("Patient", "Patient"),
        ("Doctor", "Doctor"),
        ("Admin", "Admin"),
    )
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Not confirmed", "Not confirmed"),
    )
    account_type = models.CharField(max_length=100, choices=ACCOUNT_TYPE, null=True, db_index=True)
    username = models.CharField(max_length=100, null=True, db_index=True)
    profile = models.ImageField(upload_to="profile/images", blank=True, null=True)
    bio = models.TextField(null=True)
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(db_index=True, unique=True)
    date_of_birth = models.DateField(default=None, null=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, db_index=True)
    mobile_number = models.BigIntegerField(null=True)
    address = models.TextField(null=True)
    otp = models.PositiveIntegerField(null=True)
    otp_limit = models.IntegerField(null=True)
    otp_delay = models.TimeField(auto_now=True)
    last_login = models.DateTimeField(default=None, null=True)
    is_blocked = models.BooleanField(default=False, null=True)
    is_verified = models.BooleanField(default=False)
    
    # Doctor Profile
    doctor_cv = models.FileField( db_index=True, null=True)
    speciality = models.CharField(max_length=100,  choices=SPECIALITY, null=True, db_index=True)
    license_number = models.CharField(max_length=50, null=True)
    years_of_experience = models.PositiveIntegerField(null=True)
    education_background = models.TextField(null=True)
    certifications = models.TextField(null=True)


    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

class Special_code(models.Model):
    code = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code