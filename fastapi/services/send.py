from loguru import logger

from . import connections


async def to_all(active_connections: list, message: str):
    for websocket in await connections.get(active_connections):
        try:
            await websocket.send_json(message)
        except RuntimeError:
            logger.error(f"Can't send json to websocket {websocket}.")
    logger.info(f"Global message '{message}' has been correctly sent to all users.")


async def to_client(active_connections: list, client_id: int, message: str):
    for websocket in await connections.get_with(active_connections, client_id):
        try:
            await websocket.send_json(message)
        except RuntimeError:
            logger.error(f"Can't send json to websocket {websocket}.")
    logger.info(f"Personal message '{message}' has been correctly sent to client with id {client_id}.")


async def to_others(active_connections: list, client_id: int, message: str):
    for websocket in await connections.get_without(active_connections, client_id):
        try:
            await websocket.send_json(message)
        except RuntimeError:
            logger.error(f"Can't send json to websocket {websocket}.")
    logger.info(f"Global message '{message}' has been correctly sent to all users except client with id {client_id}.")

async def to_room(self, message: str):
    pass
    # for room in self.rooms:
    #     for user in room.users:
    #         await user.send_text(message)
