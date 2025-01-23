import pygame
import buttons_class
from spritesheet import spritesheet
import sprite_classes
from txt_to_dictionary import get_all_dict
from callbacks import *

pygame.init()

inf = pygame.display.Info()
w, h = inf.current_w, inf.current_h - 32

win = pygame.display.set_mode((w, h))
space_ship_images = pygame.image.load("assets/ship_assets.png").convert_alpha()

deploy = pygame.image.load("assets/deployer.png").convert_alpha()
deploy = pygame.transform.scale2x(deploy)

power_up_images = pygame.image.load("assets/power_up_images.png").convert_alpha()

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

DEF = pygame.image.load("assets/default.png").convert_alpha()
D_POS = (w / 2) - (DEF.get_width() / 2), 200
CRASH = pygame.image.load("assets/crash__course.png").convert_alpha()
CR_POS = (w / 2) - (CRASH.get_width() / 2), D_POS[1] + DEF.get_height() + 50

SPEED = pygame.image.load("assets/speed__up.png").convert_alpha()
SP_POS = (w / 2) - (SPEED.get_width() / 2), 200
SLOW = pygame.image.load("assets/slow__down.png").convert_alpha()
SL_POS = (w / 2) - (SLOW.get_width() / 2), SP_POS[1] + SPEED.get_height() + 50
LEFT = pygame.image.load("assets/turn__left.png").convert_alpha()
LE_POS = (w / 2) - (LEFT.get_width() / 2), SL_POS[1] + SLOW.get_height() + 50
RIGHT = pygame.image.load("assets/turn__right.png").convert_alpha()
R_POS  = (w / 2) - (RIGHT.get_width() / 2), LE_POS[1] + LEFT.get_height() + 50
SHOOT = pygame.image.load("assets/shoot.png").convert_alpha()
SH_POS = (w /2) - (SHOOT.get_width() / 2), R_POS[1] + RIGHT.get_height() + 50

space_ships = spritesheet(space_ship_images, 6, 1, 31, 31, 2)
power_ups = spritesheet(power_up_images, 2, 1, 6, 6, 2)
enemy_data = get_all_dict("enemies.txt")
power_up_data = get_all_dict("power_ups.txt")

pygame.mixer.music.load("assets/back.wav")
pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.75)

for i, enemy in enumerate(enemy_data):
    enemy["image"] = space_ships[i + 1]

funcs = [health_boost, aim]
for i, power in enumerate(power_up_data):
    power["image"] = power_ups[i]
    power["func"] = funcs[i]

clock = pygame.time.Clock()
#ALL CAPS FOR THIS FONT EXCEPT FOR INTEGERS
font = pygame.font.Font("assets/game_font.ttf", 32)

t = "welcome to the game of shipreck. you might have a few questions on why you're fighting endless droves of enemies. well don't fear this is all the info you need. first of all the enemies goal is to crash your ship, you stole one of their prized ships, now they want you gone. next the deployers they give you nice power ups treat the deployer right and you'll be fine"

info = make_text_appear(font, t, (w - 200, B_POS[1] - 100))
shipreck = font.render("SHIPRECK", True, (255, 255, 0))
shipreck_rect = shipreck.get_rect(topleft=((w / 2) - (shipreck.get_width() / 2), 100))

