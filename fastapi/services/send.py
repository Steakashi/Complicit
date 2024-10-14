from loguru import logger

from . import connections


async def _send(websocket, message):
    try:
        await websocket.send_json(message)
    except RuntimeError as err:
        logger.error(f"Can't send json to websocket {websocket}.")
        raise err


async def to_all(active_connections: list, message: str):
    for websocket in await connections.get(active_connections):
        await _send(websocket, message)
    logger.info(f"Global message '{message}' has been correctly sent to all users.")


async def to_client(active_connections: list, client_id: int, message: str):
    for websocket in await connections.get_with(active_connections, client_id):
        await _send(websocket, message)
    logger.info(f"Personal message '{message}' has been correctly sent to client with id {client_id}.")


async def to_others(active_connections: list, client_id: int, message: str):
    for websocket in await connections.get_without(active_connections, client_id):
        await _send(websocket, message)
    logger.info(f"Global message '{message}' has been correctly sent to all users except client with id {client_id}.")


async def to_room(active_connections: list, room: object, message: str):
    for user in room.users:
        for websocket in await connections.get_with(active_connections, user.id):
            await _send(websocket, message)
    logger.info(f"Room message '{message}' has been correctly sent to client in room {room.name}.")
