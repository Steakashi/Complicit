from loguru import logger

from entities import ConnectionManager
from services import games, rooms, users, messages, send


async def launch_game(connection_manager: ConnectionManager, client_id: str, room_name: str, action: str):
    logger.debug(f"Launch game order for room {room_name} has been received from client with id {client_id}.")
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

    theme = games.pick_theme()
    pairs = games.generate_pairs(concerned_room.users)
    game = games.create(theme, pairs)
    games.add_game(connection_manager.games, game)
    rooms.assign_game(concerned_room, game)

    for user in concerned_room.users: users.await_for_answer(user)

    await send.to_room(
        active_connections=connection_manager.connections,
        room=concerned_room,
        message=messages.default(
            action=action,
            game=game,
            client_id=client_id,
            success=f"Game has started. Enjoy !"
        )
    )

    logger.info(f"Game for room named {room_name} has successfully started.")


async def register_answer(connection_manager: ConnectionManager, client_id: str, room_name:str, game_id: str, answer: str):
    logger.debug(f"Register answer '{answer}' has been received from client with id {client_id}.")

    concerned_game = games.get(connection_manager.games, game_id)
    if not concerned_game:
        logger.error(f"Can't find game with id {game_id}. Order has ben canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error=f"Can't find game with id {game_id}."
            )
        )
        return

    games.register_answer(concerned_game, client_id, answer)

    concerned_user = users.get(connection_manager.users, client_id)

    if not concerned_user:
        logger.error(f"Can't find user with id {client_id}. Order has ben canceled.")
        await send.to_client(
            active_connections=connection_manager.connections,
            client_id=client_id,
            message=messages.error(
                client_id=client_id,
                error=f"Can't find user with id {client_id}."
            )
        )
        return

    users.validate_answer(concerned_user)

    if concerned_game.all_answers_registered:
        logger.debug(f"All required answers has been registered on game side. Will now proceed to second step for every players in room.")

        concerned_room = rooms.get(connection_manager.rooms, room_name)

        if not concerned_room:
            logger.error(f"Can't find room for client with id {client_id}. Order has ben canceled.")
            await send.to_client(
                active_connections=connection_manager.connections,
                client_id=client_id,
                message=messages.error(
                    client_id=client_id,
                    error=f"Can't find room from user {client_id}."
                )
            )
            return

        await send.to_room(
            active_connections=connection_manager.connections,
            room=concerned_room,
            message=messages.default(
                action="trigger_guess_phase",
                game=concerned_game,
                client_id=client_id,
                success=f"Game has started. Enjoy !"
            )
        )

    await send.to_client(
        active_connections=connection_manager.connections,
        client_id=client_id,
        message=messages.success(
            client_id=client_id,
            success=f"Your answer '{ answer }' has been successfully registered."
        )
    )
    