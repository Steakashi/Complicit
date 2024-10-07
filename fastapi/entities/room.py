from copy import deepcopy
from uuid import uuid4

class Room(object):
    id: str = ''
    name: str = ''
    leader: object
    users: list[object] = []

    def __init__(self, room_name, user):
        self.id = str(uuid4())
        self.name = room_name
        self.leader = user
        self.users = [user]

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
                'users': users
            }
        )
        return result
