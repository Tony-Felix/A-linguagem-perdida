import pygame
from config import settings


class Intro:
    def __init__(self, jogo):
        self.jogo = jogo
        logo = pygame.image.load("assets/images/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(logo, (settings.LARGURA, settings.ALTURA))
        self.logo_rect = self.logo.get_rect(topleft=(0, 0))

        self.alpha = 0
        self.velocidade_fade = 2
        self.pronto = False
        self.adiantado = False  # Novo: indica se o usuário adiantou o fade

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jogo.quit_game()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                self.adiantado = True  # sinaliza para acelerar o fade

    def update(self):
        # Se o jogador adiantou, faz o fade ir direto para 255
        if self.adiantado:
            self.alpha = 255
            self.pronto = True
            self.jogo.estado_atual = "menu"
        else:
            if self.alpha < 255:
                self.alpha += self.velocidade_fade
                if self.alpha > 255:
                    self.alpha = 255
            else:
                pygame.time.delay(1500)
                self.pronto = True
                self.jogo.estado_atual = "menu"

    def draw(self):
        self.jogo.screen.fill(settings.PRETO)
        logo_temp = self.logo.copy()
        logo_temp.set_alpha(self.alpha)
        self.jogo.screen.blit(logo_temp, self.logo_rect)
        pygame.display.flip()
