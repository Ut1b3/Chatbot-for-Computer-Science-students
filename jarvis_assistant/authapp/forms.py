from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Reminder, SavedReminder, Feedback
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    matric_number = forms.CharField(max_length=20, required=True)
    reg_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'matric_number', 'reg_number', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'matric_number', 'reg_number', 'password')

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['course_code', 'description', 'due_date', 'due_time']

class SavedReminderForm(forms.ModelForm):
    class Meta:
        model = SavedReminder
        fields = ['text', 'due_date', 'due_time']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Enter your feedback here...'}),
        }