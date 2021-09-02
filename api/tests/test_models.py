"""Module to define test cases for API models."""
from api.models import Task
from utils.setup_test import TestSetUp

class TestTaskModel(TestSetUp):
    """Testing task model."""

    def test_create_task(self):
        """Test case for tast creation."""

        user = self.create_test_user()
        todo_task = Task(user=user, title='Testing task', dueDate="2021-08-01 16:18:2")
        todo_task.save()
        self.assertEqual(str(todo_task), 'Testing task')
