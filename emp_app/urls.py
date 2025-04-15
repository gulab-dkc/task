from django.urls import path
from django.shortcuts import redirect
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', lambda request: redirect('employee_signin')),
    path('emp-login/', views.signin_view, name='employee_signin'),
    path('logout/', views.logout_view, name='logout'),
    path('locations/', views.location_crud_view, name='location_crud'),
    path('locations/<int:pk>/', views.location_crud_view, name='location_crud'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/update/status/', views.update_task_status, name='update_task_status'),
    path('task/<int:pk>/update/priority/', views.update_task_priority, name='update_task_priority'),
    path('task/<int:pk>/update/location/', views.update_task_location, name='update_task_location'),
    path('task/<int:pk>/update/task/', views.task_mark_complete, name='task_mark_complete'),
    path('update-description/<int:pk>/', views.update_task_description, name='update_task_description'),
    path('task/<int:pk>/update_end_date/', views.update_task_end_date, name='update_task_end_date'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
