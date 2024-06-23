from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone   

class CustomUser(AbstractUser):
    matric_number = models.CharField(max_length=20, unique=True)
    reg_number = models.CharField(max_length=20, unique=True)

class Reminder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=10)
    description = models.TextField()
    due_date = models.DateField()
    due_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class SavedReminder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    due_date = models.DateField(default=timezone.now)
    due_time = models.TimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    
class ChatHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    length = models.IntegerField()
    history = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    feedback_text = models.TextField()

    def __str__(self):
        return self.feedback_text
