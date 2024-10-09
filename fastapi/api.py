from fastapi import WebSocket


from entities import ConnectionManager
from uses_cases import game, lobby, websocket


def synchronize_after_for_all(f):
    async def wrap(*args, **kwargs):
        returned_value = await f(*args, **kwargs)
        await synchronize_all(
            connection_manager=kwargs.get('connection_manager'), 
            client_id=kwargs.get('client_id')
        )
        return returned_value
    return wrap


def synchronize_after_for_room(f):
    async def wrap(*args, **kwargs):
        returned_value = await f(*args, **kwargs)
        await synchronize_room(
            connection_manager=kwargs.get('connection_manager'), 
            client_id=kwargs.get('client_id'),
            room_name=kwargs.get('room_name')
        )
        return returned_value
    return wrap


async def synchronize_all(*, connection_manager: ConnectionManager, client_id: str, action: str = None):
    await websocket.synchronize_for_all(
        connection_manager=connection_manager, 
        client_id=client_id
    )


async def synchronize_room(*, connection_manager: ConnectionManager, client_id: str, room_name: str, action: str = None):
    await websocket.synchronize_for_room(
        connection_manager=connection_manager, 
        client_id=client_id,
        room_name=room_name
    )


@synchronize_after_for_all
async def connect(*, connection_manager: ConnectionManager, client_id: str, websocket_client: WebSocket):
    return await websocket.connect(
        connection_manager=connection_manager, 
        websocket=websocket_client, 
        client_id=client_id
    )


async def receive(*, websocket_client: WebSocket):
    return await websocket.receive_data(websocket_client)


@synchronize_after_for_all
async def disconnect(*, connection_manager: ConnectionManager, client_id: str, websocket_client: WebSocket):
    await websocket.disconnect(
        connection_manager=connection_manager, 
        websocket=websocket_client, 
        client_id=client_id
    )


@synchronize_after_for_all
async def update_user_name(*, connection_manager: ConnectionManager, client_id: str, action: str, user_name: str):
    await lobby.update_user_name(
        connection_manager=connection_manager, 
        client_id=client_id,
        action=action,
        user_name=user_name
    )


@synchronize_after_for_all
async def create_room(*, connection_manager: ConnectionManager, client_id: str, room_name: str, action: str = None):
    await lobby.create_room(
        connection_manager=connection_manager, 
        client_id=client_id,
        room_name=room_name
    )
    

@synchronize_after_for_all
async def join_room(*, connection_manager: ConnectionManager, client_id: str, room_name: str, action: str = None):
    await lobby.join_room(
        connection_manager=connection_manager, 
        client_id=client_id,
        room_name=room_name
    )


@synchronize_after_for_all
async def leave_room(*, connection_manager: ConnectionManager, client_id: str, room_name: str, action: str = None):
    await lobby.leave_room(
        connection_manager=connection_manager, 
        client_id=client_id,
        room_name=room_name
    )
 
@synchronize_after_for_room
async def launch_game(*, connection_manager: ConnectionManager, client_id: str, room_name: str, action: str = None):
    await game.launch_game(
        connection_manager=connection_manager, 
        client_id=client_id,
        room_name=room_name,
        action=action
    )

@synchronize_after_for_room
async def register_answer(*, connection_manager: ConnectionManager, client_id: str, room_name: str, game_id: str, answer: str, action: str = None):
    await game.register_answer(
        connection_manager=connection_manager, 
        client_id=client_id,
        room_name=room_name,
        game_id=game_id,
        answer=answer
    )
