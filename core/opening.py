import pygame
import random
from config import settings
from core.colors import CIANO, AZUL_OPENING
from core.utils import aplicar_ondulacao  # importando do utils


class LetraBugada:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.largura)
        r = random.random()
        self.y = int(self.altura * (r**2))
        self.char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*")

        self.cor = random.choice([CIANO, AZUL_OPENING])
        self.velocidade = random.randint(1, 5)

    def update(self):
        self.y += self.velocidade
        if self.y > self.altura:
            self.reset()

    def draw(self, surface, fonte):
        surface.blit(fonte.render(self.char, True, self.cor), (self.x, self.y))


class Opening:
    TEMPO_ENTRE_LINHAS = 4000  # milissegundos entre cada linha

    def __init__(self, screen, jogo):
        self.screen = screen
        self.jogo = jogo
        self.fonte_letras = pygame.font.SysFont("Consolas", 20)
        self.letras = [
            LetraBugada(settings.LARGURA, settings.ALTURA) for _ in range(200)
        ]

        self.texto = [
            "NO FUTURO, AS IAS CONTROLAM TUDO...",
            "POR ISSO, PROGRAMADORES NÃO EXISTEM MAIS...",
            "EM 2150, UMA TEMPESTADE SOLAR CORROMPE TODOS OS SISTEMAS!",
            "PARA SALVAR O MUNDO VOCÊ DECIDE SE TORNAR UM PROGRAMADOR PROFISSIONAL.",
            "SUA MISSÃO: RESTAURAR OS CONCEITOS DE PROGRAMAÇÃO E RECRIAR TODAS AS DOCUMENTAÇÕES.",
        ]

        self.linhas_ativas = []
        self.indice_texto = 0
        self.ultimo_tempo = pygame.time.get_ticks()
        self.terminado = False

        # NOVO: controle do "PRESSIONE ENTER"
        self.mostrar_press_enter = False
        self.timer_press_enter = None
        self.fonte_press_enter = pygame.font.SysFont("Consolas", 36, bold=True)
        self.cor_dourado = (220, 220, 0)

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jogo.quit_game()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.terminado = True

    def update(self):
        # Atualiza letras bugadas
        for letra in self.letras:
            letra.update()

        # Adiciona novas linhas baseado no tempo
        tempo_atual = pygame.time.get_ticks()
        tempo_entre_linhas_corrigido = (
            self.TEMPO_ENTRE_LINHAS + len(self.linhas_ativas) * 500
        )
        if (
            self.indice_texto < len(self.texto)
            and tempo_atual - self.ultimo_tempo > tempo_entre_linhas_corrigido
        ):
            self.linhas_ativas.append(self.texto[self.indice_texto])
            self.indice_texto += 1
            self.ultimo_tempo = tempo_atual

            # Se foi a última linha, inicia timer para "PRESSIONE ENTER"
            if self.indice_texto == len(self.texto):
                self.timer_press_enter = tempo_atual + 6000  # 6 segundos

        # Se todas as linhas foram exibidas, prepara mostrar "PRESSIONE ENTER"
        if self.timer_press_enter and tempo_atual >= self.timer_press_enter:
            self.mostrar_press_enter = True

        # Transição de estado
        if self.terminado:
            self.jogo.estado_atual = "jogo"

    def draw(self):
        frame = pygame.Surface((settings.LARGURA, settings.ALTURA))
        frame.fill(settings.FUNDO)

        for letra in self.letras:
            letra.draw(frame, self.fonte_letras)

        altura_base = settings.ALTURA / 2
        espacamento_vertical = 40
        escala_max = 1.0
        decaimento_escala = 0.1

        for i, linha in enumerate(reversed(self.linhas_ativas)):
            escala = escala_max * max(0.4, 1 - i * decaimento_escala)
            tamanho_fonte = int(32 * escala)
            fonte_texto = pygame.font.SysFont("Consolas", tamanho_fonte, bold=True)
            y = altura_base - i * espacamento_vertical
            render = fonte_texto.render(linha, True, (0, 255, 0))
            rect = render.get_rect(center=(settings.LARGURA / 2, y))
            frame.blit(render, rect)

        # Ondulação
        tempo_ms = pygame.time.get_ticks()
        ciclo = 8000
        duracao_ondulacao = 300
        if (tempo_ms % ciclo) < duracao_ondulacao:
            frame = aplicar_ondulacao(frame, tempo_ms / 1000.0)

        # MOSTRA "PRESSIONE ENTER" se timer expirou
        if self.mostrar_press_enter:
            texto_enter = self.fonte_press_enter.render(
                "PRESSIONE ENTER", True, self.cor_dourado
            )
            rect_enter = texto_enter.get_rect(
                center=(settings.LARGURA / 2, settings.ALTURA * 0.75)
            )
            frame.blit(texto_enter, rect_enter)

        self.screen.blit(frame, (0, 0))
        pygame.display.flip()
