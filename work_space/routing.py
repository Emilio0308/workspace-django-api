from django.urls import re_path
from .consumers import ConsumerView

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<user_id>\d+)/(?P<workspace_id>\d+)', ConsumerView.as_asgi())
]