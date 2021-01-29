import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from user.models import User


@database_sync_to_async
def check_exist_pending_room():

    print("--------------------------")
    print("check_exist_pending_room")
    print("--------------------------")
    
    if Room.objects.filter(status="pending").exists():
        print(Room.objects.filter(status="pending"))
        return True
    else:
        return False
    

@database_sync_to_async
def get_pending_room_id():
    
    print("--------------------------")
    print("get_pending_room_id")
    print("--------------------------")
    
    return Room.objects.filter(status="pending").values_list("id", flat=True).first()


@database_sync_to_async
def change_room_status_to_matched(room_id, participant):
    
    print("--------------------------")
    print("change_room_status_to_matched")
    print("--------------------------")
    
    Room.objects.filter(id=room_id).update(status="matched", participant=participant)
    

@database_sync_to_async
def change_room_status_to_closed(room_id):
    
    print("--------------------------")
    print("change_room_status_to_closed")
    print("--------------------------")
    
    Room.objects.filter(id=room_id).update(status="closed")
    
    
@database_sync_to_async
def create_pending_room(creater):
    
    print("--------------------------")
    print("create_pending_room")
    print("--------------------------")   
     
    room = Room.objects.create(status="pending", creater=creater)
    return room
    

@database_sync_to_async
def get_another_user_pk(room_id, sender_id):

    print("--------------------------")
    print("get_another_user_pk")
    print("--------------------------")   

    room = Room.objects.get(pk=room_id)
    
    if room.creater.id == int(sender_id):
        print("get_another_user_pk if")
        return room.participant.id
    else:
        print("get_another_user_pk else")
        return room.creater.id
    

@database_sync_to_async
def get_room_info(room_id):

    print("--------------------------")
    print("get_room_info")
    print("--------------------------")
    
    return Room.objects.get(pk=room_id)




class ChatConsumer(AsyncWebsocketConsumer):
    
    
    async def create_room(self, creater):
        
        print("--------------------------")
        print("create_room")
        print("--------------------------")
        
        
        new_room = await create_pending_room(creater)
        pending_room_id = new_room.id


        print("--------------------------")
        print("room created, room id: ", pending_room_id)
        print("--------------------------")

        self.room_id = pending_room_id
        self.room_group_name = 'chat_' + str(pending_room_id)
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        ) 
    
    
    async def join_room(self, room_id, participant):
        
        print("--------------------------")
        print("join_room")
        print("room joined, room id: ", room_id)
        print("--------------------------")
        
        pending_room_id = room_id
        await change_room_status_to_matched(pending_room_id, participant)
        
        self.room_id = pending_room_id
        self.room_group_name = 'chat_' + str(pending_room_id)
            
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_meesage',
                'sender_id' : "system",
                'message': "대화가 시작되었습니다.",
                'event_type' : 'start_chat'
            }
        )
        
    

    async def connect(self):
        
        is_exist_pending_room = await check_exist_pending_room()
        
        if is_exist_pending_room:
            
            pending_room_id = await get_pending_room_id()
            await self.join_room(pending_room_id, self.scope['user'])    
        else:
            await self.create_room(self.scope['user'])
            
        await self.accept()





    async def disconnect(self, close_code):
        # Leave room group
        
        
        print("--------------------------")
        print("DISCONNECT")
        print("--------------------------")
        
        await change_room_status_to_closed(self.room_id)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_meesage',
                'sender_id' : "system",
                'message': "상대방이 나갔습니다.",
                'event_type' : 'end_chat'
            }
        )
        
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        client_event = text_data_json['client_event']
        sender_id = text_data_json['sender_id']
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_meesage',
                'sender_id' : sender_id,
                'message': message,
                'event_type' : 'chat_message'
            }
        )

            




    # Receive message from room group
    async def send_meesage(self, event):
        message = event['message']
        sender_id = event['sender_id'] 
        server_event = event['event_type']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'server_event' : server_event,
            'message': message,
            'sender_id' : sender_id
        }))
