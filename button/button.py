import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, x, y, scale_factor=1.0):
        super().__init__()

        # Pega tamanho real da imagem fornecida
        sheet_width, sheet_height = sprite_sheet.get_size()
        half_width = sheet_width // 2

        # Salva tamanho original
        self.original_width = half_width
        self.original_height = sheet_height

        # Novo tamanho com escala
        new_width = int(half_width * scale_factor)
        new_height = int(sheet_height * scale_factor)

        # Recorta imagem normal
        normal_img = sprite_sheet.subsurface((0, 0, half_width, sheet_height))
        normal_img = pygame.transform.scale(normal_img, (new_width, new_height))

        # Recorta imagem clicada
        clicked_img = sprite_sheet.subsurface((half_width, 0, half_width, sheet_height))
        clicked_img = pygame.transform.scale(clicked_img, (new_width, new_height))

        self.images = [normal_img, clicked_img]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.clicked = False
        self.action = False

    def draw(self, surface):
        self.action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.image = self.images[1]
                self.action = True

        if not pygame.mouse.get_pressed()[0] and self.clicked:
            self.clicked = False
            self.image = self.images[0]

        surface.blit(self.image, self.rect)