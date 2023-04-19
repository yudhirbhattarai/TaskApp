from rest_framework import serializers

from .models import Project, Task, Team, User


class TaskSerializer(serializers.ModelSerializer):
    subtasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    assigned_primary = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    assigned_secondary = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'body', 'due_date', 'status', 'creation', 'priority', 'story_point',
                  'subtasks', 'project', 'creator', 'assigned_primary', 'assigned_secondary', 'parent_task']


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Project
        fields = ['project_name', 'creation', 'tasks', 'creator']


class UserSerializer(serializers.ModelSerializer):
    created_tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    assigned_tasks_primary = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    assigned_tasks_secondary = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    created_projects = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Project.objects.all(),
        required=False
    )
    member_of = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'created_tasks',
                  'assigned_tasks_primary', 'assigned_tasks_secondary', 'created_projects', 'member_of']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'members']
