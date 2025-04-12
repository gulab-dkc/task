from django.contrib import admin
from .models import EmployeeSignUp, Task, Comment, FinishedTask

@admin.register(EmployeeSignUp)
class EmployeeSignUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'assigned_to', 'status', 'priority', 'start_date', 'expected_end_date')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('task_name', 'assigned_to__name')
    date_hierarchy = 'start_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'created_at')
    search_fields = ('task__task_name', 'comment_text')
    list_filter = ('created_at',)


@admin.register(FinishedTask)
class FinishedTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'emp_name', 'finished_date', 'finished')
    list_filter = ('finished', 'finished_date')
    search_fields = ('task_name__task_name', 'emp_name__name')
