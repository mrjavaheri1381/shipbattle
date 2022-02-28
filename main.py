from socket import socket
from asyncio import sleep
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from models import Player, Game, Ship
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


Queue: list[Player] = []
Games: list[Game] = []


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await websocket.accept()
    await websocket.send_text('salam')
    player = Player(websocket, client_name)
    if(len(Queue) < 1):
        # host
        Queue.append(player)
    else:
        # peer
        game = Game(player, Queue[0])
        Queue.pop(0)
        print('qqq')
        game.Start()
    print(Queue)
    try:
        while 1:
            pass
    except WebSocketDisconnect:
        await player.currentRival.send_text(f"{client_name} left")
        socket.close()
