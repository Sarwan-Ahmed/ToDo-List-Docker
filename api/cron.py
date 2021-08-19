from .models import Task
from accounts.models import User
from datetime import datetime
from django.core.mail import send_mail



def send_remainders():

    # get all the users
    print('running cronjob')
    
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
        messageContent = 'Hello '+user.username+"\n\nYou have task(s) due today. List of task(s) is appended below\n\n"+str(tasks_detail)
        messageSubject = '[Remainder] Tasks Due Today'

        send_mail(subject=messageSubject,
            message=messageContent,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,)