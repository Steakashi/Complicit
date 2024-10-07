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

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}
        self.rooms: list[Room] = []

    async def connect(self, websocket: WebSocket):
        client_id = 2#websocket.path_params['client_id']
        logger.debug(f"Connecting client with id {client_id}.")
        await websocket.accept()

        if not self.active_connections.get(client_id):
            logger.debug(f"Client with ID {client_id} has no active connection. Initializing list.")
            self.active_connections[client_id] = list()  
        
        self.active_connections[client_id].append(websocket)

        logger.info(f"Client with ID {client_id} has successfully connected.")
        logger.debug(f"Client with ID {client_id} has currently {len(self.active_connections[client_id])} active websockets.")

        return websocket

    def disconnect(self, websocket: WebSocket):
        client_id = websocket.path_params['client_id']
        logger.debug(f"Disconnecting client with id {client_id}.")
        websockets_for_client = self.active_connections.get(client_id)
        
        if not websockets_for_client:
            logger.error(f"No active connection has been found for client with ID {client_id}. Abort process.")
            return
        
        if not websocket in websockets_for_client:
            logger.error(f"Can't find websocket {websocket} for client with ID {client_id}.")

        websockets_for_client.remove(websocket)

        if len(websockets_for_client) <= 0:
            logger.info(f"Client with id {client_id} has been completely disconnected.")
        
        else:
            logger.info(
                f"Websocket {websocket} has been removed for client with id {client_id} "
                f"but still has {len(websockets_for_client)} active connection."
            )

    async def create_room(self, client_id, room_name):
        logger.debug(f"New create room order with name {room_name} has been received from client with id {client_id}.")
        room = Room(room_name)
        room.add_user(client_id)
        self.rooms.append(room)
        await self.broadcast(message='{"result": "room_created", "room_name": "room_name}"}')
        logger.info(f"New room named {room_name} has been successfully created.")

    async def _get_user_active_connections(self, client_id: str):
        return self.active_connections.get(client_id, [])
    
    async def _get_active_connections(self, exclude=None):
        websockets = list()
        for client_id, user_websockets in self.active_connections.items():
            if exclude and client_id in exclude: continue
            websockets.extend(user_websockets)
        return websockets

    async def send_personal_message(self, client_id: str, message: str):
        for websocket in await self._get_user_active_connections(client_id):
            await websocket.send_json(message)
        logger.info(f"Personal message '{message}' has been correctly sent to client with id {client_id}.")

    async def send_message_to_others(self, client_id: str, message: str):
        for websocket in await self._get_active_connections(exclude=[client_id]):
            await websocket.send_json(message)
        logger.info(f"Global message '{message}' has been correctly sent to all users except client with id {client_id}.")

    async def broadcast(self, message: str):
        for websocket in await self._get_active_connections():
            await websocket.send_json(message)
        logger.info(f"Global message '{message}' has been correctly sent to all users.")

    async def broadcast_to_room(self, message: str):
        pass
        # for room in self.rooms:
        #     for user in room.users:
        #         await user.send_text(message)


class Room:
    id: str = ''
    users: list = []

    def __init__(self, room_name):
        self.id = str(uuid4())
        self.name = room_name

    def add_user(self, user):
        self.users.append(user)
