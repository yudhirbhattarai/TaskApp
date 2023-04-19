from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from task_app.serializers import TeamSerializer

from .factories import TeamFactory


class TeamSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.team = TeamFactory.create()

    def test_that_a_team_is_correctly_serialized(self):
        team = self.team
        serializer = TeamSerializer
        serialized_team = serializer(team).data

        assert serialized_team['id'] == str(team.id)
        assert serialized_team['name'] == team.name
