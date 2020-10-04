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
    title = models.CharField(max_length=150) # *
    description = models.TextField() # *
    created = models.DateField(auto_now_add=True) # *
    updated = models.DateField(auto_now=True)
    status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, default='new') # *
    completion = models.DateTimeField(editable=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = str(self.id)
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

