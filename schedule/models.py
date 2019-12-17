from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
import datetime

User = settings.AUTH_USER_MODEL

choices = (('p', 'pending'), ('c',
                                    'completed'))
# Create your models here.
class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
class Project(models.Model):
    """Project Tables"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    client = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Section(models.Model):
    """Sections table"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)    
        
    def __str__(self):
        return self.name
    


class Tasks(models.Model):
    """Tasks table"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=choices)
    start_date = models.DateField()
    end_date = models.DateField()
    completion_date = models.DateField(null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def due_for_reminder(self):
        datecalc = self.end_date - datetime.date.today()
        return  datecalc.days <= 1

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Store the comment information for tasks"""
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author')
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='task')
    comment_body = models.TextField()
    commented_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment on {self.task.name}'


class Invitedusers(models.Model):
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Admin_permission(models.Model):
    class Meta:
        managed = False

        permissions = [('full_permission', 'have full permission')]