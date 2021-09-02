"""Module to define serializers"""
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serialize task data"""

    class Meta:
        model = Task
        fields = "__all__"
