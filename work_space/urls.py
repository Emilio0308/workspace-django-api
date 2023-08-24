from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet, WorkSpaceViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename = 'userPath')
router.register(r'workspace/(?P<owner_id>\d+)', WorkSpaceViewSet, basename = 'workSpacePath')
router.register(r'tasks/(?P<owner_id>\d+)/workspace/(?P<workspace_id>\d+)', TaskViewSet, basename = 'taskPath')

urlpatterns = [
]
urlpatterns = urlpatterns + router.urls