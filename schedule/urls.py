from django.urls import path
from .views import create_project, projects, project

app_name = 'schedule'

urlpatterns = [
    path('create_project/', create_project, name="createProject"),
    path('projects/', projects, name="projects"),
    path('project/<int:project_id>', project, name="project")
]
