from loguru import logger

from entities import Room


def create(room_name, user):
    return Room(
        room_name,
        user
    )


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
    if room.users: room.leader = room.users[0]


def add_user(room, user):
    room.users.append(user)


def add_room(rooms, room):
    rooms.append(room)


def delete_room(rooms, room):
    rooms.remove(room)


def remove_user(room, user):
    room.users.remove(user)
    set_next_user_as_leader(room)


def assign_game(room, game):
    room.game = game
