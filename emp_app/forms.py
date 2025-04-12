from django import forms
from .models import Task, EmployeeSignUp, FinishedTask, Comment


class EmployeeSignUpForm(forms.ModelForm):
    class Meta:
        model = EmployeeSignUp
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'assigned_to', 'start_date', 'expected_end_date', 'priority']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'expected_end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class FinishedTaskForm(forms.ModelForm):
    class Meta:
        model = FinishedTask
        fields = ['description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write your comment...'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)





