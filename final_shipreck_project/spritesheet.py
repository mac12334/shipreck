import pygame

pygame.init()

def spritesheet(surface: pygame.Surface, rows: int, cols: int, width: int, height: int, scale: float) -> list[pygame.Surface]:
    images = []
    for y in range(rows):
        for x in range(cols):
            image = pygame.Surface((width, height))
            image.blit(surface, (-width * x, -height * y))
            image = pygame.transform.scale(image, (width * scale, height * scale))
            image.set_colorkey((0, 0, 0))
            images.append(image)
    return images