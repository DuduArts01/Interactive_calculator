import pygame
from mainImages import MainControlImages
from button.button import Button
from font.font_edit import Font

class MainMenuProgram:
    def __init__(self, screen):
        self.screen = screen
        self.fullscreen = False
        self.image_data = MainControlImages.start_image_data
        self.resizedElements()

    def resizedElements(self):
        width, height = self.screen.get_size()
        base_width = 1280
        base_height = 720
        scale_x = width / base_width
        scale_y = height / base_height
        scale_factor = min(scale_x, scale_y) * 8

        self.start_button = Button(
            self.image_data["image"],
            x=width / 2,
            y=height - (height / 5),
            scale_factor=scale_factor
        )


        self.title = Font("Calculador Interativa", "Arial", 60, (0,0,0)) #Title Game

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.resizedElements()

    def run(self):
        running = True
        next_screen = None

        while running:
            self.screen.fill((255, 255, 255))
            pygame.display.set_caption("Calculadora Interativa (MAIN MENU)")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    next_screen = None  # Encerra o jogo

                elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    width, height = event.size
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self.resizedElements()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()

            '''Button action'''
            if self.start_button.action:
                self.start_button.draw(self.screen)         # Mostra imagem clicada
                pygame.display.update()                    # Atualiza tela
                pygame.time.delay(150)                     # Delay de 150ms
                running = False
                next_screen = "gameselect"                      # Troca para tela da loja

            # Draw Title (show on screen)
            self.title.draw(self.screen, y=100)  # Draw center title

            # Draw button (show on screen)
            self.start_button.draw(self.screen) # Button Start
            
            pygame.display.flip()

        return next_screen