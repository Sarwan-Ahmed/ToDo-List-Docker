"""Register api models here."""

from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Register task model to display columns in database."""

    list_display = ['user', 'title', 'description',	'attachment', 'creationDate',
					'dueDate', 'completionDate', 'completionStatus']

#admin.site.register(Task)
