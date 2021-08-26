from django.db import models

# Create your models here.

class ChatMessage(models.Model):
    sender = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='outbox')
    receiver = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='inbox')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)