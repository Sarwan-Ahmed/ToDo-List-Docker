from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from accounts.models import User



class TestSetUp(APITestCase):

    def setUp(self):
        # Accounts urls
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.resendLink_url = reverse('resend-link')

        # Api urls
        self.task_create_url = reverse('task-create')
        self.task_list_url = reverse('task-list')
        self.total_tasks_report_url = reverse('total-tasks')
        self.average_completed_report_url = reverse('average-completed')
        self.overdue_tasks_report_url = reverse('overdue-tasks')
        self.max_date_report_url = reverse('max-date')
        self.count_opened_report_url = reverse('count-opened')
        self.similar_tasks_url = reverse('similar-tasks')

        self.fake = Faker()
        self.email = self.fake.email()

        self.user_register_data = {
            'email': self.email,
            'username': self.email.split('@')[0],
            'password': self.email,
        }

        self.user_login_data = {
            'username': self.email,
            'password': self.email,
        }

        self.user_email = {'email': self.email
        }

        self.attachment = open('media_cdn/emumba logo.jpg', 'rb')
        self.task_data = {
                'title': 'abc',
                'description': 'hello',
                'dueDate': '2021-08-8 12:23:28',
                'attachment': self.attachment,
                'completionDate': '2021-08-7 12:23:28',
                'completionStatus': True
        }

        self.attachment2 = open('media_cdn/emumba logo.jpg', 'rb')
        self.task_data2 = {
                'title': 'new title',
                'description': '',
                'dueDate': '2021-08-8 12:23:28',
                'attachment': self.attachment2,
                'completionDate': '2021-08-8 14:23:28',
                'completionStatus': False
        }

        self.attachment3 = open('media_cdn/emumba logo.jpg', 'rb')
        self.task_update_data = {
                'title': 'new title',
                'description': 'new description',
                'dueDate': '2021-08-9 12:23:28',
                'attachment': self.attachment3,
                'completionStatus': False
        }

        return super().setUp()


    def create_test_user(self):
            user = User.objects.create_user(username=self.email.split('@')[0], email=self.email)
            user.set_password(self.email)
            user.email_verified = True
            user.save()
            return user

    def tearDown(self):
        return super().tearDown()
