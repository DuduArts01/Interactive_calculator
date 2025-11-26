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
        CORRIGIDO: A leitura estável é mantida mesmo com leituras intermitentes de falha.
        Retorna o número do cartão lido ou -1.
        """
        # Tenta ler o cartão.
        ten, unit, total = self.nfc.read_once() 
        
        if self.game_state == self.WAITING_FOR_REMOVAL:
            # Não fazemos nada com a leitura enquanto esperamos a remoção
            return self.current_card_number

        # --- Lógica de Cartão Detectado/Inserido (total >= 0) ---
        if total >= 0:
            # Se a leitura foi bem sucedida, atualiza o estado e o número.
            # Se o estado atual era WAITING_FOR_CARD, ou se o cartão mudou, atualiza.
            if self.game_state == self.WAITING_FOR_CARD or total != self.current_card_number:
                self.game_state = self.CARD_DETECTED
                self.current_card_number = total
                self.statusMessage = Font(f"Sensor: {total}", "Arial", 40, color=(0, 200, 0)) # Verde
                self.last_card_read = total # Marca a última leitura estável
            
            # Se a leitura for bem sucedida E for o mesmo cartão, mantemos o estado e o número.
        
        # --- Lógica de Cartão Removido/Leitura Falha (total == -1) ---
        else: 
            # Se estamos no estado CARD_DETECTED E a leitura falhou,
            # consideramos que o cartão foi removido.
            # NOTA: Com esta alteração, leituras instáveis (0 -> -1 -> 0)
            # farão com que o statusMessage mude brevemente para "Insira o cartão...",
            # mas a próxima leitura de 0-9 (que é rápida) o trará de volta para CARD_DETECTED
            # e atualizará a mensagem. A correção de fato é o delay de 0.5s no botão 'send'
            # para capturar a leitura estável.
            if self.game_state == self.CARD_DETECTED:
                # Cartão removido (ou leitura falha persistente)
                self.game_state = self.WAITING_FOR_CARD
                self.current_card_number = -1
                self.statusMessage = Font("Insira o cartão de respostas!", "Arial", 40, color=(255, 0, 0)) # Vermelho
        
        return self.current_card_number

    def show_card_removal_screen(self, screen):
        """
        Desenha a tela de "Retirar Cartão" e pausa por 2 segundos (tempo fixo para evitar travamento).
        """
        self.timer.pause()
        
        # Desenha a mensagem de "Retirar Cartão"
        self.background_green.draw()
        self.PVsComputerTitle.draw(screen)
        removal_msg = Font("Retire o cartão para continuar...", "Arial", 40, color=(255, 165, 0)) # Laranja
        removal_msg.draw(screen, y=self.height / 2.5)
        pygame.display.update()
        
        sleep(2) # A tela fica visível por 2 segundos
        
        # Processa eventos básicos do Pygame para evitar 'Not Responding' durante o sleep
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.nfc.close()
                return None
        
        return True

    def process_send_action(self, next_screen):
        """
        Lógica de processamento da resposta do usuário.
        """
        self.timer.pause()
        answer_user = self.current_card_number
        
        # --- PROCESSAMENTO DA RESPOSTA ---
        if self.logic.is_correct(answer_user):
            # ACERTO
            self.score += 1
            self.timer.add_time(5)
            self.operation_and_random = True # Próxima questão
            
            # Exibe mensagem de acerto
            self.background_green.draw()
            success_msg = Font("ACERTOU! +5 segundos", "Arial", 60)
            success_msg.draw(self.screen, y=self.height / 2.2)
            pygame.display.update()
            sleep(1) # Delay para mensagem de acerto
            
            # Próximo estado: Espera a remoção do cartão
            self.game_state = self.WAITING_FOR_REMOVAL
            return None # Continua o jogo (mas vai para a tela de remoção)
            
        else:
            # ERRO - FIM DE JOGO
            self.background_green.draw()
            error_msg = Font(f"Você errou! A resposta era: {self.logic.get_correct_answer()}", "Arial", 40)
            error_msg.draw(self.screen, y=self.height / 2.2)
            pygame.display.update()
            sleep(2)

            self.background_green.draw()
            total_msg = Font(f"Total de Acertos: {self.score}", "Arial", 60)
            total_msg.draw(self.screen, y=self.height / 2.2)
            pygame.display.update()
            sleep(2)
            
            # Próximo estado: Espera a remoção do cartão (FIM DE JOGO)
            self.game_state = self.WAITING_FOR_REMOVAL
            return "gameselect" # Define a tela de destino (FIM DE JOGO)

    def run(self):
        """
        Loop principal da tela Game_computer.
        """
        running = True
        next_screen = None

        while running:
            self.background_green.draw()
            pygame.display.set_caption("Calculadora Interativa (1 Vs Computer)")
            
            # 1. Geração de Pergunta
            if self.operation_and_random:
                operator = self.logic.choose_operator()
                self.NumbershowScreen = Font(f"{self.logic.n1} {operator} {self.logic.n2} = ?", "Arial", 60)
                self.operation_and_random = False 

            # 2. Atualiza estados do NFC
            self.handle_nfc_status()

            # --- Lógica de Transição de Remoção (Tempo Fixo) ---
            if self.game_state == self.WAITING_FOR_REMOVAL:
                next_screen_after_removal = next_screen # Salva a tela de destino (gameselect ou None)
                
                # Chama a tela de remoção que fará o sleep(2)
                result = self.show_card_removal_screen(self.screen)
                
                if result is None: # Se o usuário fechou o Pygame durante o sleep
                    running = False
                    next_screen = None
                    continue

                # Após o sleep, volta para WAITING_FOR_CARD
                self.game_state = self.WAITING_FOR_CARD
                self.current_card_number = -1
                self.statusMessage = Font("Insira o cartão de respostas!", "Arial", 40, color=(255, 0, 0))
                self.timer.resume() # Retoma o timer

                # Se a próxima tela for "gameselect" (FIM DE JOGO), encerra o loop principal
                if next_screen_after_removal == "gameselect":
                    running = False
                    next_screen = "gameselect"
                
                continue # Volta ao topo para redesenhar a tela principal/finalizar

            # 3. Lógica de Fim de Jogo (Tempo Esgotado)
            remaining = self.timer.update()
            if remaining <= 0:
                # Transiciona para espera de remoção e fim de jogo
                self.game_state = self.WAITING_FOR_REMOVAL
                next_screen = "gameselect"
                continue # Volta ao topo do loop para processar o WAITING_FOR_REMOVAL

            # 4. Gerenciamento de Eventos (Teclado, Mouse, Seta de Voltar, Botão Enviar)
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
                        pygame.time.delay(150)
                        running = False
                        next_screen = "gameselect"
                    
                    # 5. BOTÃO DE ENVIAR (Verifica o clique no loop de eventos)
                    if self.game_state == self.CARD_DETECTED:
                        if self.send.rect.collidepoint(event.pos):
                            # Desenha o botão pressionado
                            self.send.draw(self.screen)
                            pygame.display.update()
                            
                            # O delay de 0.5s é CRUCIAL para capturar a leitura estável do sensor
                            sleep(0.5) 
                            
                            # Processa a resposta (Acerto/Erro) e define o próximo estado/tela
                            next_screen = self.process_send_action(next_screen)
                            
                            # Se o estado mudou para WAITING_FOR_REMOVAL, o próximo ciclo do
                            # loop principal processará a tela de remoção.
                            if self.game_state == self.WAITING_FOR_REMOVAL:
                                break

                    elif self.game_state == self.WAITING_FOR_CARD:
                        if self.send.rect.collidepoint(event.pos):
                             # Se pressionar o botão em WAITING_FOR_CARD
                            self.statusMessage = Font("Insira o cartão antes de enviar!", "Arial", 40, color=(255, 0, 0))

            # 6. --- DESENHO DE TELA ---
            self.PVsComputerTitle.draw(self.screen)
            self.NumbershowScreen.draw(self.screen, y=self.height / 2.5)
            
            # Desenha a mensagem de status (Insira/Sensor: X)
            if self.game_state != self.WAITING_FOR_REMOVAL:
                self.statusMessage.draw(self.screen, y=self.height / 1.7)
            
            # Desenha o botão de enviar.
            self.send.draw(self.screen) 

            self.screen.blit(self.back_img, self.back_rect)

            # Contador de acertos
            score_text = Font(f"Acertos: {self.score}", "Arial", 30)
            score_text.draw(self.screen, x=self.width / 20, y=self.height / 9)

            # Cronômetro
            timer_text = Font(self.timer.get_time_string(), "Arial", 30)
            timer_text.draw(self.screen, x=self.width - 150, y=self.height / 9)

            pygame.display.update()

        # ENCERRAR NFC AO SAIR
        self.nfc.close()
        return next_screen