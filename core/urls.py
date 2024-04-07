from django.urls import path
from core.views import search_input_doctor, search_doctor, search_input_beds, search_beds, declined_appointment, accept_appointment, appointment_gainer, doc_user_info, appointment_agent, bed_reservation_agent, bed_viewer, bed_reservation, doctor_appointment, about_us, contact_us, freq_ask_questions
urlpatterns = [

    path('bed-reservation', bed_reservation, name="BEDRESERVATION" ),
    path('doctor-appointments', doctor_appointment, name="DOCTORAPPOINTMENTS" ),
    path('about-us', about_us, name="ABOUTUS" ),
    path('contact-us', contact_us, name="CONTACTUS" ),
    path('fqs-s', freq_ask_questions, name="FAQs" ),
    path('bed-viewer', bed_viewer, name="bedviewer" ),
    path('doctor-user', doc_user_info, name="doctoruser" ),
    path('appointment-gainer-user', appointment_gainer, name="appointmentgainer" ),
    path('appointment-accept/<int:id>/', accept_appointment, name="appointmentgainer" ),
    path('appointment-decline/<int:id>/', declined_appointment, name="appointmentgainer" ),
    path('bed-reservation-agent/<int:id>/',bed_reservation_agent,  name="bagent"),
    path('appointment-agent/<int:doc_id>/',appointment_agent,  name="appag"),
    path('search-bed/', search_beds, name="searchbed" ),
    path('search-bed-by-input/', search_input_beds, name="searchbedunput" ),
    path('search-doctor/', search_doctor, name="searchdoc" ),
    path('search-doctor-by-input/', search_input_doctor, name="searchdocinput" ),
]
