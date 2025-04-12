from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, EmployeeSignUpForm, FinishedTaskForm, CommentForm, LoginForm
from django.contrib import messages
from .models import Task, Comment, EmployeeSignUp, FinishedTask
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models.functions import TruncDate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import reverse_lazy

# This view is for creating a new task
@login_required(login_url='/emp-login/')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully.")
            return redirect('task_list')
        else:
            messages.error(request, "There were errors in your form.")
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


# This view is for displaying the list of tasks
@login_required(login_url='/emp-login/')
def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')

    task_name = request.GET.get('task_name')
    assigned_to = request.GET.get('assigned_to')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    start_date = request.GET.get('start_date')
    expected_end_date = request.GET.get('expected_end_date')

    if task_name:
        tasks = tasks.filter(task_name__icontains=task_name)
    if assigned_to:
        tasks = tasks.filter(assigned_to__name__icontains=assigned_to)
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if start_date:
        tasks = tasks.filter(start_date=start_date)
    if expected_end_date:
        tasks = tasks.filter(expected_end_date=expected_end_date)

    return render(request, 'task_list.html', {'tasks': tasks})


# This view is for signing up a new employee
def employee_signup(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            cleaned_data = form.cleaned_data
            password = cleaned_data.get('password')
            
            # Hash the password before saving it
            hashed_password = make_password(password)

            # Create the EmployeeSignUp object and save the hashed password
            employee_signup_instance = form.save(commit=False)
            employee_signup_instance.password = hashed_password  # Set the hashed password
            employee_signup_instance.save()

            messages.success(request, "User registered successfully.")
            return redirect('employee_signin')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeSignUpForm()

    return render(request, 'signup_form.html', {'form': form})

# This view is for marking a task as finished
@login_required(login_url='/emp-login/')
def finished_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    completed_task = task.finished_tasks.all().order_by('-id')
    if request.method == 'POST':
        form = FinishedTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.task = task
            new_task.finished = True
            try:
                user_id = request.session.get('user_id')
                user = EmployeeSignUp.objects.get(id=user_id)
                new_task.emp_name = user
                form.save()
                task.status = 'completed'
                task.actual_end_date = timezone.now()
                task.save()
                messages.success(request, "Task marked as completed.")
                return redirect('task_list')
            except EmployeeSignUp.DoesNotExist:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "There were errors in your form.")
    else:
        form = FinishedTaskForm()
    return render(request, 'finished_task_form.html', {'form': form, 'task': task})


# This view is for displaying the task details and comments
@login_required(login_url='/emp-login/')
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    comments = task.comments.all().order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.task = task
            new_comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('task_detail', pk=pk)
        else:
            messages.error(request, "There were errors in your comment.")
    else:
        comment_form = CommentForm()
    return render(request, 'task_detail.html', {
        'task': task,
        'comments': comments,
        'form': comment_form
    })


# This view is for displaying the dashboard with task counts and priorities
@login_required(login_url='/emp-login/')
def dashboard(request):
    task_counts = Task.objects.values('status').annotate(total=Count('status'))
    priorities = Task.objects.values('priority').annotate(total=Count('priority'))
    task_dates = Task.objects.annotate(date=TruncDate('created_at')).values('date').annotate(total=Count('id')).order_by('date')

    return render(request, 'dashboard.html', {
        'task_counts': task_counts,
        'priorities': priorities,
        'task_dates': task_dates
    })


# This view is for displaying the list of comments
@login_required(login_url='/emp-login/')
def comment_list(request):
    comments = Comment.objects.select_related('task').order_by('-created_at')

    # Filtering based on form input
    search_term = request.GET.get('search', '')
    comment_text = request.GET.get('comment_text', '')
    created_at = request.GET.get('created_at', '')

    if search_term:
        comments = comments.filter(task__task_name__icontains=search_term)
    
    if comment_text:
        comments = comments.filter(comment_text__icontains=comment_text)

    if created_at:
        comments = comments.filter(created_at__date=created_at)

    return render(request, 'comment_list.html', {'comments': comments})


# This view is for signing in the user
# It checks if the user is already logged in and redirects to the dashboard if so
def signin_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('dashboard')  # Use your named URL here
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, 'employee_signin.html', {'form': form})

# This view is for displaying the list of completed tasks
@login_required(login_url='/emp-login/')
def completed_tasks(request):
    tasks = FinishedTask.objects.filter(finished=True).select_related('task', 'emp_name').order_by('-finished_date')

    # Filtering based on form input
    search_term = request.GET.get('search', '')
    emp_name = request.GET.get('emp_name', '')
    description = request.GET.get('description', '')
    finished_date = request.GET.get('finished_date', '')

    if search_term:
        tasks = tasks.filter(task_name__icontains=search_term)
    
    if emp_name:
        tasks = tasks.filter(emp_name__name__icontains=emp_name)
    
    if description:
        tasks = tasks.filter(description__icontains=description)

    if finished_date:
        tasks = tasks.filter(finished_date=finished_date)

    return render(request, 'finished_tasks_list.html', {'tasks': tasks})


# This view is for logging out the user
@login_required(login_url='/emp-login/')
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('employee_signin')



# This view is for changing the status of a task using a modal
@login_required(login_url='/emp-login/')
@require_POST
def change_task_status_modal(request):
    task_id = request.POST.get('task_id')
    new_status = request.POST.get('status')
    if task_id and new_status in ['in progress', 'completed', 'hold']:
        try:
            task = Task.objects.get(pk=task_id)
            task.status = new_status
            task.save()
            messages.success(request, f"Task '{task.task_name}' status updated to '{new_status}'.")
        except Task.DoesNotExist:
            messages.error(request, "Task not found.")
    else:
        messages.error(request, "Invalid status or task ID.")
    return redirect('task_list')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/custom_password_reset.html'
    email_template_name = 'registration/custom_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/custom_password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/custom_password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/custom_password_reset_complete.html'
