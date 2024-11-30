
from django.db import models
from django.utils import timezone
from staff_app.models import *
from django.utils.timezone import now

# class Conversation(models.Model):
#     """Model to store information about each chat conversation."""
#     user1 = models.ForeignKey(CoustomUser, related_name='conversation_user1', on_delete=models.CASCADE)
#     user2 = models.ForeignKey(CoustomUser, related_name='conversation_user2', on_delete=models.CASCADE)
#     started_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"Conversation between {self.user1} and {self.user2}"

# class Message(models.Model):
#     """Model to store each message in a conversation."""
#     conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
#     sender = models.ForeignKey(CoustomUser, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"Message from {self.sender} at {self.timestamp}"
class Message(models.Model):
    sender = models.ForeignKey(CoustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CoustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'

class Notification(models.Model):
    
    sender=models.ForeignKey(CoustomUser,on_delete=models.CASCADE,related_name="sent_notification")
    receiver=models.ForeignKey(CoustomUser,on_delete=models.CASCADE,related_name="received_notification")
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    content=models.TextField(blank=True)
    
    def __str__(self) :
        return f"{self.sender}-{self.receiver}-{self.is_read}-{self.created_at}"