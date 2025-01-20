import pygame
import buttons_class
from spritesheet import spritesheet
import sprite_classes
from txt_to_dictionary import get_all_dict

pygame.init()

inf = pygame.display.Info()
w, h = inf.current_w, inf.current_h - 32

win = pygame.display.set_mode((w, h))
space_ship_images = pygame.image.load("assets/ship_assets.png").convert_alpha()

deploy = pygame.image.load("assets/deployer.png").convert_alpha()
deploy = pygame.transform.scale2x(deploy)


PLAY = pygame.image.load("assets/play.png").convert_alpha()
P_POS = (w / 2) - (PLAY.get_width() / 2), 200
SETTING = pygame.image.load("assets/settings.png").convert_alpha()
S_POS = (w / 2) - (SETTING.get_width() / 2), PLAY.get_height() + 250
MODE = pygame.image.load("assets/mode.png").convert_alpha()
M_POS = (w / 2) - (MODE.get_width() / 2), S_POS[1] + SETTING.get_height() + 50
ESC = pygame.image.load("assets/escape.png").convert_alpha()
E_POS = (w / 2) - (MODE.get_width() / 2), M_POS[1] + MODE.get_height() + 50

SOUND = pygame.image.load("assets/sound.png").convert_alpha()
SO_POS = (w /2) - (SOUND.get_width() / 2), 200
CONTROLS = pygame.image.load("assets/controls.png").convert_alpha()
C_POS = (w / 2) - (CONTROLS.get_width() / 2), SOUND.get_height() + 250
INFO = pygame.image.load("assets/info.png").convert_alpha()
I_POS = (w / 2) - (INFO.get_width() / 2), C_POS[1] + CONTROLS.get_height() + 50
BACK = pygame.image.load("assets/back.png").convert_alpha()
B_POS = (w / 2) - (BACK.get_width() / 2), I_POS[1] + INFO.get_height() + 50

VOL_HIGH = pygame.image.load("assets/vol__high.png").convert_alpha()
VOL_NORM = pygame.image.load("assets/vol__normal.png").convert_alpha()
VOL_LOW = pygame.image.load("assets/vol__low.png").convert_alpha()
NO_VOL = pygame.image.load("assets/no__vol.png").convert_alpha()

NO_POS = 449.5, 200
L_POS = NO_POS[0] + NO_VOL.get_width() + 50, 200
N_POS = L_POS[0] + VOL_LOW.get_width() + 50, 200
H_POS = N_POS[0] + VOL_NORM.get_width() + 50, 200

space_ships = spritesheet(space_ship_images, 6, 1, 31, 31, 2)
enemy_data = get_all_dict("enemies.txt")

pygame.mixer.music.load("assets/back.wav")
pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.75)

for i, enemy in enumerate(enemy_data):
    enemy["image"] = space_ships[i + 1]

clock = pygame.time.Clock()
#ALL CAPS FOR THIS FONT EXCEPT FOR INTEGERS
font = pygame.font.Font("assets/game_font.ttf", 32)

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

def main():
    player = sprite_classes.Player(space_ships[0], win)
    deployer = sprite_classes.Deployer(deploy)
    enemies = sprite_classes.EnemyGroup()
    menu = buttons_class.ButtonTree()

    menu.add_branch("", "play", "func", PLAY, P_POS, play)

    menu.add_branch("", "setting", "button", SETTING, S_POS)

    menu.add_branch("setting", "sound", "button", SOUND, SO_POS)
    menu.add_branch("setting/sound", "mute", "func", NO_VOL, NO_POS, no_vol)
    menu.add_branch("setting/sound", "low", "func", VOL_LOW, L_POS, low)
    menu.add_branch("setting/sound", "norm", "func", VOL_NORM, N_POS, norm)
    menu.add_branch("setting/sound", "high", "func", VOL_HIGH, H_POS, high)
    menu.add_branch("setting/sound", "back", "back", BACK, B_POS)

    menu.add_branch("setting", "controls", "button", CONTROLS, C_POS)
    menu.add_branch("setting/controls", "back", "back", BACK, B_POS)

    menu.add_branch("setting", "info", "button", INFO, I_POS)
    menu.add_branch("setting/info", "back", "back", BACK, B_POS)

    menu.add_branch("setting", "back", "back", BACK, B_POS)

    menu.add_branch("", "mode", "button", MODE, M_POS)
    menu.add_branch("mode", "back", "back", BACK, B_POS)

    menu.add_branch("", "escape", "quit", ESC, E_POS)
    run = True
    while run:
        
        win.fill((0, 0, 0))

        fps = clock.get_fps()
        text = font.render(f"FPS {int(fps)}", True, (255, 255, 255))
        health = font.render(f"HEALTH {player.health}", True, (255, 255, 255))
        h_rect = health.get_rect(topright=(w - 10, 10))

        win.blit(text, (10, 10))
        if player.play == "play":

            for enemy in enemy_data:
                en = sprite_classes.Enemy(enemy, win, player)
                enemies.enemy_add(en)

            win.blit(health, h_rect)
            
            sprite_classes.player_bullets.update()
            sprite_classes.player_bullets.draw(win)
            enemies.update()
            enemies.draw(win)
            deployer.update(win)
            deployer.draw(win)
            player.update()
            player.draw(win)
        elif player.play == "menu":
            run = menu.update(win, player)
            pygame.mixer.music.set_volume(player.vol)
        else:
            prev_sound = player.vol
            enemies.empty()
            sprite_classes.player_bullets.empty()
            player = sprite_classes.Player(space_ships[0], win)
            deployer = sprite_classes.Deployer(deploy)
            player.play = "menu"
            player.vol = prev_sound
            menu.starting_point()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

if __name__ == "__main__":
    main()
pygame.mixer.music.unload()
pygame.quit()