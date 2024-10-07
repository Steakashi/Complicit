import json
import random
from pathlib import Path

from loguru import logger

from entities import UserStatus


def get_from_room(room, user):
    return next(iter(room_user for room_user in room.users if user == room_user), None)

def get(users, client_id):
        return next(iter(user for user in users if user.id == client_id), None)

def add(users, user):  
    users.append(user)

def update_name(user, new_name):
    user.name = new_name

def connect_user(user):
     user.status = UserStatus.CONNECTED

def disconnect_user(user):
     user.status = UserStatus.DISCONNECTED

def generate_user_name():
    usernames_file_path = Path("./static/usernames.json").resolve()
    try:
        with open(usernames_file_path, 'r', encoding="utf-8") as usernames_file:
            usernames = json.load(usernames_file)
    except FileNotFoundError:
            logger.warning(f"Couldn't find usernames files located at {usernames_file_path}. Default name will be used.")
            return "Default and boring username"
    
    surnames, adjectives = usernames
    return random.choice(
        [
            ' '.join([random.choice(surnames).capitalize(), random.choice(adjectives)]),
            ' '.join([random.choice(adjectives).capitalize(), random.choice(surnames)]),
        ]
    )
