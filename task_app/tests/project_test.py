import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Project
from .factories import ProjectFactory, TaskFactory, UserFactory

faker = Factory.create()


class Project_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ProjectFactory.create_batch(size=3)
        self.creator = UserFactory.create()

    def test_create_project(self):
        """
        Ensure we can create a new project object.
        """
        client = self.api_client
        project_count = Project.objects.count()
        project_dict = factory.build(
            dict, FACTORY_CLASS=ProjectFactory, creator=self.creator.id)
        response = client.post(reverse('project-list'), project_dict)
        created_project_pk = response.data['project_name']
        assert response.status_code == status.HTTP_201_CREATED
        assert Project.objects.count() == project_count + 1
        project = Project.objects.get(pk=created_project_pk)

        assert project_dict['project_name'] == project.project_name
        assert project_dict['creation'] == project.creation.isoformat()

    def test_get_one(self):
        client = self.api_client
        project_pk = Project.objects.first().pk
        project_detail_url = reverse(
            'project-detail', kwargs={'pk': project_pk})
        response = client.get(project_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('project-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Project.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        project_qs = Project.objects.all()
        project_count = Project.objects.count()

        for i, project in enumerate(project_qs, start=1):
            response = client.delete(
                reverse('project-detail', kwargs={'pk': project.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert project_count - i == Project.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        project_pk = Project.objects.first().pk
        project_detail_url = reverse(
            'project-detail', kwargs={'pk': project_pk})
        project_dict = factory.build(
            dict, FACTORY_CLASS=ProjectFactory, creator=self.creator.id)
        project_dict.pop('project_name')
        response = client.patch(project_detail_url, data=project_dict)
        assert response.status_code == status.HTTP_200_OK

        assert project_pk == response.data['project_name']
        assert project_dict['creation'] == response.data['creation'].replace(
            'Z', '+00:00')

    def test_update_creation_with_incorrect_value_data_type(self):
        client = self.api_client
        project = Project.objects.first()
        project_detail_url = reverse(
            'project-detail', kwargs={'pk': project.pk})
        project_creation = project.creation
        data = {
            'creation': faker.pystr(),
        }
        response = client.patch(project_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert project_creation == Project.objects.first().creation

    def test_update_project_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        project = Project.objects.first()
        project_detail_url = reverse(
            'project-detail', kwargs={'pk': project.pk})
        project_project_name = project.project_name
        data = {
            'project_name': faker.pystr(min_chars=31, max_chars=31),
        }
        response = client.patch(project_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert project_project_name == Project.objects.first().project_name
