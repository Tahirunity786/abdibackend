from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/hospitrack/user/login")
def admin_index(request):
    return render(request, 'super_controller/index.html')

@login_required(login_url="/hospitrack/user/login")
def admin_appointments(request):
    return render(request, 'super_controller/Appointments.html')

@login_required(login_url="/hospitrack/user/login")
def admin_doctors(request):
    return render(request, 'super_controller/Doctors.html')

@login_required(login_url="/hospitrack/user/login")
def admin_userprofile(request):
    return render(request, 'super_controller/users-profile.html')