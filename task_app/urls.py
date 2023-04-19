from django.conf.urls import include, re_path
from drf_yasg import openapi
from django.urls import path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, TaskViewSet, TeamViewSet, UserViewSet


class OptionalSlashRouter(DefaultRouter):
    def __init__(self):
        super(DefaultRouter, self).__init__()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()

router.register(r'task', TaskViewSet, 'task')
router.register(r'project', ProjectViewSet, 'project')
router.register(r'user', UserViewSet, 'user')
router.register(r'team', TeamViewSet, 'team')

schema_view = get_schema_view(
    openapi.Info(
        title="task_app",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path('^', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
