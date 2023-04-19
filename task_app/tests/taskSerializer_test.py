from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from task_app.serializers import TaskSerializer

from .factories import (
    ProjectFactory,
    TaskFactory,
    TaskWithForeignFactory,
    UserFactory,
)


class TaskSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.task = TaskWithForeignFactory.create()

    def test_that_a_task_is_correctly_serialized(self):
        task = self.task
        serializer = TaskSerializer
        serialized_task = serializer(task).data

        assert serialized_task['id'] == str(task.id)
        assert serialized_task['title'] == task.title
        assert serialized_task['body'] == task.body
        assert serialized_task['due_date'] == task.due_date
        assert serialized_task['status'] == task.status
        assert serialized_task['creation'] == task.creation
        assert serialized_task['priority'] == task.priority
        assert serialized_task['story_point'] == task.story_point

        assert len(serialized_task['subtasks']) == task.subtasks.count()
