from datetime import timedelta, timezone
from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from task_app.models import Project, Task, Team, User

faker = Factory.create()


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    project = factory.SubFactory('task_app.tests.factories.ProjectFactory')
    creator = factory.SubFactory('task_app.tests.factories.UserFactory')
    assigned_primary = factory.SubFactory(
        'task_app.tests.factories.UserFactory')
    title = LazyAttribute(lambda o: faker.text(max_nb_chars=20))
    body = LazyAttribute(lambda o: faker.text(max_nb_chars=1000))
    due_date = LazyFunction(faker.date)
    status = fuzzy.FuzzyChoice(Task.STATUS_CHOICES, getter=lambda c: c[0])
    creation = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())
    priority = LazyAttribute(lambda o: randint(1, 5))
    story_point = LazyAttribute(lambda o: uniform(0, 10000))


class TaskWithForeignFactory(TaskFactory):
    @factory.post_generation
    def subtasks(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TaskFactory(parent_task=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TaskFactory(parent_task=obj)


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project
        django_get_or_create = ('project_name',)

    creator = factory.SubFactory('task_app.tests.factories.UserFactory')
    project_name = LazyAttribute(
        lambda o: faker.text(max_nb_chars=30) .replace('.', ''))
    creation = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())


class ProjectWithForeignFactory(ProjectFactory):
    @factory.post_generation
    def tasks(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TaskFactory(project=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TaskFactory(project=obj)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = LazyAttribute(lambda o: faker.text(max_nb_chars=80))
    first_name = LazyAttribute(lambda o: faker.text(max_nb_chars=80))
    last_name = LazyAttribute(lambda o: faker.text(max_nb_chars=80))


class UserWithForeignFactory(UserFactory):
    @factory.post_generation
    def created_tasks(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TaskFactory(creator=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TaskFactory(creator=obj)

    @factory.post_generation
    def assigned_tasks_primary(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TaskFactory(assigned_primary=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TaskFactory(assigned_primary=obj)

    @factory.post_generation
    def assigned_tasks_secondary(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TaskFactory(assigned_secondary=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TaskFactory(assigned_secondary=obj)

    @factory.post_generation
    def created_projects(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ProjectFactory(creator=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                ProjectFactory(creator=obj)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=80))
