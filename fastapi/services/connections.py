from fastapi import WebSocket


async def get(connections):
    return [websocket for _, user_websockets in connections.items() for websocket in user_websockets]

async def get_without(connections, exclude):
    if type(exclude) is not list: exclude = [exclude]
    return [
        websocket for client_id, user_websockets in connections.items() for websocket in user_websockets
        if client_id not in exclude
    ]

async def get_with(connections, client_id: str):
    return connections.get(client_id, [])

async def add(connections: list, client_id: str, websocket: WebSocket):
    connections[client_id].append(websocket)

async def initialize_for_client(connections: list, client_id: str):
    connections[client_id] = list()  