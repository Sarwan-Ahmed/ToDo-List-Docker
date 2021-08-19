from django.test.utils import override_settings
from utils.setup_test import TestSetUp
from accounts.models import User
from api.models import Task
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.conf import settings
import pdb


class TestTaskCreateView(TestSetUp):

	def test_task_create_without_token(self):
		res = self.client.post(self.task_create_url, self.task_data)
		self.assertEqual(res.status_code, 401)

	def test_task_create_with_invalid_token(self):
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_task_create_with_put_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.put(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_task_create_with_valid_data(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 201)

	def test_task_create_without_title(self):
		del self.task_data['title']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_create_without_description(self):
		del self.task_data['description']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 201)

	def test_task_create_without_dueDate(self):
		del self.task_data['dueDate']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_create_without_attachment(self):
		del self.task_data['attachment']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_create_without_completionDate(self):
		del self.task_data['completionDate']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 201)

	def test_task_create_without_compltionStatus(self):
		del self.task_data['completionStatus']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 201)

	def test_task_create_invalid_dueDate(self):
		self.task_data['dueDate'] = 'abcd'
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_create_invalid_completionDate(self):
		self.task_data['completionDate'] = 'abcd'
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_create_with_existing_title(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 409)


	def test_task_create_upto_fifty_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		
		for i in range(50):
			self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
			self.attachment = open('media_cdn/emumba logo.jpg', 'rb')
			self.task_data['title'] = str(i)
			self.task_data['attachment'] = self.attachment

		res = self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.queryset = Task.objects.filter(user_id=user.pk)
		self.assertEqual(len(self.queryset), 50)
		self.assertEqual(res.status_code, 403)
'''

'''
class TestTaskUpdateView(TestSetUp):

	def test_task_update_without_token(self):
		res = self.client.post('/api/task-update/title/', self.task_data)
		self.assertEqual(res.status_code, 401)

	def test_task_update_with_invalid_token(self):
		res = self.client.post('/api/task-update/title/', self.task_data, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_task_update_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post('/api/task-update/title/', self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_task_update_with_not_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.put('/api/task-update/title/', self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 404)

	def test_task_update_with_valid_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['title'], self.task_update_data['title'])
		self.assertEqual(res.status_code, 200)

	def test_task_update_with_existing_title(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 409)


	def test_task_update_without_title(self):
		del self.task_update_data['title']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_update_without_description(self):
		del self.task_update_data['description']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 200)

	def test_task_update_without_dueDate(self):
		del self.task_update_data['dueDate']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_update_without_attachment(self):
		del self.task_update_data['attachment']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_update_without_compltionStatus(self):
		del self.task_update_data['completionStatus']
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 200)

	def test_task_update_invalid_dueDate(self):
		self.task_update_data['dueDate'] = 'abcd'
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)

	def test_task_create_invalid_completionDate(self):
		self.task_update_data['completionDate'] = 'abcd'
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.put('/api/task-update/'+self.task_data['title']+'/', 
			self.task_update_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 400)
