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
        Retorna o número do cartão lido ou -1.
        """
        # Tenta ler o cartão. Assume que nfc.read_once() não bloqueia e retorna (-1,-1,-1) se falhar.
        # Estamos interessados apenas no 'total' (o número decimal 0-9).
        ten, unit, total = self.nfc.read_once() 
        
        # Mapeia o resultado do NFC para o estado do jogo
        if total >= 0:
            # Cartão detectado (0 a 9)
            if self.game_state == self.WAITING_FOR_CARD:
                self.game_state = self.CARD_DETECTED
                self.current_card_number = total
                self.statusMessage = Font(f"Sensor: {total}", "Arial", 40, color=(0, 200, 0)) # Verde
            elif self.game_state == self.CARD_DETECTED and total != self.current_card_number:
                # O cartão mudou enquanto o jogo estava pronto para enviar
                self.current_card_number = total
                self.statusMessage = Font(f"Sensor: {total}", "Arial", 40, color=(0, 200, 0)) # Atualiza mensagem
            
        else: # total == -1 (Nenhum cartão válido ou cartão removido)
            if self.game_state == self.CARD_DETECTED:
                # Cartão removido antes de enviar (Opção 2)
                self.game_state = self.WAITING_FOR_CARD
                self.current_card_number = -1
                self.statusMessage = Font("Insira o cartão de respostas!", "Arial", 40, color=(255, 0, 0)) # Vermelho
            
        return total # Retorna o número lido (-1 se falhar)

    def wait_for_card_removal(self, screen, next_screen):
        """
        Bloqueia a tela e espera o usuário remover o cartão (Estado WAITING_FOR_REMOVAL).
        """
        self.timer.pause() # Pausa o timer enquanto espera a remoção
        
        # Desenha a mensagem de "Retirar Cartão"
        self.background_green.draw()
        self.PVsComputerTitle.draw(screen)
        removal_msg = Font("Retire o cartão para continuar...", "Arial", 40, color=(255, 165, 0)) # Laranja
        removal_msg.draw(screen, y=self.height / 2.5)
        pygame.display.update()
        
        # Loop de bloqueio até o cartão ser removido
        while True:
            # Tenta ler o cartão
            ten, unit, total = self.nfc.read_once() 

            if total == -1: # Cartão removido
                sleep(1) # Delay de 1 segundo solicitado
                self.game_state = self.WAITING_FOR_CARD # Volta ao estado inicial
                self.current_card_number = -1
                self.statusMessage = Font("Insira o cartão de respostas!", "Arial", 40, color=(255, 0, 0))
                self.timer.resume() # Retoma o timer (se for para a próxima pergunta)
                return next_screen 
            
            # Processa eventos básicos do Pygame para evitar 'Not Responding'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nfc.close()
                    return None
                # Permite sair do loop de espera clicando na seta (melhor UX)
                if event.type == pygame.MOUSEBUTTONDOWN and self.back_rect.collidepoint(event.pos):
                    self.game_state = self.WAITING_FOR_CARD # Reseta estado
                    self.timer.resume()
                    return "gameselect"
            
            pygame.time.delay(100)
            
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
            sleep(1) 
            
            # Próximo estado: Espera a remoção do cartão
            self.game_state = self.WAITING_FOR_REMOVAL
            # next_screen já é None (continua o jogo)
            return None
            
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
            # Só lida com detecção e remoção natural do cartão
            self.handle_nfc_status()

            # 3. Lógica de Fim de Jogo
            remaining = self.timer.update()
            if remaining <= 0:
                # Lógica de Fim de Jogo (Tempo Esgotado)
                # ... (Exibe mensagens de Tempo Esgotado e Total de Acertos)
                
                # Transiciona para espera de remoção e fim de jogo
                self.game_state = self.WAITING_FOR_REMOVAL
                final_screen = self.wait_for_card_removal(self.screen, "gameselect")
                running = False
                next_screen = final_screen
                continue

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
                            # Desenha o botão pressionado e pausa o timer antes de processar
                            self.send.draw(self.screen)
                            pygame.display.update()
                            pygame.time.delay(250)
                            
                            # Processa a resposta (Acerto/Erro) e define o próximo estado/tela
                            next_screen_after_process = self.process_send_action(next_screen)
                            
                            # Se a resposta causou FIM DE JOGO (erro), o next_screen será "gameselect"
                            if next_screen_after_process is not None:
                                next_screen = next_screen_after_process
                            
                            # Entra no loop de bloqueio WAITING_FOR_REMOVAL
                            if self.game_state == self.WAITING_FOR_REMOVAL:
                                result = self.wait_for_card_removal(self.screen, next_screen)
                                
                                # O result será a tela de destino ("gameselect" ou None se sair)
                                running = False
                                next_screen = result
                                break # Sai do loop de eventos para ir ao topo do loop principal

                    elif self.game_state == self.WAITING_FOR_CARD:
                        if self.send.rect.collidepoint(event.pos):
                             # Se pressionar o botão em WAITING_FOR_CARD
                            self.statusMessage = Font("Insira o cartão antes de enviar!", "Arial", 40, color=(255, 0, 0))
                            # Pisca a mensagem de erro no próximo draw

            # Se o loop principal foi interrompido por um break (após o wait_for_card_removal), pular o draw
            if not running and next_screen is not None:
                continue


            # 6. --- DESENHO DE TELA ---
            self.PVsComputerTitle.draw(self.screen)
            self.NumbershowScreen.draw(self.screen, y=self.height / 2.5)
            
            # Desenha a mensagem de status (Insira/Sensor: X) no lugar do botão temporariamente
            if self.game_state != self.WAITING_FOR_REMOVAL:
                self.statusMessage.draw(self.screen, y=self.height / 1.7)
            
            # Desenha o botão de enviar.
            # 💡 CORREÇÃO DO TYPEERROR: Removido 'enabled'
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