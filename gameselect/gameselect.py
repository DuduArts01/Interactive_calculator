import pygame
from mainImages import MainControlImages
from button.button import Button
from font.font_edit import Font

class Select_Mode:
    def __init__(self, screen):
        self.screen = screen
        self.fullscreen = False
        self.image_1vC_data = MainControlImages.sprite_1vComputer_image_data
        self.resizedElements()

    def resizedElements(self):
        width, height = self.screen.get_size()
        base_width = 1280
        base_height = 720
        scale_x = width / base_width
        scale_y = height / base_height
        scale_factor = min(scale_x, scale_y) * 8

        self.onevsComputer = Button(
            self.image_1vC_data["image"],
            x=width / 3,
            y=height - (height / 5),
            scale_factor=scale_factor
        )


        self.title = Font("Selecione o modo de jogo", "Arial", 60, (0,0,0)) #Title Game

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
            pygame.display.set_caption("Calculadora Interativa (Selecionar Modo de Jogo)")

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

            # Verifica se o botão foi clicado
            if self.onevsComputer.action:
                self.onevsComputer.draw(self.screen)         # Mostra imagem clicada
                pygame.display.update()                    # Atualiza tela
                pygame.time.delay(150)                     # Delay de 150ms
                running = False
                next_screen = "computergame"                      # Troca para tela 1vComputer

            # Draw title (show on screen)
            self.title.draw(self.screen, y=100)  # Draw center title

            # Draw buttons (show on screen)
            self.onevsComputer.draw(self.screen) # Button one vs computer
            
            pygame.display.update()

        return next_screen