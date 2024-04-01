from django.urls import path
from core_admin.views import admin_index, admin_appointments, admin_doctors, admin_userprofile
urlpatterns = [
    path("dashboard", admin_index, name="dashboard"),
    path("appointment", admin_appointments, name="Appointment"),
    path("doctors", admin_doctors, name="doctors"),
    path("profile", admin_userprofile, name="profile"),
]
