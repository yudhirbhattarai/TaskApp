# Generated by Django 3.2 on 2023-04-19 23:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('creation', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=80)),
                ('first_name', models.CharField(blank=True, max_length=80, null=True)),
                ('last_name', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('members', models.ManyToManyField(blank=True, db_table='team_members', related_name='member_of', to='task_app.User')),
            ],
            options={
                'db_table': 'team',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('body', models.CharField(blank=True, max_length=1000, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('TO_DO', 'TO_DO'), ('IN_PROGRESS', 'IN_PROGRESS'), ('DONE', 'DONE')], max_length=11)),
                ('creation', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('priority', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('story_point', models.FloatField(blank=True, null=True)),
                ('assigned_primary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks_primary', to='task_app.user')),
                ('assigned_secondary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks_secondary', to='task_app.user')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to='task_app.user')),
                ('parent_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subtasks', to='task_app.task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='task_app.project')),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to='task_app.user'),
        ),
    ]
