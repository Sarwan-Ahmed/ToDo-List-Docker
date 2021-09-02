"""Module to define test cases for API views."""
from django.test.utils import override_settings
from django.conf import settings
from api.models import Task
from utils.setup_test import TestSetUp



class TestTaskCreateView(TestSetUp):
    """Test cases for task create view"""

    def test_task_create_without_token(self):
        """User must athorize itself through it's unique token to create task"""
        res = self.client.post(self.task_create_url, self.task_data)
        self.assertEqual(res.status_code, 401)


    def test_task_create_with_invalid_token(self):
        """User must provide valid token to authorize itself."""
        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_task_create_with_put_method(self):
        """Request method must be POST for task creation"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.put(self.task_create_url, self.task_data,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 405)


    def test_task_create_with_valid_data(self):
        """Task will be created on valid data only"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 201)


    def test_task_create_without_title(self):
        """Task cannot be created without title"""
        del self.task_data['title']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_create_without_description(self):
        """Task can be created without description"""
        del self.task_data['description']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 201)


    def test_task_create_without_due_date(self):
        """Task cannot be created without due date"""
        del self.task_data['dueDate']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_create_without_attachment(self):
        """Task cannot be created without attachment"""
        del self.task_data['attachment']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_create_without_completion_date(self):
        """Task can be created without completion date"""
        del self.task_data['completionDate']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 201)


    def test_task_create_without_compltion_status(self):
        """Task can be created without completion status"""
        del self.task_data['completionStatus']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 201)


    def test_task_create_invalid_due_date(self):
        """Task cannot be created with invalid type or format of due date"""
        self.task_data['dueDate'] = 'abcd'
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_create_invalid_completion_date(self):
        """Task cannot be created with invalid type or format of completion date"""
        self.task_data['completionDate'] = 'abcd'
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_create_with_existing_title(self):
        """Task cannot be created with existing task title"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 409)


    def test_task_create_upto_fifty_tasks(self):
        """Tasks cannot exceed 50 per user"""
        user = self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        for i in range(50):
            self.client.post(self.task_create_url, self.task_data,
                             **{'HTTP_AUTHORIZATION':'token '+token})

            self.attachment = open('media_cdn/emumba logo.jpg', 'rb')
            self.task_data['title'] = str(i)
            self.task_data['attachment'] = self.attachment

        res = self.client.post(self.task_create_url, self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.queryset = Task.objects.filter(user_id=user.pk)
        self.assertEqual(len(self.queryset), 50)
        self.assertEqual(res.status_code, 403)



class TestTaskUpdateView(TestSetUp):
    """Test cases for Task update view"""

    def test_task_update_without_token(self):
        """User must provide it's unique token to update the task"""
        res = self.client.post('/api/task-update/title/', self.task_data)
        self.assertEqual(res.status_code, 401)


    def test_task_update_with_invalid_token(self):
        """User must provide valid token to update the task"""
        res = self.client.post('/api/task-update/title/', self.task_data,
                               **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_task_update_with_post_method(self):
        """Request method must be PUT to update the task"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post('/api/task-update/title/', self.task_data,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 405)


    def test_task_update_with_not_existing_task(self):
        """Task can only be updated if it exists"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.put('/api/task-update/title/', self.task_data,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 404)


    def test_task_update_with_valid_task(self):
        """Task can be updated if it exists and update data is valid"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['title'], self.task_update_data['title'])
        self.assertEqual(res.status_code, 200)


    def test_task_update_with_existing_title(self):
        """Task cannot be updated if title of update data already exists"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 409)


    def test_task_update_without_title(self):
        """Task cannot be updated if title is missing in update data"""
        del self.task_update_data['title']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_update_without_description(self):
        """Task can be updated if description is missin in updated data"""
        del self.task_update_data['description']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 200)


    def test_task_update_without_due_date(self):
        """Task cannot be updated if due date is missing in updated data"""
        del self.task_update_data['dueDate']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_update_without_attachment(self):
        """Task cannot be updated if attachment is missing in updated data"""
        del self.task_update_data['attachment']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_update_without_compltion_status(self):
        """Task can be updated if completion status is missing in updated data"""
        del self.task_update_data['completionStatus']
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 200)


    def test_task_update_invalid_due_date(self):
        """Task cannot be updated if due date type or format is invalid in update data"""
        self.task_update_data['dueDate'] = 'abcd'
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)


    def test_task_create_invalid_completion_date(self):
        """Task cannot be updated if competion date type or format is invalid in update data"""
        self.task_update_data['completionDate'] = 'abcd'
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.put('/api/task-update/'+self.task_data['title']+'/',
                              self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 400)




