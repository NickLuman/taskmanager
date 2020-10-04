from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created', 'status')
    list_filter = ('status', 'created', 'user')
    search_fields = ('title', 'desciption')
    date_hierarchy = 'created'
    ordering = ('status', 'created')