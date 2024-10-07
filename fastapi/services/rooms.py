from loguru import logger

from entities import Room


def get_from_user(rooms, user):
    return next(
        iter(
            room for room in rooms
            if user and user in room.users
        ), None
    )


def get(rooms, room_name):
    return next(iter(room for room in rooms if room.name == room_name), None)


def set_next_user_as_leader(room):
    room.leader = room.users[0]


def create(room_name, user):
    return Room(
        room_name,
        user
    )


def add_user(room, user):
    room.users.append(user)


def add_room(rooms, room):
    rooms.append(room)


def remove_user(rooms, room, user):
    room.users.remove(user)
    if not room.users:
        rooms.remove(room)
        logger.info(f"Room with name {room.name} has no longer user in it and has been erased.")
    
    else:
        set_next_user_as_leader(room)

