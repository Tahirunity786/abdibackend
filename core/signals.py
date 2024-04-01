from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    print("Checking")
    if created:
        print("Checked")
        channel_layer = get_channel_layer()
        print(channel_layer)
        notification_type = instance.notification_type
        print(notification_type)
        if notification_type == 'reservation':
            # Send notification to admin
            async_to_sync(channel_layer.group_send)(
                'admin_notifications',  # Change to appropriate group name
                {
                    "type": "send_notification",
                    "message": instance.message
                }
            )
        elif notification_type == 'appointment_booking':
            # Send notification to doctor
            async_to_sync(channel_layer.group_send)(
                'doctor_notifications',  # Change to appropriate group name
                {
                    "type": "send_notification",
                    "message": instance.message
                }
            )
        elif notification_type == 'admin_notification':
            # Send notification to all users
            async_to_sync(channel_layer.group_send)(
                'public_room',
                {
                    "type": "send_notification",
                    "message": instance.message
                }
            )