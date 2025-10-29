import pygame
from mainImages import MainControlImages
from button.button import Button
from font.font_edit import Font
from onevscomputer.logic import Logic_calculator
from time import sleep
from nfc.nfc_game_interface_on_demand import NFCGameInterface

class Game_computer:
    def __init__(self, screen):
        self.screen = screen
        self.fullscreen = False
        self.image_1vC_data = MainControlImages.sprite_1vComputer_image_data
        self.resizedElements()
        self.nfc = NFCGameInterface("uids.json")

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


        self.title = Font("1 Vs Computer", "Arial", 60, (0,0,0)) #Title Game

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
            pygame.display.set_caption("Calculadora Interativa (1 Vs Computer)")

            self.title = Font(f"Player vs Computer", "Arial", 60, (0,0,0)) #Title Game

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

            '''Call the functions logic game'''
            logic = Logic_calculator() # Call the class
            logic.randomNumber() # Computer random two numbers
            operator = logic.choose_operator() # symbols operator: + - * /

            answer_user = None

            # Show operation on screen
            self.NumbershowScreen = Font(f"{logic.n1} {operator} {logic.n2} = ?", "Arial", 60, (0,0,0)) #Title Game

            '''Button action'''
            # Verifica se o botão foi clicado
            if self.onevsComputer.action:
                self.onevsComputer.draw(self.screen)         # Mostra imagem clicada
                pygame.display.update()                    # Atualiza tela
                pygame.time.delay(150)                     # Delay de 150ms
                
                # no loop do pygame, no evento do botão "Enviar":
                # quando o jogador clicar em enviar:
                ten, unit, total = self.nfc.read_once()
                print("Leitura ao enviar -> dezena:", ten, "unidade:", unit, "total:", total)

            # Draw title (show on screen)
            self.title.draw(self.screen, y=100)  # Draw center title

            # Draw operation (show on screen)
            self.NumbershowScreen.draw(self.screen, y=300)

            # Draw buttons (show on screen)
            self.onevsComputer.draw(self.screen) # Button one vs computer
            
            pygame.display.update()

            '''In this block it will be replaced by NFC '''
            # Test in terminal
            answer_user = int(input(f"Quanto é {logic.n1} {operator} {logic.n2}?\n")) # input value of User

            print(logic.checknumber(answer_user)) # Check answer User
            
            '''Show result'''
            if answer_user != None:
                # Clean screen
                self.screen.fill((255, 255, 255))

                # Keeps the title on the screen
                self.title = Font(f"Player vs Computer", "Arial", 60, (0,0,0)) #Title Game

                # Show result on screen
                self.result = Font(f"{logic.checknumber(answer_user)}", "Arial", 60, (0,0,0)) #Title Game

                # Title Show
                self.title.draw(self.screen, y = 100)

                # Result Show
                self.result.draw(self.screen, y = 300)

                pygame.display.update()

                sleep(2) # Wait 2 seconds to update screen again
        
        # ao finalizar o jogo:
        self.nfc.close()

        return next_screen