import pygame, sprite_classes

pygame.init()

def play(client: sprite_classes.Player) -> None:
    client.play = "play"

def high(client: sprite_classes.Player) -> None:
    client.vol = client.high_vol
def norm(client: sprite_classes.Player) -> None:
    client.vol = client.norm_vol
def low(client: sprite_classes.Player) -> None:
    client.vol = client.low_vol
def no_vol(client: sprite_classes.Player) -> None:
    client.vol = 0

def health_boost(client: sprite_classes.Player) -> None:
    client.health += 50
    if client.health > 100:
        client.health = 100

def aim(client: sprite_classes.Player) -> None:
    client.power = "aim"