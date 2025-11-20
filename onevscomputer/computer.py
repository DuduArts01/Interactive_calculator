import pygame
from mainImages import MainControlImages
from button.button import Button
from font.font_edit import Font
from onevscomputer.logic import Logic_calculator
from time import sleep
from nfc.nfc_game_interface_on_demand import NFCGameInterface
from background.background import Background
from title.title import Title
from onevscomputer.timer import Timer  

class Game_computer:
    def __init__(self, screen):
        self.screen = screen
        self.fullscreen = False
        self.image_1vC_data = MainControlImages.send_imag_image_data
        self.PVsComputerTitle_image_data = MainControlImages.PVsComputerTitle_image_data
        self.resizedElements()

        self.nfc = NFCGameInterface("nfc/uids.json")

        self.operation_and_random = True
        self.background_green = Background(self.screen)

        self.score = 0  # contador de acertos
        self.timer = Timer(60)  # <<--- cronômetro de 1 minuto

        self.back_img = pygame.image.load("data/icon/arrow_back.png").convert_alpha()
        self.back_img = pygame.transform.scale(self.back_img, (40, 40))  # tamanho da seta

        self.back_rect = self.back_img.get_rect()
        self.back_rect.topleft = (20, 10)  # posição no canto superior esquerdo


    def resizedElements(self):
        width, height = self.screen.get_size()
        self.width = width
        self.height = height
        base_width = 800
        base_height = 480
        scale_x = width / base_width
        scale_y = height / base_height
        scale_factor = min(scale_x, scale_y) * 8

        self.PVsComputerTitle = Title(
            self.PVsComputerTitle_image_data["image"],
            x=width / 2,
            y=height - (height / 1.15),
            width=self.PVsComputerTitle_image_data["resize_x"],
            height=self.PVsComputerTitle_image_data["resize_y"]
        )

        self.send = Button(
            self.image_1vC_data["image"],
            x=width / 2,
            y=height - (height / 8),
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
            self.background_green.draw()
            pygame.display.set_caption("Calculadora Interativa (1 Vs Computer)")

            # Atualiza cronômetro
            remaining = self.timer.update()

            # Se o tempo acabar
            if remaining <= 0:
                self.background_green.draw()
                final_msg = Font(f"Tempo esgotado!", "Arial", 60)
                final_msg.draw(self.screen, y=self.height / 2.3)

                pygame.display.update()
                sleep(2)

                # mostra total de acertos
                self.background_green.draw()
                score_msg = Font(f"Total de Acertos: {self.score}", "Arial", 60)
                score_msg.draw(self.screen, y=self.height / 2.3)
                pygame.display.update()
                sleep(2)

                running = False
                next_screen = "gameselect"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    next_screen = None

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
                        next_screen = "gameselect"


            answer_user = None

            if self.operation_and_random:
                logic = Logic_calculator()
                logic.randomNumber()
                operator = logic.choose_operator()

                self.NumbershowScreen = Font(f"{logic.n1} {operator} {logic.n2} = ?", "Arial", 60)
            
            self.operation_and_random = False

            # BOTÃO DE ENVIAR
            if self.send.action:
                self.send.draw(self.screen)
                pygame.display.update()
                pygame.time.delay(250)

                # Pausar o cronômetro antes de mostrar qualquer feedback
                self.timer.pause()

                
                ten, unit, total = self.nfc.read_once()
                answer_user = total
                

                # ----------- RESULTADOS -------------
                if answer_user == logic.correct_answer:
                    # ACERTO → +5s e próxima questão
                    self.score += 1
                    self.timer.add_time(5)
                
                    # retoma o tempo antes da nova questão
                    self.timer.resume()
                
                    self.operation_and_random = True
                
                else:
                    # ERRO - mensagem em tela
                    self.background_green.draw()
                    self.PVsComputerTitle.draw(self.screen)
                    error_msg = Font("Você errou! Tente novamente!", "Arial", 60)
                    error_msg.draw(self.screen, y=self.height / 2.2)
                    pygame.display.update()
                    sleep(2)
                
                    # total de acertos final
                    self.background_green.draw()
                    total_msg = Font(f"Total de Acertos: {self.score}", "Arial", 60)
                    total_msg.draw(self.screen, y=self.height / 2.2)
                    pygame.display.update()
                    sleep(2)
                
                    running = False
                    next_screen = "gameselect"
                
                self.timer.resume()
                self.operation_and_random = True


            # --- DESENHO DE TELA ---
            self.PVsComputerTitle.draw(self.screen)
            self.NumbershowScreen.draw(self.screen, y=self.height / 2.5)
            self.send.draw(self.screen)

            self.screen.blit(self.back_img, self.back_rect)


            # Contador de acertos
            score_text = Font(f"Acertos: {self.score}", "Arial", 30)
            score_text.draw(self.screen, x=self.width / 20, y=self.height / 9)

            # Cronômetro no canto superior direito
            timer_text = Font(self.timer.get_time_string(), "Arial", 30)
            timer_text.draw(self.screen, x=self.width - 150, y=self.height / 9)

            pygame.display.update()

        # ENCERRAR NFC AO SAIR
        self.nfc.close()

        return next_screen
