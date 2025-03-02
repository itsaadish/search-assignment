import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import SearchQuery

# Configure logging
logger = logging.getLogger(__name__)

class SearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.search_id = self.scope['url_route']['kwargs']['search_id']
        self.room_group_name = f'search_{self.search_id}'
        
        logger.info(f'WebSocket connecting: search_id={self.search_id}, channel_name={self.channel_name}')
        
        try:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f'WebSocket connection accepted: search_id={self.search_id}')
        except Exception as e:
            logger.error(f'Error during WebSocket connection: {e}')
            await self.close()

    async def disconnect(self, close_code):
        logger.info(f'WebSocket disconnecting: search_id={self.search_id}, close_code={close_code}')
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f'WebSocket disconnected: search_id={self.search_id}')
        except Exception as e:
            logger.error(f'Error during WebSocket disconnection: {e}')

    async def send_update(self, event):
        try:
            logger.info(f'Sending update: {event}')
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.error(f'Error sending WebSocket update: {e}')
