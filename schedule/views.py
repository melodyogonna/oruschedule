from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from .forms import ProjectForm, SectionForm, TasksForm, InviteuserForm, Commentform
from .models import Project, Section, Tasks, Admin_permission, CustomUser, Invitedusers
from .forms import CustomeUserCreationForm
from .utils import account_activation_token

# Create your views here.

# Handling projects

@login_required
def dashboard(request):
    print(get_current_site(request).domain)
    return render(request, 'schedule/dashboard.html')

@login_required
def projects(request):
    user = request.user
    if user.has_perm('schedule.full_permission'):
        allprojects = Project.objects.all()
    else:
        allprojects = Project.objects.filter(section__users__id__exact=user.id)
    context = {'projects': allprojects}
    return render(request, 'schedule/projects.html', context)

@login_required
def project(request, project_id):
    theproject = get_object_or_404(Project, pk=project_id)
    context = {'project': theproject}
    return render(request, 'schedule/project.html', context)

@login_required
@permission_required('schedule.full_permission', raise_exception=True)
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        # Check that submitted form is valid
        if form.is_valid():
            form.save()
            print(form.instance.id)
            return redirect('schedule:project', form.instance.id)
    else:
        form = ProjectForm()
    context = {'form': form}
    return render(request, 'schedule/create_project.html', context)



# Handling Sections
@login_required
def section(request, section_id):
    thesection = get_object_or_404(Section, pk=section_id)
    members = CustomUser.objects.filter()
    context = {'section': thesection}
    return render(request, 'schedule/section.html', context)

@login_required
@permission_required('schedule.full_permission', raise_exception=True)
def create_section(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = SectionForm(request.POST)

        # Check that submitted form is valid
        if form.is_valid():
            form.instance.project = Project.objects.get(pk=project_id)
            form.save()
            return redirect('schedule:section', form.instance.id)
    else:
        form = SectionForm()
    context = {'form': form, 'project': project}
    return render(request, 'schedule/create_section.html', context)

@login_required
def tasks(request):
    alltask = Tasks.objects.all()
    return HttpResponse(alltask)

    
@login_required
def task(request, task_id):
    thetask = get_object_or_404(Tasks, pk=task_id)
    user = request.user
    if request.method == 'POST':
        try:
            # Check if the commenting user is assigned to the section this task belongs to
            user_in_section = thetask.section.users.get(id=user.id)
            comment = Commentform(request.POST)
            print(comment)
            context = {'task': thetask, 'form': comment}
            if comment.is_valid():
                print('mekid')
                comment.instance.author = user_in_section
                comment.instance.task = thetask
                comment.save()
        except (CustomUser.DoesNotExist):
            return HttpResponseForbidden('You cannot comment here')
    context = {'task': thetask, 'form': Commentform}
    return render(request, 'schedule/task.html', context)
            


@login_required
@permission_required('schedule.full_permission', raise_exception=True)
def create_task(request, section_id):
    if request.method == 'POST':
        form = TasksForm(request.POST)

    # Check that submitted form is valid
        if form.is_valid():
            form.instance.status  = 'p'
            form.instance.section = Section.objects.get(pk=section_id)
            form.save()
            return redirect('schedule:task', form.instance.id)
    else:
        form = TasksForm()
    

    task_section = get_object_or_404(Section, pk=section_id)
    context = {'form': form, 'section': task_section}
    return render(request, 'schedule/create_task.html', context)

@login_required
@permission_required('schedule.full_permission', raise_exception=True)
def members(request):
    if request.user.is_staff:
        members = CustomUser.objects.all()
    else:
        p = Permission.objects.get(codename='full_permission')
        members = CustomUser.objects.exclude(user_permissions.p).all
    return render(request, 'schedule/members.html', {'members': members})


@login_required
@permission_required('schedule.full_permission', raise_exception=True)
def delete_member(request):
    member_id = request.GET.get('id')
    user = get_object_or_404(CustomUser, pk=member_id)
    user.is_active = False
    user.save()
    return HttpResponse('changed')


@login_required
@permission_required('schedule.full_permission', raise_exception=True)
def assign_user(request):
    # Assign users a section. get their information from the url
    user = get_object_or_404(CustomUser, pk=request.GET.get('user_id'))
    section = get_object_or_404(Section, pk=request.GET.get('section'))

    # Make sure the user is not already in the section
    try:
        exist = section.users.get(pk=request.GET.get('user_id'))
        return JsonResponse({'status': 'error', 'message': 'user already exist'})
    except CustomUser.DoesNotExist:
        section.users.add(user)
        section.save()
        return JsonResponse({'status': 'success', 'message': 'user added'})
        

@login_required
@permission_required('schedule.full_permission', raise_exception=True)
def invite_user(request):
    if request.method == 'POST':
        form = InviteuserForm(request.POST)
        if form.is_valid():
            user = Invitedusers(email=form.cleaned_data.get('email'))
            user.save()
            message = render_to_string('schedule/verification_message.html', {
                'id': urlsafe_base64_encode(force_bytes(user.id)),
                'sitename': get_current_site(request).domain,
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Invitation to join OruSchedule'
            mail_from = 'admin@localhost.com'
            mail_to = (form.cleaned_data.get('email'),)
            try:
                send_mail(mail_subject, message, mail_from, mail_to, html_message=message)
                return HttpResponse('Invitation sent')
            except BadHeaderError:
                return HttpResponse('Bad header supplied')
    return render(request, 'schedule/inviteusers.html', {'form': InviteuserForm})


def verify_user(request, vid, token):
    try:
        uid = force_text(urlsafe_base64_decode(vid))
        user = Invitedusers.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Invitedusers.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()
        return HttpResponse('verified')
    else:
        return HttpResponse('invalid token')

class login(LoginView):
    template_name = 'auth/login.html'
        

class logout(LogoutView):
    template_name = 'auth/login.html'

class register(CreateView):
    form_class = CustomeUserCreationForm
    template_name = 'auth/register.html'
