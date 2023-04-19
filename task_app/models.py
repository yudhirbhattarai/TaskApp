import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Task(models.Model):
    TO_DO = 'TO_DO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    STATUS_CHOICES = [
        (TO_DO, 'TO_DO'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (DONE, 'DONE')
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=20)
    body = models.CharField(max_length=1000, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    creation = models.DateTimeField(null=True, blank=True, default=timezone.now)
    priority = models.IntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(5)], null=True, blank=True)
    story_point = models.FloatField(null=True, blank=True)
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='tasks')
    creator = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='created_tasks')
    assigned_primary = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='assigned_tasks_primary')
    assigned_secondary = models.ForeignKey(
        'User', on_delete=models.SET_NULL, related_name='assigned_tasks_secondary', null=True, blank=True)
    parent_task = models.ForeignKey(
        'Task', on_delete=models.SET_NULL, related_name='subtasks', null=True, blank=True)

    class Meta:
        db_table = "task"


class Project(models.Model):

    project_name = models.CharField(max_length=30, primary_key=True)
    creation = models.DateTimeField(null=True, blank=True, default=timezone.now)
    creator = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='created_projects')

    class Meta:
        db_table = "project"


class User(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        db_table = "user"


class Team(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(
        'User', related_name='member_of', db_table='team_members', blank=True)

    class Meta:
        db_table = "team"
