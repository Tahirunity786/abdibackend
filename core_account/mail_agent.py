from django.core.mail import send_mail
from django.contrib.auth import get_user_model

def send_user_to_admin(subject, message, user):
    if subject and message and user:
        admin_emails = get_user_model().objects.filter(is_admin=True).values_list('email', flat=True)
        if admin_emails:
            try:
                for email in admin_emails:
                    send_mail(subject=subject, message=message, from_email=user.email, recipient_list=[email])
                # Optionally, you can return True or some success message if the emails are sent successfully
                return True
            except Exception as e:
                return f"An error occurred while sending emails: {e}"
        else:
            # Handle the case where there are no admin users
            return "No admin users found."
    else:
        # Handle the case where subject, message, or user is missing
        return "Subject, message, or user is missing."

def send_patient_to_doctor(subject, message, patient_user, doctor_user):
    if subject and message and patient_user and doctor_user:
        doctor_email = doctor_user.email
        if doctor_email:
            try:
                send_mail(subject=subject, message=message, from_email=patient_user.email, recipient_list=[doctor_email])
                # Optionally, you can return True or some success message if the email is sent successfully
                return True
            except Exception as e:
                return f"An error occurred while sending email: {e}"
        else:
            # Handle the case where doctor email is not found
            return "Doctor email not found."
    else:
        # Handle the case where subject, message, patient user, or doctor user is missing
        return "Subject, message, patient user, or doctor user is missing."