from . import Room, User

class ConnectionManager:
    connections: dict = {}
    rooms: list[Room] = []
    users: list[User] = []
