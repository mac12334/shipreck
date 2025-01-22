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

def default(client: sprite_classes.Player) -> None:
    client.game = "default"
def crash(client: sprite_classes.Player) -> None:
    client.game = "crash"

def health_boost(client: sprite_classes.Player) -> None:
    client.health += 10
    if client.health > 100:
        client.health = 100
    client.collect_health.play()

def aim(client: sprite_classes.Player) -> None:
    client.power = "aim"
    client.collect_aim.play()

def change_speed(client: sprite_classes.Player) -> None:
    client.change_speed = True
def change_slow(client: sprite_classes.Player) -> None:
    client.change_slow = True
def change_left(client: sprite_classes.Player) -> None:
    client.change_left = True
def change_right(client: sprite_classes.Player) -> None:
    client.change_right = True
def change_shoot(client: sprite_classes.Player) -> None:
    client.change_shoot = True

def make_text_appear(font: pygame.font.Font, text: str, size: tuple[int, int]) -> pygame.Surface:
    surface = pygame.Surface(size)
    surface.fill((0,0,0))
    letter = font.render("A", True, (0, 0, 0))
    max_char = size[0] // letter.get_width()
    lines = break_up_text(text, max_char)
    for y, line in enumerate(lines):
        t = font.render(line.upper(), True, (255, 255, 255))
        pos = (surface.get_width() / 2) - (t.get_width() / 2), y * (t.get_height() + 25)
        surface.blit(t, pos)
    surface.set_colorkey((0, 0,0))
    return surface.convert_alpha()


def break_up_text(text: str, max_char: int) -> list[str]:
    individual_words = text.split(" ")
    line = ""
    lines = []
    for word in individual_words:
        if len(word) + len(line) + 1 <= max_char:
            line = line + word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    return lines