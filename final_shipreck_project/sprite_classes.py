import pygame, math, random
from typing import Self

pygame.init()
player_bullets = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, screen: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.o_image = image
        self.image = image
        self.pos = (screen.get_width() / 2, screen.get_height() / 2)
        self.rect = self.image.get_rect(center = self.pos)
        self.screen = screen

        self.angle = 0
        self.speed = 2.5

        self.can_shoot = True
        self.wait_over = True
        self.last_update = pygame.time.get_ticks()
        self.level = 0
        self.health = 100
        self.max_health = 100
        self.mask_image = None

        self.play = "menu"
        self.vol = 0.66
        self.high_vol = 1
        self.norm_vol = 0.66
        self.low_vol = 0.33

        # controls
        self.speed_up = pygame.K_UP
        self.turn_left = pygame.K_LEFT
        self.turn_right = pygame.K_RIGHT
        self.slow_down = pygame.K_DOWN
        self.shoot = pygame.K_SPACE
    
    def waiting(self, should_wait: bool) -> None:
        if should_wait:
            self.last_update = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= 375 and not self.wait_over:
            self.wait_over = True
    
    def movement(self):
        k = pygame.key.get_pressed()
        if not k[self.shoot]:
            self.can_shoot = True

        if k[self.turn_left]:
            self.angle += 2
        if k[self.turn_right]:
            self.angle -= 2
        if k[self.speed_up] and self.speed < 5:
            self.speed += 0.1
        if k[self.slow_down] and self.speed > 0:
            self.speed -= 0.1
        if k[pygame.K_ESCAPE]:
            self.play = "else"

        #movement forward
        rad_angle = math.radians(self.angle)
        dx = math.cos(rad_angle) * self.speed
        dy = math.sin(rad_angle) * self.speed
        self.pos = (self.pos[0] + dx, self.pos[1] - dy)

        if k[self.shoot] and self.can_shoot and self.wait_over:
            bullet = Bullet(self.angle, self.pos, self.screen)
            player_bullets.add(bullet)
            self.can_shoot = False
            self.wait_over = False
            self.waiting(True)
    
    def screen_wrapping(self):
        x, y = self.pos
        x = x % self.screen.get_width()
        y = y % self.screen.get_height()
        self.pos = x, y
    
    def get_color(self) -> None:
        t = self.health / self.max_health
        r = 255 * (1 - t)
        g = 255 * t
        mask = pygame.mask.from_surface(self.image)
        self.mask_image = mask.to_surface(setcolor=(r, g, 0, 100), unsetcolor=(0, 0, 0, 0))
        
    def update(self) -> None:
        if self.health <= 0:
            self.play = "else"
        self.image = pygame.transform.rotate(self.o_image, self.angle - 90)
        self.rect = self.image.get_rect(center = self.pos)
        self.movement()
        self.waiting(False)
        self.screen_wrapping()
        if self.health != self.max_health:
            self.get_color()
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        if self.mask_image != None:
            screen.blit(self.mask_image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle: int | float, pos: tuple[int, int], screen: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.pos = pos
        img = pygame.image.load("assets/bullet.png").convert_alpha()
        img = pygame.transform.scale(img, (62,62))
        self.image = pygame.transform.rotate(img, self.angle - 90)
        self.rect = self.image.get_rect(center=self.pos)
        self.screen = screen
        self.has_hit: list = []
    
    def move(self) -> None:
        rad = math.radians(self.angle)
        x = math.cos(rad) * 10
        y = math.sin(rad) * 10
        self.pos = self.pos[0] + x, self.pos[1] - y
    
    def off_screen(self) -> None:
        x, y = self.pos
        width, height = self.screen.get_width(), self.screen.get_height()
        if not (0 < x < width) and not (0 < y < height) and self.alive():
            self.kill()
    
    def update(self) -> None:
        self.move()
        self.rect.center = self.pos
        self.off_screen()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, attr: dict[str, any], screen: pygame.Surface, client: Player) -> None:
        pygame.sprite.Sprite.__init__(self)
        if "name" in attr:
            self.name: str = attr["name"]
        if "image" in attr:
            self.image: pygame.Surface = attr["image"]
        if "speed" in attr:
            self.speed: int = attr["speed"]
            self.o_speed = self.speed
        if "health" in attr:
            self.health: int = attr["health"]
        if "max" in attr:
            self.max: int = attr["max"]
        if "level" in attr:
            self.level: int = attr["level"]
        if "damage" in attr:
            self.damage: int = attr["damage"]

        self.o_image = self.image
        self.max_health = self.health
        self.radius = 25

        self.pos = random.randint(31, screen.get_width() - 31), random.randint(31, screen.get_height() - 31)
        self.rect = self.image.get_rect(center=self.pos)

        self.client = client
        self.angle = 0

        self.mask_image = None
    
    def find_angle(self) -> None:
        sx, sy = self.pos
        cx, cy = self.client.pos
        x = cx - sx
        y = cy - sy
        rad = math.atan2(-y, x)
        self.angle = math.degrees(rad)
    
    def player_col(self) -> None:
        if pygame.sprite.collide_mask(self, self.client) and self.alive():
            self.client.health -= self.damage
            self.kill()

    def bullet_col(self) -> None:
        collided = pygame.sprite.spritecollide(self, player_bullets, False, pygame.sprite.collide_mask)
        for col in collided:
            if not (self in col.has_hit):
                self.health -= 10
                col.has_hit.append(self)
    
    def move(self) -> None:
        rad_angle = math.radians(self.angle)
        dx = float(math.cos(rad_angle)) * self.speed
        dy = float(math.sin(rad_angle)) * self.speed
        self.pos = (self.pos[0] + dx, self.pos[1] - dy)
    
    def get_color(self) -> None:
        t = self.health / self.max_health
        r = 255 * (1 - t)
        g = 255 * (t)
        mask = pygame.mask.from_surface(self.image)
        self.mask_image = mask.to_surface(setcolor=(r, g, 0, 50),unsetcolor=(0, 0, 0, 0))
    
    def collide_other(self) -> None:
        has_collided = False
        groups = self.groups()
        for group in groups:
            for sprite in group.sprites():
                if sprite != self:
                    if pygame.sprite.collide_circle(self, sprite):
                        self.collided(sprite)
                        has_collided = True
        if not has_collided:
            self.speed = self.o_speed

    def collided(self, other: Self) -> None:
        # unpacks their respective x and y coordinates
        sx, sy = self.pos
        ox, oy = other.pos
        # gets distance between the two points
        dx = abs(sx - ox)
        dy = abs(sy - oy)
        d = math.sqrt(dx**2 + dy**2)
        # x is the max overlap between the two circles s is the intended distance between them
        s = self.radius + other.radius
        x = s - d
        # getting the angle using tangent
        angle = math.atan2(dy, dx)
        disx = math.sin(angle) * x
        disy = math.cos(angle) * x

        #aplies the changes to the position so that the circles don't overlap
        self.pos = self.pos[0] + (disx / 2), self.pos[1] + (disy / 2)
        other.pos = other.pos[0] + (-disx / 2), other.pos[1] + (-disy / 2)
        
        self.speed = self.o_speed + 1
        other.speed = other.o_speed - 1
        
    
    def update(self) -> None:
        if self.health <= 0:
            self.kill()
        self.find_angle()
        self.move()
        self.image = pygame.transform.rotate(self.o_image, self.angle - 90)
        self.rect = self.image.get_rect(center = self.pos)
        self.player_col()
        self.bullet_col()
        self.collide_other()
        if self.health != self.max_health:
            self.get_color()

class EnemyGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        pygame.sprite.Group.__init__(self)
    
    def enemy_add(self, enemy: Enemy) -> None:
        level = enemy.level
        m = enemy.max
        name = enemy.name
        num = 0
        for sprite in self.sprites():
            if sprite.name == name:
                num += 1
        if num < m and level <= enemy.client.level:
            self.add(enemy)
    
    def draw(self, screen: pygame.Surface) -> None:
        for sprite in self.sprites():
            screen.blit(sprite.image, sprite.rect)
            if sprite.mask_image != None:
                screen.blit(sprite.mask_image, sprite.rect)