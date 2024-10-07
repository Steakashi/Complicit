from copy import deepcopy
from enum import Enum

class UserStatus(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    WAITING = "WAITING"


class User(object):
    id: str = ''
    name: str = ''
    status: str = UserStatus.WAITING

    def __init__(self, client_id, user_name):
        self.id = client_id
        self.name = user_name
        self.status = UserStatus.CONNECTED

    def __str__(self):
        return str(self.flattened)
    
    def __eq__(self, other):
        return self.id == other.id

    @property
    def flattened(self):
        flattened_values = deepcopy(vars(self))
        flattened_values['status'] = flattened_values['status'].value
        return flattened_values
