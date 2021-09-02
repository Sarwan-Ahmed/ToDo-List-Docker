"""Module to create models for API."""
from django.db.models.signals import post_delete
from django.db import models
from django.dispatch import receiver
from accounts.models import User


def upload_location(instance, filename, **kwargs):
    """Specifying locations for each user to save their attachments."""

    file_path = 'attachments/{user_name}/{title}-{filename}'.format(
		user_name = str(instance.user.username), title = str(instance.title), filename = filename
		)
    return file_path


class Task(models.Model):
    """Model to define columns for todo tasks."""

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to=upload_location, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField()
    completionDate = models.DateTimeField(null=True, blank=True)
    completionStatus = models.BooleanField(default=False)

    def __str__(self):
        """Returns title of task when convert task object to string."""
        return self.title

    class Meta:
        ordering = ['completionStatus', 'dueDate']



@receiver(post_delete, sender=Task)
def submission_delete(instance, **kwargs):
    """Delete attachment when task is deleted"""

    instance.attachment.delete(False)
