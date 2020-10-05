from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
import re


class Task(models.Model):
    STATUS_CHOICES = (
        ('new', 'NEW'),
        ('planned', 'PLANNED'),
        ('in progress', 'IN PROGRESS'),
        ('done', 'DONE'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)  # *
    description = models.TextField()  # *
    created = models.DateTimeField(auto_now_add=True)  # *
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, default='new')  # *
    completion = models.DateTimeField(editable=True)

    def __str__(self):
        return self.title


class TaskChange(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    changed_title = models.CharField(max_length=305, default="No changes.")
    changed_description = models.TextField(default="No changes.")
    changed_status = models.CharField(max_length=35, default="No changes.")
    changed_completion = models.CharField(max_length=55, default="No changes.")
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} changed at {1}'.format(task.id, self.changed_at)
