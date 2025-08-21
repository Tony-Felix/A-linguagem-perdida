import pygame
from config.settings import AZUL, LARGURA, ALTURA


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect(center=(LARGURA // 2, ALTURA // 2))
        self.velocidade = 5

    def update(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        # Limitar na tela
        self.rect.x = max(0, min(LARGURA - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(ALTURA - self.rect.height, self.rect.y))
