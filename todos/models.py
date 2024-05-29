from django.db import models
from django.contrib.auth.models import User

# added for Django channels -------------->
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# added for Django channels - ends here -------------->


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at",)


# Added for django channels-------------->
class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    notification = models.TextField(max_length=100)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # get all channels in the project.
        channel_layer = get_channel_layer()

        # create data to be sent from backend to frontend.
        notification_objs = Notification.objects.filter(is_seen=False).count()
        data = {
            "count": notification_objs,
            "current_notification": self.notification,
        }

        # creating the function to send data to the group.
        # Note: send notification will be defined in consumers.py
        async_to_sync(channel_layer.group_send)(
            "test_consumer_group",
            {"type": "send_notification", "value": json.dumps(data)},
        )
        return super(Notification, self).save(*args, **kwargs)
