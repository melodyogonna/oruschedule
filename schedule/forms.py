from django.forms import ModelForm
from django import forms
from .models import Project, Section, Tasks, Comment
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class ProjectForm(ModelForm):
    """Create a form  to handle projects"""
    class Meta:
        model = Project
        fields = ['name', 'description', 'client']


class SectionForm(ModelForm):
    """Create a form to handle section"""
    class Meta:
        model = Section
        fields = ['name', 'description']


class TasksForm(ModelForm):
    """Create a form to handle tasks"""
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'start_date', 'end_date',]

class Commentform(ModelForm):
    'Create a form to handle comments'

    class Meta:
        model = Comment
        fields = ['comment_body']

class InviteuserForm(forms.Form):
    email = forms.EmailField()

class CustomUserChangeForm(UserChangeForm):
    """Extend default form change"""
    class Meta:
        """Meta data for custom field"""
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomeUserCreationForm(UserCreationForm):
    """Extend default creation form"""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email']



class CustomeUserCreationFormInvite(UserCreationForm):
    """Extend default creation form"""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']