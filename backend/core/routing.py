from django.urls import re_path
from . import consumers
import logging
logger = logging.getLogger(__name__)

websocket_urlpatterns = [
    re_path(r'ws/search/(?P<search_id>\w+)/$', consumers.SearchConsumer.as_asgi()),
]
print(websocket_urlpatterns)
logger.info('WebSocket URL patterns loaded')