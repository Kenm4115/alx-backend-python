import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ---------------------------------
# 1️⃣ Custom User model
# ---------------------------------
class User(AbstractUser):
    # Replace default id with UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # AbstractUser already has: username, password, first_name, last_name, email
    # We'll add phone_number and role as per specification
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(default=timezone.now)

    # Enforce unique email
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


# ---------------------------------
# 2️⃣ Conversation model
# ---------------------------------
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# ---------------------------------
# 3️⃣ Message model
# ---------------------------------
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"
