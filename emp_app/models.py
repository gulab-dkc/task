from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .manager import Manager
from simple_history.models import HistoricalRecords


class EmployeeSignUp(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = Manager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email


class Locations(models.Model):
    location_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.location_name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS = [
        ('in progress', 'IN PROGRESS'),
        ('completed', 'COMPLETED'),
    ]

    task_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='in progress')
    created_at = models.DateField(default=timezone.now)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    history = HistoricalRecords()

    def __str__(self):
        return self.task_name
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    comment_by = models.ForeignKey(EmployeeSignUp, on_delete=models.CASCADE, null=True, blank=True)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Comment on {self.task.task_name} by {self.created_at}"    


class FinishedTask(models.Model):
   
    description = models.TextField(null=True, blank=True)
    emp_name = models.ForeignKey(EmployeeSignUp, on_delete=models.CASCADE)
    finished_date = models.DateTimeField(default=timezone.now)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='finished_tasks')
    finished = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.task.task_name

