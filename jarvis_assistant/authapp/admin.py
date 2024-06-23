from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Reminder, SavedReminder
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'matric_number', 'reg_number']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Reminder)
admin.site.register(SavedReminder)