from copy import deepcopy
from uuid import uuid4
from enum import Enum


class Room(object):
    id: str = ''
    name: str = ''
    leader: object
    users: list[object] = []
    game: object = None

    def __init__(self, room_name, user):
        self.id = str(uuid4())
        self.name = room_name
        self.leader = user
        self.users = [user]
        self.game = None

    def __str__(self):
        return str(self.flattened)
    
    @property
    def flattened(self):
        result = deepcopy(vars(self))
        users = list()
        for user in self.users:
            users.append(user.flattened)
        result.update(
            {
                'leader': self.leader.flattened,
                'users': users,
                'game_in_progress': self.game_in_progress
            }
        )
        if self.game: result.update({'game': self.game.flattened})
        return result
    @property
    def is_empty(self):
        return bool(self.users)

    @property
    def game_in_progress(self):
        return self.game and self.game.in_progress 
        
