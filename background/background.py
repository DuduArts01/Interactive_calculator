import pygame
import math

class Background:
    def __init__(self, screen, center_color=(0, 90, 80), edge_color=(10, 40, 35)):
        self.screen = screen
        self.center_color = center_color
        self.edge_color = edge_color

    def draw(self):
        width, height = self.screen.get_size()
        center_x, center_y = width // 2, height // 2
        max_radius = math.hypot(center_x, center_y)

        for i in range(int(max_radius), 0, -2):
            t = i / max_radius
            r = int(self.center_color[0] * t + self.edge_color[0] * (1 - t))
            g = int(self.center_color[1] * t + self.edge_color[1] * (1 - t))
            b = int(self.center_color[2] * t + self.edge_color[2] * (1 - t))
            pygame.draw.circle(self.screen, (r, g, b), (center_x, center_y), i)
