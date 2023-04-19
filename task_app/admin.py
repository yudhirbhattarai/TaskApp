from django.contrib import admin

from .models import Project, Task, Team, User

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(User)
admin.site.register(Team)
