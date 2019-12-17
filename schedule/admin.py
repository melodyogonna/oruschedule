from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomeUserCreationForm, CustomUserChangeForm
from .models import Project, Section, Tasks, CustomUser, Comment, Invitedusers

class CustomUserAdmin(UserAdmin):
    add_form = CustomeUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project)
admin.site.register(Section)
admin.site.register(Tasks)
admin.site.register(Comment)
admin.site.register(Invitedusers)