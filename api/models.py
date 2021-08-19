from django.db.models.signals import post_delete
from django.db import models
from accounts.models import User
from django.dispatch import receiver

# Create your models here.

def upload_location(instance, filename, **kwargs):
	file_path = 'attachments/{user_name}/{title}-{filename}'.format(
		user_name = str(instance.user.username), title = str(instance.title), filename = filename
		)
	return file_path


# todo tasks model
class Task(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	attachment = models.FileField(upload_to=upload_location, null=True, blank=True)
	creationDate = models.DateTimeField(auto_now_add=True)
	dueDate = models.DateTimeField()
	completionDate = models.DateTimeField(null=True, blank=True)
	completionStatus = models.BooleanField(default=False)
	
	def __str__(self):
		return self.title

	class Meta:
		ordering = ['completionStatus', 'dueDate']



@receiver(post_delete, sender=Task)
def submission_delete(sender, instance, **kwargs):
	instance.attachment.delete(False)