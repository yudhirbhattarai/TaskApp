import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Task
from .factories import ProjectFactory, TaskFactory, UserFactory

faker = Factory.create()


class Task_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        TaskFactory.create_batch(size=3)
        self.project = ProjectFactory.create()
        self.creator = UserFactory.create()
        self.assigned_primary = UserFactory.create()
        self.assigned_secondary = UserFactory.create()
        self.parent_task = TaskFactory.create()

    def test_create_task(self):
        """
        Ensure we can create a new task object.
        """
        client = self.api_client
        task_count = Task.objects.count()
        task_dict = factory.build(dict, FACTORY_CLASS=TaskFactory, project=self.project.project_name, creator=self.creator.id,
                                  assigned_primary=self.assigned_primary.id, assigned_secondary=self.assigned_secondary.id, parent_task=self.parent_task.id)
        response = client.post(reverse('task-list'), task_dict)
        created_task_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == task_count + 1
        task = Task.objects.get(pk=created_task_pk)

        assert task_dict['title'] == task.title
        assert task_dict['body'] == task.body
        assert task_dict['due_date'] == str(task.due_date)
        assert task_dict['status'] == task.status
        assert task_dict['creation'] == task.creation.isoformat()
        assert task_dict['priority'] == task.priority
        assert task_dict['story_point'] == task.story_point

    def test_get_one(self):
        client = self.api_client
        task_pk = Task.objects.first().pk
        task_detail_url = reverse('task-detail', kwargs={'pk': task_pk})
        response = client.get(task_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('task-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Task.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        task_qs = Task.objects.all()
        task_count = Task.objects.count()

        for i, task in enumerate(task_qs, start=1):
            response = client.delete(
                reverse('task-detail', kwargs={'pk': task.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert task_count - i == Task.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        task_pk = Task.objects.first().pk
        task_detail_url = reverse('task-detail', kwargs={'pk': task_pk})
        task_dict = factory.build(dict, FACTORY_CLASS=TaskFactory, project=self.project.project_name, creator=self.creator.id,
                                  assigned_primary=self.assigned_primary.id, assigned_secondary=self.assigned_secondary.id, parent_task=self.parent_task.id)
        response = client.patch(task_detail_url, data=task_dict)
        assert response.status_code == status.HTTP_200_OK

        assert task_dict['title'] == response.data['title']
        assert task_dict['body'] == response.data['body']
        assert task_dict['due_date'] == response.data['due_date']
        assert task_dict['status'] == response.data['status']
        assert task_dict['creation'] == response.data['creation'].replace(
            'Z', '+00:00')
        assert task_dict['priority'] == response.data['priority']
        assert task_dict['story_point'] == response.data['story_point']

    def test_update_due_date_with_incorrect_value_data_type(self):
        client = self.api_client
        task = Task.objects.first()
        task_detail_url = reverse('task-detail', kwargs={'pk': task.pk})
        task_due_date = task.due_date
        data = {
            'due_date': faker.pystr(),
        }
        response = client.patch(task_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert task_due_date == Task.objects.first().due_date

    def test_update_creation_with_incorrect_value_data_type(self):
        client = self.api_client
        task = Task.objects.first()
        task_detail_url = reverse('task-detail', kwargs={'pk': task.pk})
        task_creation = task.creation
        data = {
            'creation': faker.pystr(),
        }
        response = client.patch(task_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert task_creation == Task.objects.first().creation

    def test_update_priority_with_incorrect_value_data_type(self):
        client = self.api_client
        task = Task.objects.first()
        task_detail_url = reverse('task-detail', kwargs={'pk': task.pk})
        task_priority = task.priority
        data = {
            'priority': faker.pystr(),
        }
        response = client.patch(task_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert task_priority == Task.objects.first().priority

    def test_update_story_point_with_incorrect_value_data_type(self):
        client = self.api_client
        task = Task.objects.first()
        task_detail_url = reverse('task-detail', kwargs={'pk': task.pk})
        task_story_point = task.story_point
        data = {
            'story_point': faker.pystr(),
        }
        response = client.patch(task_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert task_story_point == Task.objects.first().story_point

    def test_update_title_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        task = Task.objects.first()
        task_detail_url = reverse('task-detail', kwargs={'pk': task.pk})
        task_title = task.title
        data = {
            'title': faker.pystr(min_chars=21, max_chars=21),
        }
        response = client.patch(task_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert task_title == Task.objects.first().title

    def test_update_body_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        task = Task.objects.first()
        task_detail_url = reverse('task-detail', kwargs={'pk': task.pk})
        task_body = task.body
        data = {
            'body': faker.pystr(min_chars=1001, max_chars=1001),
        }
        response = client.patch(task_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert task_body == Task.objects.first().body

    def test_update_priority_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        task = Task.objects.first()
        task_detail_url = reverse('task-detail', kwargs={'pk': task.pk})
        task_priority = task.priority
        data = {
            'priority': faker.pyint(min_value=6),
        }
        response = client.patch(task_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert task_priority == Task.objects.first().priority
