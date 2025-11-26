import pygame
from mainImages import MainControlImages
from button.button import Button
from background.background import Background
from title.title import Title

class Select_Mode:
    def __init__(self, screen):
        self.screen = screen
        self.fullscreen = False
        self.sprite_1vComputer_image_data = MainControlImages.sprite_1vComputer_image_data
        self.selectmode_image_data = MainControlImages.selectmode_image_data
        self.resizedElements()

        self.background_green = Background(self.screen)

        # Back arrow
        self.back_img = pygame.image.load("data/icon/arrow_back.png").convert_alpha()
        self.back_img = pygame.transform.scale(self.back_img, (40, 40))  # tamanho da seta

        self.back_rect = self.back_img.get_rect()
        self.back_rect.topleft = (20, 10)  # posição no canto superior esquerdo

    def resizedElements(self):
        width, height = self.screen.get_size()
        base_width = 800
        base_height = 480
        scale_x = width / base_width
        scale_y = height / base_height
        scale_factor = min(scale_x, scale_y) * 8

        self.selectmode = Title(
            self.selectmode_image_data["image"],
            x=width / 2,
            y=height - (height / 1.25),
            width= self.selectmode_image_data["resize_x"],
            height= self.selectmode_image_data["resize_y"]
        )

        self.onevsComputer = Button(
            self.sprite_1vComputer_image_data["image"],
            x=width / 2,
            y=height - (height / 4),
            scale_factor=scale_factor / 20
        )

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 480), pygame.RESIZABLE)
        self.resizedElements()

    def run(self):
        running = True
        next_screen = None

        while running:
            # Draw green background
            self.background_green.draw()

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

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_rect.collidepoint(event.pos):
                        pygame.time.delay(150)  # pequeno delay opcional
                        running = False
                        next_screen = "menu"

            '''Button action'''            
            if self.onevsComputer.action:
                self.onevsComputer.draw(self.screen)         # Mostra imagem clicada
                pygame.display.update()                    # Atualiza tela
                pygame.time.delay(250)                     # Delay de 150ms
                running = False
                next_screen = "computergame"                      # Troca para tela 1vComputer

            # Draw buttons (show on screen)
            self.onevsComputer.draw(self.screen) # Button one vs computer

            # Draw title (show on screen)
            self.selectmode.draw(self.screen)  # Draw center title

            self.screen.blit(self.back_img, self.back_rect)

            pygame.display.update()

        return next_screen