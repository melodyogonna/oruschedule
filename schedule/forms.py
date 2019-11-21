from django.forms import ModelForm
from .models import Project, Section, Tasks


class ProjectForm(ModelForm):
    """Create a form  to handle projects"""
    class Meta:
        model = Project
        fields = ['name', 'description', 'client']


class SectionForm(ModelForm):
    """Create a form to handle section"""
    class Meta:
        model = Section
        fields = ['name', 'description', 'project']


class TasksForm(ModelForm):
    """Create a form to handle tasks"""
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'status', 'start_date', 'end_date', 'section']
