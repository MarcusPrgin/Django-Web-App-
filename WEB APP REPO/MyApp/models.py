from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
  
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reminder_time = models.DateTimeField(null=True, blank=True)
    is_snoozed = models.BooleanField(default=False)
    snoozed_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title