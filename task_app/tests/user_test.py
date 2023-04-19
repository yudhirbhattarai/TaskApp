import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import User
from .factories import ProjectFactory, TaskFactory, TeamFactory, UserFactory

faker = Factory.create()


class User_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        UserFactory.create_batch(size=3)

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        client = self.api_client
        user_count = User.objects.count()
        user_dict = factory.build(dict, FACTORY_CLASS=UserFactory)
        response = client.post(reverse('user-list'), user_dict)
        created_user_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == user_count + 1
        user = User.objects.get(pk=created_user_pk)

        assert user_dict['username'] == user.username
        assert user_dict['first_name'] == user.first_name
        assert user_dict['last_name'] == user.last_name

    def test_create_user_with_m2m_relations(self):
        client = self.api_client

        member_of = TeamFactory.create_batch(size=3)
        member_of_pks = [team.pk for team in member_of]

        user_dict = factory.build(
            dict, FACTORY_CLASS=UserFactory, member_of=member_of_pks)

        response = client.post(reverse('user-list'), user_dict)
        created_user_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.get(pk=created_user_pk)
        assert member_of[0].members.first().pk == user.pk
        assert user.member_of.count() == len(member_of)

    def test_get_one(self):
        client = self.api_client
        user_pk = User.objects.first().pk
        user_detail_url = reverse('user-detail', kwargs={'pk': user_pk})
        response = client.get(user_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('user-list'))
        assert response.status_code == status.HTTP_200_OK
        assert User.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        user_qs = User.objects.all()
        user_count = User.objects.count()

        for i, user in enumerate(user_qs, start=1):
            response = client.delete(
                reverse('user-detail', kwargs={'pk': user.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert user_count - i == User.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        user_pk = User.objects.first().pk
        user_detail_url = reverse('user-detail', kwargs={'pk': user_pk})
        user_dict = factory.build(dict, FACTORY_CLASS=UserFactory)
        response = client.patch(user_detail_url, data=user_dict)
        assert response.status_code == status.HTTP_200_OK

        assert user_dict['username'] == response.data['username']
        assert user_dict['first_name'] == response.data['first_name']
        assert user_dict['last_name'] == response.data['last_name']

    def test_update_username_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        user = User.objects.first()
        user_detail_url = reverse('user-detail', kwargs={'pk': user.pk})
        user_username = user.username
        data = {
            'username': faker.pystr(min_chars=81, max_chars=81),
        }
        response = client.patch(user_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_username == User.objects.first().username

    def test_update_first_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        user = User.objects.first()
        user_detail_url = reverse('user-detail', kwargs={'pk': user.pk})
        user_first_name = user.first_name
        data = {
            'first_name': faker.pystr(min_chars=81, max_chars=81),
        }
        response = client.patch(user_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_first_name == User.objects.first().first_name

    def test_update_last_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        user = User.objects.first()
        user_detail_url = reverse('user-detail', kwargs={'pk': user.pk})
        user_last_name = user.last_name
        data = {
            'last_name': faker.pystr(min_chars=81, max_chars=81),
        }
        response = client.patch(user_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_last_name == User.objects.first().last_name
