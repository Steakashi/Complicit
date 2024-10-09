from . import Room, User, Game

class ConnectionManager:
    connections: dict = {}
    rooms: list[Room] = []
    users: list[User] = []
    games: list[Game] = []
