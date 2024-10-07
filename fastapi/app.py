import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

from typing import Annotated, Union

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Request,
    Query,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status,
    responses
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import logging
import sys
from loguru import logger

import api
from entities.connections_manager import ConnectionManager


sys.path.append(os.path.join(os.path.dirname(__file__)))
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
STATIC = Path(BASE_PATH, "static").resolve()


app = FastAPI(title="Complicit")
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = [
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
manager = ConnectionManager()


@app.get("/")
async def root(request: Request) -> dict:
    logging.info("Entry route has been called.")
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
        }
    )


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[Union[str, None], Cookie()] = None,
    token: Annotated[Union[str, None], Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    logger.debug(f"Websocket connection order received from client with id {client_id}")
    websocket = await api.connect(
        connection_manager=manager, 
        websocket_client=websocket, 
        client_id=client_id
    )
    try:
        while True:
            data = await api.receive(websocket_client=websocket)
            logger.debug(f"Data received : {data}")
            await getattr(api, data['action'])(
                connection_manager=manager, 
                client_id=client_id, 
                **data
            )

    except WebSocketDisconnect:
        await api.disconnect(
            connection_manager=manager, 
            websocket_client=websocket, 
            client_id=client_id
        )
