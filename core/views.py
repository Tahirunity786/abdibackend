from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required(login_url="/hospitrack/user/login")
def bed_reservation(request):

    return render(request, 'core/bed-reservation.html')

@login_required(login_url="/hospitrack/user/login")
def doctor_appointment(request):

    return render(request, 'core/doctor-appointment.html')

@login_required(login_url="/hospitrack/user/login")
def about_us(request):

    return render(request, 'core/about-us.html')

@login_required(login_url="/hospitrack/user/login")
def contact_us(request):

    return render(request, 'core/contact.html')

@login_required(login_url="/hospitrack/user/login")
def freq_ask_questions(request):

    return render(request, 'core/freq-q-ans.html')