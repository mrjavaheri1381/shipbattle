from uuid import uuid4
from typing import List, Dict

from fastapi import WebSocket


class Ship():
    target = [None, None]

    def __init__(self, speed, damage, health, distance, uid):
        self.speed = speed
        self.damage = damage
        self.health = health
        self.range = distance
        self.x = 100
        self.uid = uid
        self.alive = True
        self.movement = True
        self.fighting = False

    def getX(self):
        if(self.movement):
            self.x += 1
            return self.x
        return None

    def __repr__(self):
        return f"{self.uid}|{self.x}|{self.health}|{self.alive}"


class Tower():
    def __init__(self):
        self.Health = 1500


class Player():
    ships: List[Ship] = []
    tower = Tower()

    def __init__(self, socket: WebSocket, name):
        self.socket = socket
        self.name = name


class Game():
    isPlay = False

    def __init__(self, player1: Player, player2: Player):
        # self.players = {player1.id: player1, player2.id: player2}
        self.players = [player1, player2]

    async def sendData(self):
        player1, player2 = self.players
        for ship1 in player1.ships:
            await player1.socket.send_text(ship1)
            await player2.socket.send_text('@'+ship1)
        for ship2 in player2.ships:
            await player1.socket.send_text('@'+ship2)
            await player2.socket.send_text(ship2)

        pass

    def calculateDistances(self):
        for ship1 in self.players[0].ships:
            for ship2 in self.players[1].ships:
                distance = 854-ship1.x-ship2.x
                if(distance > ship1.range and ship1.alive and ship2.alive):
                    ship1.movement = False
                    if(ship1.target[1] and ship1.target[1] < distance):
                        ship1.target = [ship2, distance]
                if(distance > ship2.range):
                    ship2.movement = False
                    if(ship2.target[1] and ship1.alive and ship2.alive):
                        ship1.target = [ship2, distance]

    async def Start(self):
        await self.players[0].socket.send_text('start?')
        await self.players[0].socket.receive_text()
        # await self.players[1].socket.send_text('start?')
        # await self.players[1].socket.receive_text()
        # self.isPlay = True
        # while self.isPlay:
        #     self.calculateDistances()
        #     self.sendData()

        pass
