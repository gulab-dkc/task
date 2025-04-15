from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, LoginForm, LocationForm
from django.contrib import messages
from .models import Task, Comment, EmployeeSignUp, FinishedTask, Locations
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models.functions import TruncDate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import reverse_lazy
from itertools import zip_longest


# This view is for displaying the task details and comments
@login_required(login_url='/emp-login/')
def add_comment(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        try:
            user = EmployeeSignUp.objects.get(id=request.user.id)
            Comment.objects.create(
                task=task,
                comment_by=user,
                comment_text=comment_text,
                created_at=timezone.now()
            )
            messages.success(request, "Comment added successfully.")
            return redirect('task_detail', pk=pk)

        except EmployeeSignUp.DoesNotExist:
            messages.error(request, "User not found.")

    latest_comment = Comment.objects.filter(task=task).order_by('-id').first()        
    print("latest_comment", latest_comment)
    return render(request, 'task_detail.html', {
        'task': task,
        'latest_comment': latest_comment,
    })

# Function to group locations into tuples of n
def group_locations(locations, n=3):
    args = [iter(locations)] * n
    return list(zip_longest(*args))


#dashboard views
@login_required(login_url='/emp-login/')
def dashboard(request):
    # selected_loc_id =None
    selected_status = request.GET.get('status', 'in progress')
    sort_by = request.GET.get('sort', 'location')
    loc_id = request.GET.get('loc_id')
    # print('loc_id',loc_id)
    try:
        selected_loc_id = int(loc_id)
    except (TypeError, ValueError):
        selected_loc_id = None

    # Handle form submissions
    if request.method == 'POST':
        if 'submit_task' in request.POST:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task_form.save()
                messages.success(request, "Task created successfully!")
                return redirect('dashboard')

        elif 'submit_location' in request.POST:
            location_form = LocationForm(request.POST)
            if location_form.is_valid():
                location_form.save()
                messages.success(request, "Location added successfully!")
                return redirect('dashboard')

    tasks = Task.objects.filter(status=selected_status)
    grouped_locations = None
    

    if loc_id:
        try:
            selected_location = Locations.objects.get(id=loc_id)
            tasks = tasks.filter(location=selected_location)
        except Locations.DoesNotExist:
            selected_location = None

    if sort_by == 'location':
        tasks = tasks.order_by('location__location_name', 'end_date')
        all_locations = Locations.objects.all()
        grouped_locations = group_locations(all_locations, 2)
    else:
        tasks = tasks.order_by('end_date')

    task_counts = Task.objects.values('status').annotate(total=Count('id'))
    print('selected_loc_id',loc_id)
    context = {
        'tasks': tasks,
        'selected_status': selected_status,
        'task_counts': task_counts,
        'form': TaskForm(),
        'location_form': LocationForm(),
        'active_sort': sort_by,
        'active_location': loc_id,
        'selected_loc_id': selected_loc_id,
    }

    if grouped_locations:
        context['locations_grouped'] = grouped_locations

    return render(request, 'dashboard.html', context)



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


# This view is for logging out the user
@login_required(login_url='/emp-login/')
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('employee_signin')


def location_crud_view(request, pk=None):
    if pk:
        location_instance = get_object_or_404(Locations, pk=pk)
    else:
        location_instance = None

    form = LocationForm(request.POST or None, instance=location_instance)
    locations = Locations.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if 'delete' in request.POST:
            location_instance.delete()
            messages.success(request, 'Location deleted successfully!')
            return redirect('location_crud')
        elif form.is_valid():
            form.save()
            messages.success(request, 'Location saved successfully!')
            return redirect('location_crud')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'add_location.html', {
        'form': form,
        'locations': locations,
        'edit_mode': bool(location_instance),
        'edit_id': location_instance.id if location_instance else None
    })


def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    locations = Locations.objects.all()
    latest_comment = Comment.objects.filter(task=task).order_by('-created_at').first()
    print("latest_comment", latest_comment)
    return render(request, 'task_detail.html', {'task': task, 'locations': locations,'latest_comment': latest_comment})


@require_POST
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = request.POST['status']
    task.save()
    return redirect('task_detail', pk=pk)


@require_POST
def update_task_priority(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.priority = request.POST['priority']
    task.save()
    return redirect('task_detail', pk=pk)


@require_POST
def update_task_location(request, pk):
    task = get_object_or_404(Task, pk=pk)
    location_id = request.POST.get('location')
    if location_id:
        task.location_id = location_id
        task.save()
    return redirect('task_detail', pk=pk)

@require_POST
def task_mark_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    description = request.POST.get('description', '')
    try:
        user = EmployeeSignUp.objects.get(id=request.user.id)
        # Create FinishedTask entry
        FinishedTask.objects.create(
            task=task,
            description=description,
            emp_name=user,
            finished=True,
            finished_date=timezone.now()
        )
       
        task.status = 'completed'
        task.actual_end_date = timezone.now()
        task.save()
        
        messages.success(request, "Task marked as completed.")
    except EmployeeSignUp.DoesNotExist:
        print("User not found")
        messages.error(request, "Logged-in user not found.")

    return redirect('task_detail', pk=pk)


@require_POST
def update_task_description(request, pk):
    task = get_object_or_404(Task, id=pk)
    description = request.POST.get('description')
    if description:
        task.description = description
        task.save()
        messages.success(request, "Description updated successfully.")
    else:
        messages.error(request, "Description cannot be empty.")
    return redirect('task_detail', pk=pk)

@require_POST
def update_task_end_date(request, pk):
    task = get_object_or_404(Task, id=pk)

    new_end_date = request.POST.get('end_date')
    if new_end_date:

        # Update the task's end date
        task.end_date = new_end_date
        task.save()
        messages.success(request, "Description updated successfully.")

        return redirect('task_detail',pk=pk) 
    else:
        messages.error(request, "Description cannot be empty.")
    return redirect('task_detail', pk=pk)
    
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
