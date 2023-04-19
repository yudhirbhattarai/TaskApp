from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from task_app.serializers import ProjectSerializer

from .factories import (
    ProjectFactory,
    ProjectWithForeignFactory,
    TaskFactory,
    UserFactory,
)


class ProjectSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.project = ProjectWithForeignFactory.create()

    def test_that_a_project_is_correctly_serialized(self):
        project = self.project
        serializer = ProjectSerializer
        serialized_project = serializer(project).data

        assert serialized_project['project_name'] == project.project_name
        assert serialized_project['creation'] == project.creation

        assert len(serialized_project['tasks']) == project.tasks.count()
