import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChannelsConsumer(AsyncWebsocketConsumer):

    group = 'test_group'

    async def connect(self):
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #await self.send(text_data=json.dumps({"message": message})) # echo
        await self.channel_layer.group_send(self.group, {'type': 'chatmessage', 'message': message})

    async def chatmessage(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
