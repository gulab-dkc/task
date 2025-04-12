from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .manager import Manager


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




class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS = [
        ('in progress', 'IN PROGRESS'),
        ('completed', 'COMPLETED'),
        ('hold', 'HOLD'),
    ]

    task_name = models.TextField()
    assigned_to = models.ForeignKey(EmployeeSignUp, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    expected_end_date = models.DateTimeField()
    actual_end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='in progress')
    created_at = models.DateTimeField(default=timezone.now)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='Medium')

    def __str__(self):
        return self.task_name
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.task.task_name} by {self.created_at}"    


class FinishedTask(models.Model):
   
    description = models.TextField(null=True, blank=True)
    emp_name = models.ForeignKey(EmployeeSignUp, on_delete=models.CASCADE)
    finished_date = models.DateTimeField(default=timezone.now)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='finished_tasks')
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name.task_name