def main():
    player = sprite_classes.Player(space_ships[0], win)
    deployer = sprite_classes.Deployer(deploy, power_up_data, player)
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
    menu.add_branch("setting/controls", "up", "func", SPEED, SP_POS, change_speed)
    menu.add_branch("setting/controls", "right", "func", RIGHT, R_POS, change_right)
    menu.add_branch("setting/controls", "down", "func", SLOW, SL_POS, change_slow)
    menu.add_branch("setting/controls", "left", "func", LEFT, LE_POS, change_left)
    menu.add_branch("setting/controls", "shoot", "func", SHOOT, SH_POS, change_shoot)
    menu.add_branch("setting/controls", "back", "back", BACK, (B_POS[0], B_POS[1] + 200))

    menu.add_branch("setting", "info", "button", INFO, I_POS)
    menu.add_branch("setting/info", "info", "text", info, ((w/2)-(info.get_width()/2), 200))
    menu.add_branch("setting/info", "back", "back", BACK, (B_POS[0], B_POS[1] + 100))

    menu.add_branch("setting", "back", "back", BACK, B_POS)

    menu.add_branch("", "mode", "button", MODE, M_POS)
    menu.add_branch("mode", "default", "func", DEF, D_POS, default)
    menu.add_branch("mode", "crash", "func", CRASH, CR_POS, crash)
    menu.add_branch("mode", "back", "back", BACK, B_POS)

    menu.add_branch("", "escape", "quit", ESC, E_POS)
    run = True
    while run:
        
        win.fill((0, 0, 0))

        health = font.render(f"HEALTH {player.health}", True, (255, 255, 255))
        h_rect = health.get_rect(topleft=(10, 10))
        score = font.render(f"SCORE {player.score}", True, (255, 255, 255))
        score_rect = score.get_rect(topright=(w - 10, 10))
        if player.play == "play":

            win.blit(health, h_rect)

            sprite_classes.player_bullets.update()
            sprite_classes.player_bullets.draw(win)
            
            if player.game == "default":
                win.blit(score, score_rect)
                for enemy in enemy_data:
                    en = sprite_classes.Enemy(enemy, win, player)
                    enemies.enemy_add(en)
                enemies.update()
                enemies.draw(win)
                deployer.update(win)
                deployer.draw(win)
            player.update()
            player.draw(win)
        elif player.play == "menu":
            win.blit(shipreck, shipreck_rect)
            run = menu.update(win, player)
            pygame.mixer.music.set_volume(player.vol)
            match player.game:
                case "default":
                    win.blit(DEF, DEF.get_rect(bottomright=(w,h)))
                case "crash":
                    win.blit(CRASH, CRASH.get_rect(bottomright=(w,h)))
            if menu.node.name == "controls":
                speed = font.render(pygame.key.name(player.speed_up).upper(), True, (255, 255, 255))
                sp_pos = SP_POS[0] + SPEED.get_width() + 50, 200
                slow = font.render(pygame.key.name(player.slow_down).upper(), True, (255, 255, 255))
                sl_pos = SL_POS[0] + SLOW.get_width() + 50, SL_POS[1]
                left = font.render(pygame.key.name(player.turn_left).upper(), True, (255, 255, 255))
                l_pos = LE_POS[0] + LEFT.get_width() + 50, LE_POS[1]
                right = font.render(pygame.key.name(player.turn_right).upper(), True, (255, 255, 255))
                r_pos = R_POS[0] + RIGHT.get_width() + 50, R_POS[1]
                shoot = font.render(pygame.key.name(player.shoot).upper(), True, (255, 255, 255))
                sh_pos = SH_POS[0] + SHOOT.get_width() + 50, SH_POS[1]
                win.blit(speed, sp_pos)
                win.blit(slow, sl_pos)
                win.blit(left, l_pos)
                win.blit(right, r_pos)
                win.blit(shoot, sh_pos)
        else:
            prev_sound = player.vol
            prev_mode = player.game
            prev_speed = player.speed_up
            prev_slow = player.slow_down
            prev_left = player.turn_left
            prev_right = player.turn_right
            enemies.empty()
            sprite_classes.player_bullets.empty()
            player = sprite_classes.Player(space_ships[0], win)
            deployer = sprite_classes.Deployer(deploy, power_up_data, player)
            player.play = "menu"
            player.vol = prev_sound
            player.game = prev_mode
            player.speed_up = prev_speed
            player.slow_down = prev_slow
            player.turn_left = prev_left
            player.turn_right = prev_right
            menu.starting_point()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if player.change_speed:
                    player.speed_up = event.key
                    player.change_speed = False
                if player.change_slow:
                    player.slow_down = event.key
                    player.change_slow = False
                if player.change_left:
                    player.turn_left = event.key
                    player.change_left = False
                if player.change_right:
                    player.turn_right = event.key
                    player.change_right = False
                if player.change_shoot:
                    player.shoot = event.key
                    player.change_shoot = False

if __name__ == "__main__":
    main()
pygame.mixer.music.unload()
pygame.quit()