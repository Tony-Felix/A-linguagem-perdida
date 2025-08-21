import pygame
from config.settings import AMARELO


class Pergaminho(pygame.sprite.Sprite):
    def __init__(self, x, y, conceito):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect(center=(x, y))
        self.conceito = conceito
