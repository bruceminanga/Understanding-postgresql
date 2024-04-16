# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import calculate_price  # Import the function

class PriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        academic_level = data['academic_level']
        service_type = data['service_type']
        currency = data['currency']
        price = calculate_price(academic_level, service_type, currency)  # Use the function
        await self.send(text_data=json.dumps({'price': price}))
