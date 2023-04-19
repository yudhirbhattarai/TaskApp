from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from task_app.serializers import UserSerializer

from .factories import (
    ProjectFactory,
    TaskFactory,
    UserFactory,
    UserWithForeignFactory,
)


class UserSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserWithForeignFactory.create()

    def test_that_a_user_is_correctly_serialized(self):
        user = self.user
        serializer = UserSerializer
        serialized_user = serializer(user).data

        assert serialized_user['id'] == str(user.id)
        assert serialized_user['username'] == user.username
        assert serialized_user['first_name'] == user.first_name
        assert serialized_user['last_name'] == user.last_name

        assert len(serialized_user['created_tasks']
                   ) == user.created_tasks.count()

        assert len(serialized_user['assigned_tasks_primary']
                   ) == user.assigned_tasks_primary.count()

        assert len(serialized_user['assigned_tasks_secondary']
                   ) == user.assigned_tasks_secondary.count()

        assert len(serialized_user['created_projects']
                   ) == user.created_projects.count()
