from django.urls import path

from .views import create_project, projects, project, section, create_section, create_task, task, tasks, dashboard
from .views import assign_user, invite_user, verify_user
from .views import members, delete_member


app_name = 'schedule'

urlpatterns = [
    # Projects
    path('create_project/', create_project, name="create_project"),
    path('projects/', projects, name="projects"),
    path('project/<int:project_id>/', project, name="project"),

    # Sections
    path('section/<int:section_id>/', section, name="section"),
    path('create_section/<int:project_id>/', create_section, name='create_section'),

    # Assign a user to a section
    path('assign_user', assign_user, name='assign_user'),

    # Tasks
    path('task/<int:task_id>/', task, name='task'),
    path('tasks/', tasks, name='tasks'),
    path('create_task/<int:section_id>/', create_task, name='create_task'),

    # User dashboard
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),

    # Members
    path('members/', members, name='members'),
    path('delete_member/', delete_member, name='delete_member'),

    # User invitation
    path('invite_user/', invite_user, name='invite_user'),
    path('verify_user/<slug:vid>/<slug:token>/', verify_user, name='verify_user')
]
