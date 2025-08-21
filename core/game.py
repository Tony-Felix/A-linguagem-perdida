import pygame
import sys
from config import settings
from core.player import Jogador
from core.item import Pergaminho
from core.opening import Opening
from core.utils import aplicar_ondulacao
from core.menu import Menu

# ADICIONADO: import da Intro
from core.intro import Intro


class Game:
    instancia = None

    def __init__(self):
        Game.instancia = self
        pygame.init()
        self.screen = pygame.display.set_mode((settings.LARGURA, settings.ALTURA))
        pygame.display.set_caption("NINGUÉM SABE PROGRAMAR - Protótipo")
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Arial", 24)

        # Grupos de sprites
        self.todos_sprites = pygame.sprite.Group()
        self.pergaminhos = pygame.sprite.Group()

        # Jogador
        self.jogador = Jogador()
        self.todos_sprites.add(self.jogador)

        # Pergaminho de exemplo
        perg = Pergaminho(
            200, 200, "Variáveis armazenam valores que podem mudar durante a execução."
        )
        self.todos_sprites.add(perg)
        self.pergaminhos.add(perg)

        # Texto
        self.conceito_coletado = None

        # ADICIONADO: controle de estados do jogo
        self.estado_atual = "intro"
        self.intro = Intro(self)
        self.menu = Menu(self)
        self.abertura = Opening(self.screen, self)

    def run(self):
        while True:
            if self.estado_atual == "intro":
                self.intro.handle_events()
                self.intro.update()
                self.intro.draw()

            elif self.estado_atual == "menu":
                self.menu.handle_events()
                self.menu.update()
                self.menu.draw()

            elif self.estado_atual == "opening":
                self.abertura.handle_events()
                self.abertura.update()
                self.abertura.draw()

            elif self.estado_atual == "jogo":
                self._eventos()
                self._update()
                self._desenhar()

            self.clock.tick(settings.FPS)

    def quit_game(self):
        """Encerra o jogo de forma limpa"""
        self.rodando = False
        pygame.quit()
        sys.exit()

    def _eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.quit_game()

    def _update(self):
        teclas = pygame.key.get_pressed()
        self.jogador.update(teclas)

        # Verifica colisão
        colisao = pygame.sprite.spritecollide(self.jogador, self.pergaminhos, True)
        if colisao:
            self.conceito_coletado = colisao[0].conceito

    def _desenhar(self):
        # 1) Surface temporária
        temp_surface = pygame.Surface((settings.LARGURA, settings.ALTURA))
        temp_surface.fill(settings.FUNDO)

        # 2) Desenha todos os sprites
        self.todos_sprites.draw(temp_surface)

        # 3) Texto do conceito coletado
        if self.conceito_coletado:
            texto = self.fonte.render(
                f"Conceito: {self.conceito_coletado}", True, settings.PRETO
            )
            temp_surface.blit(texto, (20, settings.ALTURA - 40))

        # 4) Aplica ondulação usando a função utilitária
        tempo = pygame.time.get_ticks() / 1000.0
        frame_ondulada = aplicar_ondulacao(temp_surface, tempo)

        # 5) Blit final na tela
        self.screen.blit(frame_ondulada, (0, 0))
        pygame.display.flip()
