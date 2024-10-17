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


from entities import Room, User, ConnectionManager
from services import rooms, users, send, connections, messages


async def connect(connection_manager: ConnectionManager, websocket: WebSocket, client_id: str):
    logger.debug(f"Connecting client with id {client_id}.")
    await websocket.accept()

    if not await connections.get_with(connection_manager.connections, client_id):
        logger.debug(f"Client with ID {client_id} has no active connection. Initializing list.")
        await connections.initialize_for_client(connection_manager.connections, client_id)
        
    await connections.add(connection_manager.connections, client_id, websocket)

    logger.info(f"Client with ID {client_id} has successfully connected.")
    logger.debug(
        f"Client with ID {client_id} has currently "
        f"{len(await connections.get_with(connection_manager.connections, client_id))} "
        f"active websockets.")

    user = users.get(connection_manager.users, client_id)
    if not user:
        user = User(
            client_id=client_id,
            user_name=users.generate_user_name()
        )
        users.add(connection_manager.users, user)
        logger.debug(f"User with ID {client_id} has not been found et has been added to users list.")

    users.connect(user)

    await send.to_client(
        active_connections=connection_manager.connections,
        client_id=client_id,
        message=messages.default(
            action="retrieve_user",
            client_id=client_id,
            user=user
        )
    )

    return websocket

async def disconnect(connection_manager: ConnectionManager, websocket: WebSocket, client_id: str):
    logger.debug(f"Disconnecting client with id {client_id}.")
    websockets_for_client = await connections.get_with(connection_manager.connections, client_id)
    
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

    user = users.get(connection_manager.users, client_id)
    room = rooms.get_from_user(connection_manager.rooms, user)

    if room:
        rooms.remove_user(connection_manager.rooms, room, user)
        logger.info(f"User named {user.name} with id {user.id} has been removed from room named {room.name} due to disconnection.")

        if room.is_empty:
            rooms.delete_room(connection_manager.rooms, room)
            logger.info(f"Room with name {room.name} has no longer user in it and has been erased.")

    users.disconnect(user)

    await send.to_all(
        active_connections=connection_manager.connections,
        message=messages.default(
            action="synchronize",
            client_id=client_id,
            rooms=connection_manager.rooms,
            users=connection_manager.users
        )
    )


async def receive_data(websocket_client: WebSocket):
    return await websocket_client.receive_json()


async def synchronize_for_all(connection_manager: ConnectionManager, client_id: str):
    logger.debug(f"Synchronize order has been received from client with id {client_id} for all users.")
    await send.to_all(
        active_connections=connection_manager.connections,
        message=messages.default(
            action="synchronize",
            client_id=client_id,
            rooms=connection_manager.rooms,
            users=connection_manager.users
        )
    )

async def synchronize_for_room(connection_manager: ConnectionManager, client_id: str, room_name: str):
    logger.debug(f"Synchronize order has been received from client with id {client_id} for room named {room_name}.")
    concerned_room = rooms.get(connection_manager.rooms, room_name)

    if not concerned_room:
        logger.error(f"Can't find room with name {room_name}. Order has ben canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error=f"Can't find room with name {room_name}."
            )
        )
        return

    await send.to_room(
        active_connections=connection_manager.connections,
        room=concerned_room,
        message=messages.default(
            action="synchronize",
            client_id=client_id,
            rooms=connection_manager.rooms,
            users=connection_manager.users
        )
    )
