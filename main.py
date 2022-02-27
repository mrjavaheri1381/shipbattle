import base64
from multiprocessing.connection import wait
from socket import socket
from time import sleep
import uuid
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class Player():
    currentRival: WebSocket = None

    def __init__(self, websocket: WebSocket, name):
        self.webSocket: WebSocket = websocket
        self.name = name
        self.id = uuid.uuid4()
        pass


Queue: list[Player] = []


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await websocket.accept()
    await websocket.send_text('start')
    # await websocket.send_text('joined')
    player = Player(websocket, client_name)
    if(len(Queue) < 1):
        # host
        Queue.append(player)
    else:
        # peer
        player.currentRival = Queue[0].webSocket
        Queue[0].currentRival = websocket
        Queue.pop(0)

    try:
        x = 0
        while True:
            await websocket.send_text("salam")
            sleep(1)

    except WebSocketDisconnect:
        await player.currentRival.send_text(f"{client_name} left")
        socket.close()