class TestTaskDeleteView(TestSetUp):
    """Test cases for task delete view"""


    def test_task_delete_without_token(self):
        """User must provide a unique token to delete the task"""
        res = self.client.post('/api/task-delete/title/')
        self.assertEqual(res.status_code, 401)


    def test_task_delete_with_invalid_token(self):
        """User must provide a valid token to delete the task"""
        res = self.client.post('/api/task-delete/title/',
                               **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_task_delete_with_post_method(self):
        """Request method must be DELETE to delete the task"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post('/api/task-delete/title/',
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 405)


    def test_task_delete_with_not_existing_task(self):
        """Task can only be deleted if it exists"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.delete('/api/task-delete/title/',
                                 **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 404)


    def test_task_delete_with_valid_task(self):
        """Task can only be deleted if it exists"""
        user = self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.delete('/api/task-delete/'+self.task_data['title']+'/',
                                 **{'HTTP_AUTHORIZATION':'token '+token})

        queryset = Task.objects.filter(user_id=user.pk)
        self.assertEqual(len(queryset), 0)
        self.assertEqual(res.status_code, 200)


    def test_task_delete_with_deleted_task(self):
        """Task cannot be deleted more than one time"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.delete('/api/task-delete/'+self.task_data['title']+'/',
                           **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.delete('/api/task-delete/'+self.task_data['title']+'/',
                                 **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 404)



class TestTaskListView(TestSetUp):
    """Test cases for task listing view"""

    def test_task_list_without_token(self):
        """User must provide it's unique token to list it's tasks"""
        res = self.client.get(self.task_list_url)
        self.assertEqual(res.status_code, 401)


    def test_task_list_with_invalid_token(self):
        """User must provide a valid token to list it's tasks"""
        res = self.client.get(self.task_list_url, **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_task_list_with_post_method(self):
        """Request method must be GET to list the tasks"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.post(self.task_list_url, **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 405)


    def test_task_list_with_not_existing_tasks(self):
        """Return empty list if tasks does not exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.get(self.task_list_url, **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 200)


    def test_task_list_with_existing_tasks(self):
        """Return list of task(s) if there exists any"""
        user = self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.task_list_url, **{'HTTP_AUTHORIZATION':'token '+token})
        queryset = Task.objects.filter(user_id=user.pk)
        self.assertEqual(len(queryset), 2)
        self.assertEqual(res.status_code, 200)



