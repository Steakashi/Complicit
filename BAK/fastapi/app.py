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
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import logging
import sys
from loguru import logger


from connection_manager import ConnectionManager


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
app = FastAPI(title="Complicit")
app.mount("/static", StaticFiles(directory="static"), name="static")

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


# @app.websocket("/items/{item_id}/ws")
# async def websocket_endpoint(
#     *,
#     websocket: WebSocket,
#     item_id: str,
#     q: Union[int, None] = None,
#     cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
# ):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(
#             f"Session cookie or query token value is: {cookie_or_token}"
#         )
#         if q is not None:
#             await websocket.send_text(f"Query parameter q is: {q}")
#         await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client_id = 2
    logger.debug(f"Websocket message received with client_id {client_id}")
    websocket = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.debug(f"Data received : {data}")
            # await getattr(manager, data['action'])(client_id, data['room_name'])

            # await manager.send_personal_message(
            #     client_id=client_id,
            #     message=f"You wrote: {data}", 
            # )
            # await manager.send_message_to_others(
            #     client_id=client_id,
            #     message=f"Client #{client_id} says: {data}", 
            # )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")