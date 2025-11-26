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
    # --- CONSTANTES DE ESTADO ---
    WAITING_FOR_CARD = 0
    CARD_DETECTED = 1
    WAITING_FOR_REMOVAL = 2

    def __init__(self, screen):
        self.screen = screen
        self.fullscreen = False
        self.image_1vC_data = MainControlImages.send_imag_image_data
        self.PVsComputerTitle_image_data = MainControlImages.PVsComputerTitle_image_data
        self.resizedElements()

        self.nfc = NFCGameInterface("nfc/uids.json")
        self.logic = Logic_calculator()
        
        # Flag inicializada como True para gerar a PRIMEIRA pergunta
        self.operation_and_random = True 
        
        self.background_green = Background(self.screen)
        self.score = 0
        self.timer = Timer(60)

        # --- NOVOS ESTADOS E VARIÁVEIS DE CONTROLE ---
        self.game_state = self.WAITING_FOR_CARD # Estado inicial
        self.current_card_number = -1 
        self.last_card_read = -1 
        
        # Variável para controlar se o botão Enviar foi clicado NESTE frame
        self.send_clicked = False 
        # Variável para controlar o tempo de espera da tela de remoção
        self.removal_start_time = 0

        self.back_img = pygame.image.load("data/icon/arrow_back.png").convert_alpha()
        self.back_img = pygame.transform.scale(self.back_img, (40, 40))
        self.back_rect = self.back_img.get_rect()
        self.back_rect.topleft = (20, 10)

        self.NumbershowScreen = Font("", "Arial", 60)
        self.statusMessage = Font("Insira o cartão de respostas!", "Arial", 40, color=(255, 0, 0)) # Mensagem inicial em vermelho

    def resizedElements(self):
        # ... (Seu código original de redimensionamento) ...
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
        # ... (Seu código original de fullscreen) ...
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 480), pygame.RESIZABLE)
        self.resizedElements()

    def handle_nfc_status(self):
        """
        Gerencia os estados WAITING_FOR_CARD e CARD_DETECTED.
        Corrige o bug de leitura intermitente.
        Retorna o número do cartão lido ou -1.
        """
        # Tenta ler o cartão.
        ten, unit, total = self.nfc.read_once() 
        
        if self.game_state == self.WAITING_FOR_REMOVAL:
            # Se estamos esperando a remoção, ignoramos todas as leituras,
            # exceto se o cartão for removido (total == -1), mas isso será 
            # tratado no loop principal após o delay (sleep).
            return self.current_card_number

        # --- Lógica de Cartão