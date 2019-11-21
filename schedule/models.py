from django.db import models
from django.contrib.auth.models import User


choices = (('pending', 'pending'), ('completed',
                                    'completed'), ('failed', 'failed'))
# Create your models here.


class Project(models.Model):
    """Project Tables"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    client = models.CharField(max_length=100)


class Section(models.Model):
    """Sections table"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Tasks(models.Model):
    """Tasks table"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=choices)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
