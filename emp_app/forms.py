from django import forms
from .models import Task, EmployeeSignUp, FinishedTask, Comment, Locations

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'location', 'start_date', 'end_date', 'priority','description',]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expected_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'actual_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    location = forms.ModelChoiceField(queryset=Locations.objects.all(), required=False, empty_label="Select Location")
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = ['location_name']
        widgets = {
            'location_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type New Location Here...' ,
            }),
        }
        error_messages = {
            'location_name': {
                'required': 'Location name is required.'
            },
        }






