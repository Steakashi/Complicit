from copy import deepcopy
from uuid import uuid4
from enum import Enum

class GameStatus(Enum):
    INITIALIZED = "INITIALIZED"
    STARTED = "STARTED"
    ABORTED = "ABORTED"
    ENDED = "ENDED"


class Game(object):
    id: str = ''
    theme: str = ''
    pairs: dict = {}
    answers: dict = {}
    associations: dict = {}
    status: Enum = GameStatus.INITIALIZED

    def __init__(self, theme, pairs):
        self.id = str(uuid4())
        self.theme = theme
        self.pairs  = pairs
        self.answers = {}
        self.status = GameStatus.STARTED

    def __str__(self):
        return str(self.flattened)
    
    @property
    def flattened(self):
        flattened_values = deepcopy(vars(self))
        flattened_values['status'] = flattened_values['status'].value
        return flattened_values
    
    @property
    def all_answers_registered(self):
        for _, target_id in self.pairs.items():
            if not self.answers.get(target_id): return False
        return True

