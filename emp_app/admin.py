from django.contrib import admin
from .models import EmployeeSignUp, Task, Comment, FinishedTask,Locations

@admin.register(EmployeeSignUp)
class EmployeeSignUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'status', 'priority', 'start_date', 'end_date', 'location')
    list_filter = ('status', 'priority')
    search_fields = ('task_name', )
    date_hierarchy = 'start_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'comment_text','created_at')
    search_fields = ('task__task_name', 'comment_text')
    list_filter = ('created_at',)


@admin.register(FinishedTask)
class FinishedTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'emp_name', 'finished_date', 'finished')
    list_filter = ('finished', 'finished_date')
    search_fields = ('emp_name__name',)

@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_name', 'created_at')
    search_fields = ('location_name',)
    date_hierarchy = 'created_at'
