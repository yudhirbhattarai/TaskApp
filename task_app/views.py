from rest_framework import viewsets

from .models import Project, Task, Team, User
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    TeamSerializer,
    UserSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []
    filterset_fields = ['id', 'title', 'body', 'due_date', 'status', 'creation',
                        'priority', 'story_point',
                        'subtasks', 'project', 'creator', 'assigned_primary',
                        'assigned_secondary', 'parent_task']


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_fields = ['project_name', 'creation', 'tasks', 'creator']
    permission_classes = []


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'username', 'first_name', 'last_name',
                        'created_tasks',
                        'assigned_tasks_primary', 'assigned_tasks_secondary',
                        'created_projects']
    permission_classes = []


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_fields = ['id', 'name']
    permission_classes = []
