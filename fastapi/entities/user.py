from copy import deepcopy
from enum import Enum

class UserStatus(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    WAITING = "WAITING"
    

class InGameStatus(Enum):
    WAITING = "WAITING"
    ANSWERED = "ANSWERED"
    NOT_IN_GAME = "NOT_IN_GAME"


class User(object):
    id: str = ''
    name: str = ''
    status: str = UserStatus.WAITING
    game_status: str = InGameStatus.NOT_IN_GAME

    def __init__(self, client_id, user_name):
        self.id = client_id
        self.name = user_name
        self.status = UserStatus.CONNECTED
        self.game_status = InGameStatus.NOT_IN_GAME

    def __str__(self):
        return str(self.flattened)
    
    def __eq__(self, other):
        return self.id == other.id

    @property
    def flattened(self):
        flattened_values = deepcopy(vars(self))
        flattened_values['status'] = flattened_values['status'].value
        flattened_values['game_status'] = flattened_values['game_status'].value
        return flattened_values
