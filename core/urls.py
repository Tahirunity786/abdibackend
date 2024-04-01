from django.urls import path
from core.views import bed_reservation, doctor_appointment, about_us, contact_us, freq_ask_questions
urlpatterns = [

    path('bed-reservation', bed_reservation, name="BEDRESERVATION" ),
    path('doctor-appointments', doctor_appointment, name="DOCTORAPPOINTMENTS" ),
    path('about-us', about_us, name="ABOUTUS" ),
    path('contact-us', contact_us, name="ABOUTUS" ),
    path('fqs-s', freq_ask_questions, name="FAQs" ),
]
