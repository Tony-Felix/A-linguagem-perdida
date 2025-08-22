import pygame
import os


class AudioManager:
    """Classe para gerenciar música de fundo e efeitos sonoros no jogo."""

    def __init__(self):
        pygame.mixer.init()
        self.efeitos_cache = {}  # Armazena efeitos já carregados

    # --- Música de fundo ---
    def play_music(self, arquivo, loop=-1, volume=0.5):
        """
        Toca música de fundo.
        :param arquivo: caminho relativo para o arquivo de música
        :param loop: -1 para loop infinito, 0 para tocar uma vez
        :param volume: 0.0 a 1.0
        """
        if not os.path.isfile(arquivo):
            print(f"[AudioManager] Arquivo de música não encontrado: {arquivo}")
            return
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)

    def stop_music(self):
        """Para a música de fundo imediatamente."""
        pygame.mixer.music.stop()

    def fadeout_music(self, tempo_ms):
        """Fade out da música de fundo em milissegundos."""
        pygame.mixer.music.fadeout(tempo_ms)

    # --- Efeitos sonoros ---
    def play_sound(self, arquivo, volume=0.5):
        """
        Toca um efeito sonoro.
        :param arquivo: caminho relativo para o arquivo de efeito
        :param volume: 0.0 a 1.0
        """
        if arquivo in self.efeitos_cache:
            som = self.efeitos_cache[arquivo]
        else:
            if not os.path.isfile(arquivo):
                print(f"[AudioManager] Arquivo de efeito não encontrado: {arquivo}")
                return
            som = pygame.mixer.Sound(arquivo)
            self.efeitos_cache[arquivo] = som

        som.set_volume(volume)
        som.play()