class TestTaskDetailView(TestSetUp):
    """Test cases for task detail view"""

    def test_task_detail_without_token(self):
        """User must provide a unique token to list task details"""
        res = self.client.get('/api/task-detail/title/')
        self.assertEqual(res.status_code, 401)


    def test_task_detail_with_invalid_token(self):
        """User must provide a valid token to list task details"""
        res = self.client.get('/api/task-detail/title/', **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_task_detail_with_post_method(self):
        """Request method must be get to list task details"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.post('/api/task-detail/title/', **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 405)


    def test_task_detail_with_not_existing_tasks(self):
        """Task detail cannot be listed if the task does not exist"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.get('/api/task-detail/title/', **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 404)


    def test_task_detail_with_existing_task(self):
        """Task detail can only be listed if that task exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get('/api/task-detail/'+self.task_data['title']+'/',
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['title'], self.task_data['title'])
        self.assertEqual(res.status_code, 200)



@override_settings(CACHES=settings.TEST_CACHES)
class TestTotalTasksView(TestSetUp):
    """Test cases for total tasks view"""

    def test_total_tasks_report_without_token(self):
        """User must provide a unique token to access total tasks view"""
        res = self.client.get(self.total_tasks_report_url)
        self.assertEqual(res.status_code, 401)


    def test_total_tasks_report_with_invalid_token(self):
        """User must provide a valid token to access total tasks view"""
        res = self.client.get(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_total_tasks_report_with_post_method(self):
        """Request method must be GET to generate total tasks report"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.post(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 405)


    def test_total_tasks_report_with_not_existing_tasks(self):
        """Return empty report if tasks dows not exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.get(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.data['Total Tasks'], 0)
        self.assertEqual(res.status_code, 201)


    def test_total_tasks_report_with_existing_task(self):
        """Return total tasks report if there exists any task(s)"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.data['Total Tasks'], 2)
        self.assertEqual(res.status_code, 201)



@override_settings(CACHES=settings.TEST_CACHES)
class TestAverageCompletedView(TestSetUp):
    """Test cases for Average completed tasks view"""

    def test_average_completed_report_without_token(self):
        """User must provide a unique token to access average completed tasks report"""
        res = self.client.get(self.average_completed_report_url)
        self.assertEqual(res.status_code, 401)


    def test_average_completed_report_with_invalid_token(self):
        """User must provide a valid token to access average completed tasks report"""
        res = self.client.get(self.average_completed_report_url,
                              **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_average_completed_report_with_post_method(self):
        """Request method must be GET to generate average completed tasks report"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.post(self.average_completed_report_url,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 405)


    def test_average_completed_report_with_not_existing_tasks(self):
        """Return 0/day average if task(s) does not exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.get(self.average_completed_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['Average completed tasks'], '0/day')
        self.assertEqual(res.status_code, 201)


    def test_average_completed_report_with_existing_task(self):
        """Return average completed tasks report if task(s) exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.average_completed_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['Average completed tasks'], '1/day')
        self.assertEqual(res.status_code, 201)



@override_settings(CACHES=settings.TEST_CACHES)
class TestOverdueTasksView(TestSetUp):
    """Test cases for task overdue view"""

    def test_overdue_tasks_report_without_token(self):
        """User must provide a unique token to access overdue tasks view"""
        res = self.client.get(self.overdue_tasks_report_url)
        self.assertEqual(res.status_code, 401)


    def test_overdue_tasks_report_with_invalid_token(self):
        """User must provide a valid token to access overdue tasks view"""
        res = self.client.get(self.overdue_tasks_report_url,
                              **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_overdue_tasks_report_with_post_method(self):
        """Request method must be GET to generate the overdue tasks report"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.post(self.overdue_tasks_report_url,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 405)


    def test_overdue_tasks_report_with_not_existing_tasks(self):
        """Return 0 overdue tasks if task(s) does not exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.get(self.overdue_tasks_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 201)


    def test_overdue_tasks_report_with_existing_task(self):
        """Return overdue tasks report if task(s) exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.overdue_tasks_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['No. of tasks not completed on time'], '1')
        self.assertEqual(res.status_code, 201)



@override_settings(CACHES=settings.TEST_CACHES)
class TestMaxDateView(TestSetUp):
    """Test cases for max date view"""

    def test_max_date_report_without_token(self):
        """User must provide a unique token to access max date view"""
        res = self.client.get(self.max_date_report_url)
        self.assertEqual(res.status_code, 401)


    def test_max_date_report_with_invalid_token(self):
        """User must provide a valid token to access max date view"""
        res = self.client.get(self.max_date_report_url,
                              **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_max_date_report_with_post_method(self):
        """Request method must be Get to generate max date report"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.post(self.max_date_report_url,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 405)


    def test_max_date_report_with_not_existing_tasks(self):
        """Returns None if task(s) does not exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.get(self.max_date_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['Maximum tasks completed on'], None)
        self.assertEqual(res.status_code, 201)


    def test_max_date_report_with_existing_task(self):
        """Returns max date and no of tasks completed on that date"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})
        res = self.client.get(self.max_date_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['No. of tasks'], '1')
        self.assertEqual(res.status_code, 201)



@override_settings(CACHES=settings.TEST_CACHES)
class TestCountOpenedView(TestSetUp):
    """Test cases for count opened tasks view"""

    def test_count_opened_report_without_token(self):
        """User must provide a unique token to access count opened tasks view"""
        res = self.client.get(self.count_opened_report_url)
        self.assertEqual(res.status_code, 401)


    def test_count_opened_report_with_invalid_token(self):
        """User must provide a valid token to access count opened tasks view"""
        res = self.client.get(self.count_opened_report_url,
                              **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_count_opened_report_with_post_method(self):
        """Request method must be GET to generate count opened report"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.post(self.count_opened_report_url,
                               **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 405)


    def test_count_opened_report_with_not_existing_tasks(self):
        """Return None if task(s) does not exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        res = self.client.get(self.count_opened_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['response'], None)
        self.assertEqual(res.status_code, 200)


    def test_count_opened_report_with_existing_task(self):
        """Return count of tasks created on each weekday"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.count_opened_report_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 201)




class TestSimilarTasksViews(TestSetUp):
    """Test cases for similar tasks view"""

    def test_similar_tasks_without_token(self):
        """User must provide a unique token to access similar tasks view"""
        res = self.client.get(self.similar_tasks_url)
        self.assertEqual(res.status_code, 401)


    def test_similar_tasks_with_invalid_token(self):
        """User must provide a valid token to access similar tasks view"""
        res = self.client.get(self.similar_tasks_url,
                              **{'HTTP_AUTHORIZATION':'token token'})
        self.assertEqual(res.status_code, 401)


    def test_similar_tasks_with_post_method(self):
        """Request method must be GET to get similar tasks"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.post(self.similar_tasks_url,
                               **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 405)


    def test_similar_tasks_with_not_existing_tasks(self):
        """Return 404 if tasks does not exists"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        res = self.client.get(self.similar_tasks_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 404)


    def test_similar_tasks_with_one_task(self):
        """Cannot check similarity if there exists only one task"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.similar_tasks_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['response'], "Can't find similar tasks, only 1 task exists")
        self.assertEqual(res.status_code, 200)


    def test_similar_tasks_with_existing_tasks(self):
        """Return emplty list if there does not exists similar tasks"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.similar_tasks_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.data['response'], "No any similar tasks found")
        self.assertEqual(res.status_code, 200)


    def test_similar_tasks_with_existing_similar_tasks(self):
        """Return list of similar tasks"""
        self.create_test_user()
        token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
        self.task_data['title'] = 'task'
        self.task_data2['title'] = 'new task'

        self.client.post(self.task_create_url, self.task_data,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        self.client.post(self.task_create_url, self.task_data2,
                         **{'HTTP_AUTHORIZATION':'token '+token})

        res = self.client.get(self.similar_tasks_url,
                              **{'HTTP_AUTHORIZATION':'token '+token})

        self.assertEqual(res.status_code, 201)