'''

'''
class TestTaskDeleteView(TestSetUp):

	def test_task_delete_without_token(self):
		res = self.client.post('/api/task-delete/title/')
		self.assertEqual(res.status_code, 401)

	def test_task_delete_with_invalid_token(self):
		res = self.client.post('/api/task-delete/title/', **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_task_delete_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post('/api/task-delete/title/', **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_task_delete_with_not_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.delete('/api/task-delete/title/', **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 404)

	def test_task_delete_with_valid_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.delete('/api/task-delete/'+self.task_data['title']+'/', **{'HTTP_AUTHORIZATION':'token '+token})
		queryset = Task.objects.filter(user_id=user.pk)
		self.assertEqual(len(queryset), 0)
		self.assertEqual(res.status_code, 200)

	def test_task_delete_with_deleted_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.delete('/api/task-delete/'+self.task_data['title']+'/', **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.delete('/api/task-delete/'+self.task_data['title']+'/', **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 404)
'''

'''
class TestTaskListView(TestSetUp):

	def test_task_list_without_token(self):
		res = self.client.get(self.task_list_url)
		self.assertEqual(res.status_code, 401)

	def test_task_list_with_invalid_token(self):
		res = self.client.get(self.task_list_url, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_task_list_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.task_list_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_task_list_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get(self.task_list_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 200)

	def test_task_list_with_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.task_list_url, **{'HTTP_AUTHORIZATION':'token '+token})
		queryset = Task.objects.filter(user_id=user.pk)
		self.assertEqual(len(queryset), 2)
		self.assertEqual(res.status_code, 200)
'''

'''
class TestTaskDetailView(TestSetUp):

	def test_task_detail_without_token(self):
		res = self.client.get('/api/task-detail/title/')
		self.assertEqual(res.status_code, 401)

	def test_task_detail_with_invalid_token(self):
		res = self.client.get('/api/task-detail/title/', **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_task_detail_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post('/api/task-detail/title/', **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_task_detail_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get('/api/task-detail/title/', **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 404)

	def test_task_detail_with_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get('/api/task-detail/'+self.task_data['title']+'/', **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['title'], self.task_data['title'])
		self.assertEqual(res.status_code, 200)
'''

'''
@override_settings(CACHES=settings.TEST_CACHES)
class TestTotalTasksView(TestSetUp):

	def test_total_tasks_report_without_token(self):
		res = self.client.get(self.total_tasks_report_url)
		self.assertEqual(res.status_code, 401)

	def test_total_tasks_report_with_invalid_token(self):
		res = self.client.get(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_total_tasks_report_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_total_tasks_report_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['Total Tasks'], 0)
		self.assertEqual(res.status_code, 201)

	def test_total_tasks_report_with_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.total_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['Total Tasks'], 2)
		self.assertEqual(res.status_code, 201)
'''

'''
@override_settings(CACHES=settings.TEST_CACHES)
class TestAverageCompletedView(TestSetUp):

	def test_average_completed_report_without_token(self):
		res = self.client.get(self.average_completed_report_url)
		self.assertEqual(res.status_code, 401)

	def test_average_completed_report_with_invalid_token(self):
		res = self.client.get(self.average_completed_report_url, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_average_completed_report_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.average_completed_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_average_completed_report_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get(self.average_completed_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['Average completed tasks'], '0/day')
		self.assertEqual(res.status_code, 201)

	def test_average_completed_report_with_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.average_completed_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['Average completed tasks'], '1/day')
		self.assertEqual(res.status_code, 201)
'''

'''
@override_settings(CACHES=settings.TEST_CACHES)
class TestOverdueTasksView(TestSetUp):

	def test_overdue_tasks_report_without_token(self):
		res = self.client.get(self.overdue_tasks_report_url)
		self.assertEqual(res.status_code, 401)

	def test_overdue_tasks_report_with_invalid_token(self):
		res = self.client.get(self.overdue_tasks_report_url, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_overdue_tasks_report_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.overdue_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_overdue_tasks_report_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get(self.overdue_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 201)

	def test_overdue_tasks_report_with_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.overdue_tasks_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['No. of tasks not completed on time'], '1')
		self.assertEqual(res.status_code, 201)
'''

'''
@override_settings(CACHES=settings.TEST_CACHES)
class TestMaxDateView(TestSetUp):

	def test_max_date_report_without_token(self):
		res = self.client.get(self.max_date_report_url)
		self.assertEqual(res.status_code, 401)

	def test_max_date_report_with_invalid_token(self):
		res = self.client.get(self.max_date_report_url, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_max_date_report_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.max_date_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_max_date_report_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get(self.max_date_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['Maximum tasks completed on'], None)
		self.assertEqual(res.status_code, 201)

	def test_max_date_report_with_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.max_date_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['No. of tasks'], '1')
		self.assertEqual(res.status_code, 201)
'''

'''
@override_settings(CACHES=settings.TEST_CACHES)
class TestCountOpenedView(TestSetUp):

	def test_count_opened_report_without_token(self):
		res = self.client.get(self.count_opened_report_url)
		self.assertEqual(res.status_code, 401)

	def test_count_opened_report_with_invalid_token(self):
		res = self.client.get(self.count_opened_report_url, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_count_opened_report_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.count_opened_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_count_opened_report_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get(self.count_opened_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['response'], None)
		self.assertEqual(res.status_code, 200)

	def test_count_opened_report_with_existing_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.count_opened_report_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 201)
'''

'''
class TestSimilarTasksViews(TestSetUp):

	def test_similar_tasks_without_token(self):
		res = self.client.get(self.similar_tasks_url)
		self.assertEqual(res.status_code, 401)

	def test_similar_tasks_with_invalid_token(self):
		res = self.client.get(self.similar_tasks_url, **{'HTTP_AUTHORIZATION':'token token'})
		self.assertEqual(res.status_code, 401)

	def test_similar_tasks_with_post_method(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.similar_tasks_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 405)

	def test_similar_tasks_with_not_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.get(self.similar_tasks_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 404)

	def test_similar_tasks_with_one_task(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.similar_tasks_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['response'], "Can't find similar tasks, only 1 task exists")
		self.assertEqual(res.status_code, 200)

	def test_similar_tasks_with_existing_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.similar_tasks_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.data['response'], "No any similar tasks found")
		self.assertEqual(res.status_code, 200)

	def test_similar_tasks_with_existing_similar_tasks(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.task_data['title'] = 'task'
		self.task_data2['title'] = 'new task'
		self.client.post(self.task_create_url, self.task_data, **{'HTTP_AUTHORIZATION':'token '+token})
		self.client.post(self.task_create_url, self.task_data2, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.get(self.similar_tasks_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 201)
