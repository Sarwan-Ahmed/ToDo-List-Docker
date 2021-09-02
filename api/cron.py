"""Define cron jobs(Scheduled jobs)"""
from datetime import datetime
from django.core.mail import send_mail
from accounts.models import User
from .models import Task



def send_remainders():
    """Send mail remainders to users for tasks due today"""

    print('running cronjob')

    # get all the users
    users = User.objects.all()
    date_today = datetime.utcnow().date()

    # for each user fetch all the tasks
    for user in users:
        tasks = Task.objects.all().filter(user_id = user.pk)
        if len(tasks)==0:
            continue

        tasks_detail = []

        # for each task see if it's due today or not
        for task in tasks:
            if task.dueDate.date() == date_today:
                tasks_detail.append({'Title': task.title, 'Due': str(task.dueDate)})

        # if there is no task due today then continue to next user
        if len(tasks_detail)==0:
            continue

        # sending remainder of tasks due today to user through email
        message_content = ("Hello " + user.username + "\n\nYou have task(s) due today. "
                            "List of task(s) is appended below\n\n" + str(tasks_detail))
        message_subject = "[Remainder] Tasks Due Today"

        send_mail(subject=message_subject,
            message=message_content,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,)
