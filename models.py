from uuid import uuid4

from fastapi import WebSocket


class Ship():
    def __init__(self, speed, damage, health, distance, uid):
        self.speed = speed
        self.damage = damage
        self.health = health
        self.currentHealth = health
        self.distance = distance
        self.x = 100
        self.uid = uid
        self.alive = True
        self.movement = True

    def getX(self):
        if(self.movement):
            self.x += 1
            return self.x
        return None


class Tower():
    def __init__(self):
        self.Health = 1500


class Player():
    ships: Ship = {}
    tower = Tower()

    def __init__(self, socket: WebSocket, name, id):
        self.socket = socket
        self.name = name
        self.id = id


class Game():
    def __init__(self, player1: Player, player2: Player):
        self.players = {player1.id: player1, player2.id: player2}

    def start():
        pass
