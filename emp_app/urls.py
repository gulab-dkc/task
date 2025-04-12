from django.urls import path
from django.shortcuts import redirect
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('task-list/', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('signup/', views.employee_signup, name='employee_signup'),
    path('ftask/<int:pk>', views.finished_task, name='finished_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('comments/', views.comment_list, name='comment_list'),
    path('completed-tasks/', views.completed_tasks, name='completed_tasks'),
    path('', lambda request: redirect('employee_signin')),
    path('emp-login/', views.signin_view, name='employee_signin'),
    path('logout/', views.logout_view, name='logout'),
    path('change-task-status/', views.change_task_status_modal, name='change_task_status_modal'),
    
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
