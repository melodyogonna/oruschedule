from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import ProjectForm, SectionForm, TasksForm
from .models import Project, Section, Tasks

# Create your views here.

# Handling projects


def projects(request):
    allprojects = Project.objects.all()
    return HttpResponse(allprojects)


def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return HttpResponse(project)


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        # Check that submitted form is valid
        if form.is_valid():
            return HttpResponse('thanks')
    else:
        form = ProjectForm()
    return HttpResponse(form.as_p())

# Handling Sections


def sections(request):
    allsection = Section.objects.all()
    return HttpResponse(allsection)


def create_sections(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)

        # Check that submitted form is valid
        if form.is_valid():
            return HttpResponse('thanks')
    else:
        form = SectionForm()
    return HttpResponse(form.as_p())


def tasks(request):
    alltask = Tasks.objects.all()
    return HttpResponse(alltask)


def create_tasks(request):
    if request.method == 'POST':
        form = TasksForm(request.POST)

    # Check that submitted form is valid
    if form.is_valid():
        return HttpResponse('thanks')
    else:
        form = TasksForm()
    return HttpResponse(form.as_p())
