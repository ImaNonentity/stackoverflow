from django.db import models
# from django.contrib.auth.models import User
from user_profile.models import User


class Message(models.Model):
    text = models.TextField(max_length=500)
    media_path = models.CharField(max_length=500, null=True, blank=True)
    sender_id = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"Message {self.id} ({self.sender_id} {self.text})"

    def __repr__(self):
        return f"Message {self.id} ({self.sender_id} {self.text})"


class Room(models.Model):
    receiver_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver_id")
    sender_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender_id")

    def __str__(self):
        return f"{self.id}"

    # def __str__(self):
    #     return f"Room {self.id} (RECEIVER-{self.receiver_id}, SENDER-{self.sender_id})"
