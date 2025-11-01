import pygame

import pygame

class Title(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width=None, height=None, scale_factor=1.0):
        super().__init__()

        img_width, img_height = image.get_size()

        # Usa os valores de redimensionamento se forem fornecidos
        if width is not None and height is not None:
            new_width = int(width)
            new_height = int(height)
        else:
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)

        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

