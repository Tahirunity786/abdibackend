from django.core.mail import send_mail
from django.conf import settings

def a_to_u(subject, message, user):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST, 
            [user.email], 
            fail_silently=False,
        )
        return True  # Email sent successfully
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False  # Email sending failed