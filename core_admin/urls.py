from django.urls import path
from core_admin.views import admin_profile_update, del_user, bed_viewer, accept_bed_request,decline_bed_request, add_bed_post, del_bed, verify_doc, Register_Doctor, decline_contact, contact_sender, contact_viewer, add_bed, admin_index, admin_appointments, admin_doctors, admin_userprofile, admin_contacts, admin_user_management, admin_bed_reservations
urlpatterns = [
    path("dashboard", admin_index, name="dashboard"),
    path("appointment", admin_appointments, name="Appointment"),
    path("doctors", admin_doctors, name="doctors"),
    path("contacts", admin_contacts, name="contacts"),
    path("profile", admin_userprofile, name="profile"),
    path("user", admin_user_management, name="user"),
    path("user/del/<int:id>/", del_user, name="user"),
    path("beds", admin_bed_reservations, name="reservation"),
    path("add-beds", add_bed, name="beds"),
    path("add-beds-data", add_bed_post, name="addbeds"),
    path("del-beds/<int:id>/", del_bed, name="delbeds"),
    path("contact-viewer", contact_viewer, name="contact_viewer"),
    path("contact-sernder/<int:id>/", contact_sender, name="contact_sender"),
    path("contact-decline/<int:id>/", decline_contact, name="contact_decline"),
    path('admin/doctor/signup/<str:slug>/', Register_Doctor, name="REG-DOC" ),
    path('admin/doctor/verify/<int:id>/<str:acc_type>/', verify_doc, name="VERIFY-DOC" ),
    path("decline-reserve/<int:id>/", decline_bed_request, name="delinereserve"),
    path("accept-reserve/<int:id>/", accept_bed_request, name="acceptreserve"),
    path("bed-viewer/", bed_viewer, name="acceptreserve"),
    path("profile_updater/", admin_profile_update, name="proupdate"),
]
