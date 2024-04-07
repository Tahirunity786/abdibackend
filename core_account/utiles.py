from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

def send_mail_to_admin(subject, message):
    try:
        # Filter admin users
        admins = User.objects.filter(account_type="Admin")
        
        # Extract email addresses from admin users
        admin_emails = [admin.email for admin in admins]

        # Send email to admin
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Sender's email address
            admin_emails,  # List of recipient email addresses
            fail_silently=False,
        )
        return True  # Email sent successfully
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False  # Email sending failed