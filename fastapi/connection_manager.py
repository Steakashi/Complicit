import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from fastapi import (   
    Cookie,
    Depends,
    FastAPI,
    Request,
    Query,
    WebSocket
)
from uuid import uuid4
from loguru import logger
from copy import deepcopy 


from entities import Room, User
from services import rooms, users, send, connections, messages


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}
        self.rooms: list[Room] = []
        self.users: list[User] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        logger.debug(f"Connecting client with id {client_id}.")
        await websocket.accept()

        if not self.active_connections.get(client_id):
            logger.debug(f"Client with ID {client_id} has no active connection. Initializing list.")
            self.active_connections[client_id] = list()  
        
        self.active_connections[client_id].append(websocket)

        logger.info(f"Client with ID {client_id} has successfully connected.")
        logger.debug(f"Client with ID {client_id} has currently {len(self.active_connections[client_id])} active websockets.")

        user = users.get(self.users, client_id)
        if not user:
            user = User(
                client_id=client_id,
                user_name="user_name"
            )
            self.users.append(user)
            logger.debug(f"User with ID {client_id} has not been found et has been added to users list.")

        await send.to_client(
            active_connections=self.active_connections,
            client_id=client_id,
            message=messages.default(
                action="retrieve_user",
                client_id=client_id,
                user=user
            )
        )

        self._trigger_synchronization(client_id)
    
        return websocket

    async def disconnect(self, websocket: WebSocket, client_id: str):
        client_id = websocket.path_params['client_id']
        logger.debug(f"Disconnecting client with id {client_id}.")
        websockets_for_client = await connections.get_with(self.active_connections, client_id)
        
        if not websockets_for_client:
            logger.error(f"No active connection has been found for client with ID {client_id}. Abort process.")
            return
        
        if not websocket in websockets_for_client:
            logger.error(f"Can't find websocket {websocket} for client with ID {client_id}.")
            return
        
        
        websockets_for_client.remove(websocket)

        if len(websockets_for_client) <= 0:
            logger.info(f"Client with id {client_id} has been completely disconnected.")
        
        else:
            logger.info(
                f"Websocket {websocket} has been removed for client with id {client_id} "
                f"but still has {len(websockets_for_client)} active connection."
            )

        user = users.get(client_id)
        room = rooms.get_from_user(user)

        if room:
            rooms.remove_user(room, user)
            logger.info(f"User named {user.name} with id {user.id} has been removed from room named {room.name} due to disconnection.")
            await self._trigger_synchronization(client_id)


    async def synchronize(self, client_id, action):
        logger.debug(f"Synchronize order has been received from client with id {client_id}.")
        await send.to_all(
            active_connections=self.active_connections,
            message=messages.default(
                action=action,
                client_id=client_id,
                rooms=self.rooms,
                users=self.users
            )
        )

    async def _trigger_synchronization(self, client_id):
        await self.synchronize(client_id, "synchronize")

    async def update_user_name(self, client_id, action, user_name):
        logger.debug(f"Update user name order with value {user_name} has been received from client with id {client_id}.")
        concerned_user = users.get(client_id)
        if not concerned_user:
            logger.error(f"Can't find user with id {client_id}. Order has ben canceled.")
            await send.to_client(
                active_connections=self.active_connections,
                client_id=client_id,
                message=messages.error(
                    client_id=client_id,
                    error=f"Can't find client with id {client_id}."
                )
            )
            return

        users.update_name(concerned_user, user_name)

        await self._trigger_synchronization(client_id)
        await send.to_client(
            active_connections=self.active_connections,
            client_id=client_id,
            message=messages.default(
                action=action,
                client_id=client_id,
                user=concerned_user,
                success="Username has been correctly updated."
            )
        )

    async def create_room(self, client_id, action, room_name):
        logger.debug(f"New create room order with name {room_name} has been received from client with id {client_id}.")
        room = Room(
            room_name=room_name, 
            user=users.get(self.users, client_id)
        )
        if rooms.get(self.rooms, room_name):
            logger.warning(f"Room with name {room_name} already exists. Order canceled.")
            await send.to_client(
                active_connections=self.active_connections,
                client_id=client_id,
                message=messages.error(
                    client_id=client_id,
                    error="A room with the same name already exists. Creation has been aborted."
                )
            )
            return

        self.rooms.append(room)
        await self._trigger_synchronization(client_id)
        await send.to_client(
            active_connections=self.active_connections,
            client_id=client_id,
            message=messages.success(
                client_id=client_id,
                success=f"You have successfully created and joined room {room.name}"
            )
        )
        logger.info(f"New room named {room_name} has been successfully created.")

    async def join_room(self, client_id, action, room_name):
        logger.debug(f"New join room order for room with name {room_name} has been received from client with id {client_id}.")
        targeted_room = rooms.get(self.rooms, room_name)

        if not targeted_room:
            logger.error(f"Can't find room with name {room_name}. Order has ben canceled.")
            await send.to_client(
                active_connections=self.active_connections,
                client_id=client_id,
                message=messages.error(
                    client_id=client_id,
                    error=f"Can't find room with name {room_name}."
                )
            )
            return
        
        user = users.get(self.users, client_id)
        if not user:
            logger.error(f"Can't find user with id {client_id}. Leave room order has ben canceled.")
            await send.to_client(
                active_connections=self.active_connections,
                client_id=client_id,
                message=messages.error(
                    client_id=client_id,
                    error=f"Can't find client with id {client_id}."
                )
            )
            return

        old_room = rooms.get_from_user(self.rooms, user)
        if old_room:
            rooms.remove_user(self.rooms, old_room, user)
            logger.info(f"User with id {user.id} has been removed from room named {room_name}.")

        rooms.add_user(targeted_room, user)
        await self._trigger_synchronization(client_id)
        await send.to_client(
            active_connections=self.active_connections,
            client_id=client_id,
            message=messages.success(
                client_id=client_id,
                success=f"You have successfully left room {targeted_room.name}."
            )
        )
        logger.info(f"Client with id {client_id} has successfully joinded room with name {room_name}.")

    async def leave_room(self, client_id, action, room_name):
        logger.debug(f"Leave room order from room with name {room_name} has been received from client with id {client_id}.")
        room = rooms.get(self.rooms, room_name)

        if not room:
            logger.error(f"Can't find room with name {room_name}. Leave room order has ben canceled.")
            await send.to_client(
                active_connections=self.active_connections,
                client_id=client_id,
                message=messages.error(
                    client_id=client_id,
                    error=f"Can't find room with name {room_name}."
                )
            )
            return
        
        user = users.get(self.users, client_id)
        if not user:
            logger.error(f"Can't find user with id {client_id}. Leave room order has ben canceled.")
            await send.to_client(
                active_connections=self.active_connections,
                client_id=client_id,
                message=messages.error(
                    client_id=client_id,
                    error=f"Can't find client with id {client_id}."
                )
            )
            return

        rooms.remove_user(self.rooms, room, user)
        await self._trigger_synchronization(client_id)
        await send.to_client(
            active_connections=self.active_connections,
            client_id=client_id,
            message=messages.success(
                client_id=client_id,
                success=f"You have successfully created and joined room {room.name}"
            )
        )
        logger.info(f"Client with id {client_id} has successfully leave room with name {room_name}.")







