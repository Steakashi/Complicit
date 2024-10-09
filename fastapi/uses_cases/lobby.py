from loguru import logger

from entities import ConnectionManager
from services import rooms, users, send, messages


async def update_user_name(connection_manager: ConnectionManager, client_id: str, action: str, user_name: str):
    logger.debug(f"Update user name order with value {user_name} has been received from client with id {client_id}.")
    concerned_user = users.get(connection_manager.users, client_id)
    if not concerned_user:
        logger.error(f"Can't find user with id {client_id}. Order has ben canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error=f"Can't find client with id {client_id}."
            )
        )
        return

    users.update_name(concerned_user, user_name)

    await send.to_client(
        active_connections=connection_manager.connections,
        client_id=client_id,
        message=messages.default(
            action=action,
            client_id=client_id,
            user=concerned_user,
            success="Username has been correctly updated."
        )
    )


async def create_room(connection_manager: ConnectionManager, client_id: str, room_name: str):
    logger.debug(f"New create room order with name {room_name} has been received from client with id {client_id}.")
    room = rooms.create(
        room_name=room_name, 
        user=users.get(connection_manager.users, client_id)
    )
    if rooms.get(connection_manager.rooms, room_name):
        logger.warning(f"Room with name {room_name} already exists. Order canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error="A room with the same name already exists. Creation has been aborted."
            )
        )
        return

    rooms.add_room(connection_manager.rooms, room)
    await send.to_client(
        active_connections=connection_manager.connections,
        client_id=client_id,
        message=messages.success(
            client_id=client_id,
            success=f"You have successfully created and joined room {room.name}"
        )
    )
    logger.info(f"New room named {room_name} has been successfully created.")


async def join_room(connection_manager: ConnectionManager, client_id: str, room_name: str):
    logger.debug(f"New join room order for room with name {room_name} has been received from client with id {client_id}.")
    targeted_room = rooms.get(connection_manager.rooms, room_name)

    if not targeted_room:
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
    
    user = users.get(connection_manager.users, client_id)
    if not user:
        logger.error(f"Can't find user with id {client_id}. Leave room order has ben canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error=f"Can't find client with id {client_id}."
            )
        )
        return

    old_room = rooms.get_from_user(connection_manager.rooms, user)
    if old_room:
        rooms.remove_user(connection_manager.rooms, old_room, user)
        logger.info(f"User with id {user.id} has been removed from room named {room_name}.")

    rooms.add_user(targeted_room, user)
    await send.to_client(
        active_connections=connection_manager.connections,
        client_id=client_id,
        message=messages.success(
            client_id=client_id,
            success=f"You have successfully left room {targeted_room.name}."
        )
    )
    logger.info(f"Client with id {client_id} has successfully joinded room with name {room_name}.")


async def leave_room(connection_manager: ConnectionManager, client_id: str, room_name: str):
    logger.debug(f"Leave room order from room with name {room_name} has been received from client with id {client_id}.")
    room = rooms.get(connection_manager.rooms, room_name)

    if not room:
        logger.error(f"Can't find room with name {room_name}. Leave room order has ben canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error=f"Can't find room with name {room_name}."
            )
        )
        return
    
    user = users.get(connection_manager.users, client_id)
    if not user:
        logger.error(f"Can't find user with id {client_id}. Leave room order has ben canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error=f"Can't find client with id {client_id}."
            )
        )
        return

    rooms.remove_user(connection_manager.rooms, room, user)
    await send.to_client(
        active_connections=connection_manager.connections,
        client_id=client_id,
        message=messages.success(
            client_id=client_id,
            success=f"You have successfully left room {room.name}"
        )
    )
    logger.info(f"Client with id {client_id} has successfully leave room with name {room_name}.")
