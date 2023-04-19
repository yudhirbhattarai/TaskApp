import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Team
from .factories import TeamFactory, UserFactory

faker = Factory.create()


class Team_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        TeamFactory.create_batch(size=3)

    def test_create_team(self):
        """
        Ensure we can create a new team object.
        """
        client = self.api_client
        team_count = Team.objects.count()
        team_dict = factory.build(dict, FACTORY_CLASS=TeamFactory)
        response = client.post(reverse('team-list'), team_dict)
        created_team_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Team.objects.count() == team_count + 1
        team = Team.objects.get(pk=created_team_pk)

        assert team_dict['name'] == team.name

    def test_create_team_with_m2m_relations(self):
        client = self.api_client

        members = UserFactory.create_batch(size=3)
        members_pks = [user.pk for user in members]

        team_dict = factory.build(
            dict, FACTORY_CLASS=TeamFactory, members=members_pks)

        response = client.post(reverse('team-list'), team_dict)
        created_team_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED

        team = Team.objects.get(pk=created_team_pk)
        assert members[0].member_of.first().pk == team.pk
        assert team.members.count() == len(members)

    def test_get_one(self):
        client = self.api_client
        team_pk = Team.objects.first().pk
        team_detail_url = reverse('team-detail', kwargs={'pk': team_pk})
        response = client.get(team_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('team-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Team.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        team_qs = Team.objects.all()
        team_count = Team.objects.count()

        for i, team in enumerate(team_qs, start=1):
            response = client.delete(
                reverse('team-detail', kwargs={'pk': team.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert team_count - i == Team.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        team_pk = Team.objects.first().pk
        team_detail_url = reverse('team-detail', kwargs={'pk': team_pk})
        team_dict = factory.build(dict, FACTORY_CLASS=TeamFactory)
        response = client.patch(team_detail_url, data=team_dict)
        assert response.status_code == status.HTTP_200_OK

        assert team_dict['name'] == response.data['name']

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        team = Team.objects.first()
        team_detail_url = reverse('team-detail', kwargs={'pk': team.pk})
        team_name = team.name
        data = {
            'name': faker.pystr(min_chars=81, max_chars=81),
        }
        response = client.patch(team_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert team_name == Team.objects.first().name
