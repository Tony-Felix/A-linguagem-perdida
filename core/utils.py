import pygame
import math
from config import settings


def aplicar_ondulacao(frame_surface, tempo):
    largura, altura = frame_surface.get_size()
    dest = pygame.Surface((largura, altura)).convert()
    dest.fill(settings.FUNDO)

    amplitude = settings.ONDULACAO_AMPLITUDE
    freq = settings.ONDULACAO_FREQ
    vel = settings.ONDULACAO_VELOCIDADE

    for y in range(altura):
        deslocamento = int(amplitude * math.sin((y / float(freq)) + tempo * vel))
        if deslocamento >= 0:
            rect1 = pygame.Rect(0, y, largura - deslocamento, 1)
            dest.blit(frame_surface, (deslocamento, y), rect1)
            if deslocamento > 0:
                rect2 = pygame.Rect(largura - deslocamento, y, deslocamento, 1)
                dest.blit(frame_surface, (0, y), rect2)
        else:
            o = -deslocamento
            rect1 = pygame.Rect(o, y, largura - o, 1)
            dest.blit(frame_surface, (0, y), rect1)
            if o > 0:
                rect2 = pygame.Rect(0, y, o, 1)
                dest.blit(frame_surface, (largura - o, y), rect2)
    return dest
