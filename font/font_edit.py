import pygame

class Font:
    def __init__(self, text, font_name, font_size, color=(255, 255, 255)):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.rendered_text = self.font.render(self.text, True, self.color)

    def draw(self, surface, x=None, y=None):
        """
        Draws the title.
        If x or y is None, that axis is centered.
        """
        screen_width, screen_height = surface.get_size()
        text_rect = self.rendered_text.get_rect()

        # Set position: use given x/y or center
        text_rect.x = x if x is not None else (screen_width - text_rect.width) // 2
        text_rect.y = y if y is not None else (screen_height - text_rect.height) // 2

        surface.blit(self.rendered_text, text_rect)