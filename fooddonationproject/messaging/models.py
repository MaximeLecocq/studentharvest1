from django.db import models
from django.conf import settings
from listings.models import Listing

#this model represents a conversation between a student and a donor regarding a specific listing
class Conversation(models.Model):
    #ForeignKey linking to the student participating in the conversation
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_conversations', on_delete=models.CASCADE)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='donor_conversations', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='conversations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.student} and {self.donor} regarding {self.listing.title}"

#this model represents a message exchanged in a conversation between a student and a donor
class Message(models.Model):
    #ForeignKey linking the message to the conversation it belongs to
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"

