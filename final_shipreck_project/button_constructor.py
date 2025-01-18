import pygame

pygame.init()

win = pygame.display.set_mode((200, 200))

left = pygame.image.load("assets/left.png").convert_alpha()
middle = pygame.image.load("assets/middle.png").convert_alpha()
right = pygame.image.load("assets/right.png").convert_alpha()

font = pygame.font.Font("assets/game_font.ttf", 32)

text = str(input("what text do you want? "))

rend = font.render(text, True, (255, 255, 0))
pixel_size = rend.get_height() // 11
rh = rend.get_height() + (pixel_size * 7)
left = pygame.transform.scale(left, (rh + pixel_size, rh))
middle = pygame.transform.scale(middle, (rend.get_width(), rh))
right = pygame.transform.scale(right, (rh + pixel_size, rh))

x_dis = -14 * pixel_size
y_dis = (-2 * pixel_size) - (pixel_size * 0.11)

mid_x = left.get_width() + x_dis
r_x = ((middle.get_width() / 2) + mid_x) - (rend.get_width() / 2)
r_y = ((middle.get_height() / 2) + y_dis) - (rend.get_height() / 2)

run = True
save = False
while run:

    k = pygame.key.get_pressed()
    if k[pygame.K_y]:
        run = False
        save = True
    if k[pygame.K_n]:
        run = False

    win.fill((255, 255, 255))

    win.blit(left, (x_dis, y_dis))
    win.blit(middle, (left.get_width() + x_dis, y_dis))
    win.blit(right, (middle.get_width() + left.get_width() + x_dis, y_dis))
    win.blit(rend, (r_x, r_y))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

def make_surf(size_cordinates: tuple[int | float, int | float]) -> pygame.Surface:
    surf = pygame.Surface(size_cordinates)
    surf.fill((255, 255, 255))

    surf.blit(left, (x_dis, y_dis))
    surf.blit(middle, (left.get_width() + x_dis, y_dis))
    surf.blit(right, (middle.get_width() + left.get_width() + x_dis, y_dis))
    surf.blit(rend, (r_x, r_y))

    surf.set_colorkey((255, 255, 255))

    return surf.convert_alpha()

s = make_surf(((rh * 2) + middle.get_width() - (pixel_size * 26), rh - (pixel_size * 3)))

if save:
    pygame.image.save(s, "assets/" + text.lower() + ".png")
pygame.quit()