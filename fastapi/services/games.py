import json
import random
from pathlib import Path
from copy import deepcopy

from loguru import logger

from entities import Game


def create(theme, pairs):
    return Game(
        theme,
        pairs
    )


def add_game(games, game):
    games.append(game)


def get(games, game_id):
    return next(iter(game for game in games if game.id == game_id), None)


def pick_theme():
    themes_file_path = Path("./static/themes.json").resolve()
    try:
        with open(themes_file_path, 'r', encoding="utf-8") as themes_file:
            return random.choice(json.load(themes_file))
    except FileNotFoundError:
            logger.warning(f"Couldn't find themes files located at {themes_file_path}. Default theme will be used.")
            return "Default and boring theme"
    

def generate_pairs(players):
    players_to_pick = deepcopy(players)
    pairs = dict()
    for player in players:
        picked_player = random.choice(players_to_pick)
        pairs[player.id] = picked_player.id
        players_to_pick.remove(picked_player)
    
    return pairs


def register_answer(game, user_id, answer):
    game.answers[user_id] = answer
     
