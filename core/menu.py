import pygame
from config import settings
from core.intro import Intro
from core.utils import aplicar_ondulacao


class Menu:
    """
    Menu que NÃO limpa a tela: desenha por cima do último frame,
    preservando a imagem de fundo que já estava exibida.
    """

    def __init__(self, jogo):
        self.jogo = jogo
        self.intro_temp = Intro(jogo)
        self.fundo = self.intro_temp.logo

        self.opcoes = ["Start Game", "Continue", "Options"]
        self.selecionado = 0

        # Fontes
        self.fonte_titulo = pygame.font.SysFont("Arial", 96, bold=True)
        self.fonte_opcoes = pygame.font.SysFont("Arial", 60)
        self.fonte_footer = pygame.font.SysFont("Arial", 40, italic=True)

        # Cores
        self.cor_normal = (255, 255, 255)
        self.cor_selecionada = (0, 255, 255)  # ciano
        self.cor_sombra = (30, 30, 30)
        self.cor_footer = (220, 220, 0)
        self.cor_titulo_principal = (0, 255, 255)  # texto principal
        self.cor_titulo_sombra_3d = (0, 100, 150)  # sombra do relevo 3D

        # Offsets de sombra
        self.sombra_dx = 3
        self.sombra_dy = 3

        # Layout
        self.y_titulo_final = int(settings.ALTURA * 0.38)
        self.y_opcoes_base = int(settings.ALTURA * 0.52)
        self.espacamento_opcoes = 80
        self.y_footer = settings.ALTURA - 150

        # Título do jogo
        self.titulo = "NINGUÉM SABE PROGRAMAR"

        # Blink do rodapé
        self.footer_visivel = True
        self.tempo_inicio = pygame.time.get_ticks()
        self.delay_inicial = 3000
        self.blink_interval = 3000
        self.ultimo_blink = 0
        self.delay_passado = False
        self.footer_area_salva = None

        # --- ANIMAÇÃO ---
        self.titulo_y = -150  # começa fora da tela
        self.titulo_velocidade = 12
        self.opcoes_animadas = [False] * len(self.opcoes)
        self.opcoes_pos_x = [
            (-800 if i % 2 == 0 else settings.LARGURA + 800)
            for i in range(len(self.opcoes))
        ]
        self.opcoes_velocidade_x = 20
        self.opcoes_alcancaram = [False] * len(self.opcoes)
        self.rodape_ativo = False

        # --- ONDULAÇÃO ---
        self.tempo_menu_completo = None  # guarda quando menu terminou
        self.aplicar_ondulacao = False   # flag para ativar efeito
        self.duracao_ondulacao = 300     # duração do efeito em ms
        self.ciclo_ondulacao = 5000      # ciclo do efeito, igual Opening

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jogo.quit_game()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    self.selecionado = (self.selecionado + 1) % len(self.opcoes)
                elif evento.key == pygame.K_UP:
                    self.selecionado = (self.selecionado - 1) % len(self.opcoes)
                elif evento.key == pygame.K_RETURN:
                    self.executar_opcao()

    def executar_opcao(self):
        opcao = self.opcoes[self.selecionado]
        if opcao == "Start Game":
            self.jogo.estado_atual = "opening"
        elif opcao == "Continue":
            self.jogo.estado_atual = "jogo"
        elif opcao == "Options":
            self.jogo.estado_atual = "jogo"

    def update(self):
        agora = pygame.time.get_ticks()
        # Atualiza blink do rodapé
        if self.rodape_ativo:
            if self.footer_visivel and agora - self.ultimo_blink >= 2000:
                self.footer_visivel = False
                self.ultimo_blink = agora
            if not self.footer_visivel and agora - self.ultimo_blink >= 500:
                self.footer_visivel = True
                self.ultimo_blink = agora

        # ANIMAÇÃO DO TÍTULO
        if self.titulo_y < self.y_titulo_final:
            self.titulo_y += self.titulo_velocidade
            if self.titulo_y > self.y_titulo_final:
                self.titulo_y = self.y_titulo_final

        # ANIMAÇÃO DAS OPÇÕES
        for i in range(len(self.opcoes)):
            if self.titulo_y >= self.y_titulo_final:  # só começam após o título
                if not self.opcoes_alcancaram[i]:
                    target_x = (
                        settings.LARGURA - self.fonte_opcoes.size(self.opcoes[i])[0]
                    ) // 2
                    if self.opcoes_pos_x[i] < target_x:
                        self.opcoes_pos_x[i] += self.opcoes_velocidade_x
                        if self.opcoes_pos_x[i] > target_x:
                            self.opcoes_pos_x[i] = target_x
                    elif self.opcoes_pos_x[i] > target_x:
                        self.opcoes_pos_x[i] -= self.opcoes_velocidade_x
                        if self.opcoes_pos_x[i] < target_x:
                            self.opcoes_pos_x[i] = target_x
                    if self.opcoes_pos_x[i] == target_x:
                        self.opcoes_alcancaram[i] = True

        # Ativa rodapé apenas se todas opções já alcançaram
        self.rodape_ativo = all(self.opcoes_alcancaram)

        # Marca tempo quando menu ficou completo
        if self.rodape_ativo and self.tempo_menu_completo is None:
            self.tempo_menu_completo = agora

        # Ativa ondulação 3s depois do menu completo
        if self.tempo_menu_completo and agora - self.tempo_menu_completo >= 3000:
            self.aplicar_ondulacao = True

    def draw(self):
        # --- FUNDO ---
        self.jogo.screen.blit(self.fundo, (0, 0))  # <- redesenha o fundo

        # --- TÍTULO COM EFEITO 3D ---
        camadas = 6
        offset_x = 2
        offset_y = 2
        for i in range(camadas, 0, -1):
            label_relevo = self.fonte_titulo.render(
                self.titulo, True, self.cor_titulo_sombra_3d
            )
            x_titulo = (settings.LARGURA - label_relevo.get_width()) // 2 + i * offset_x
            self.jogo.screen.blit(
                label_relevo, (x_titulo, self.titulo_y + i * offset_y)
            )

        label_titulo = self.fonte_titulo.render(
            self.titulo, True, self.cor_titulo_principal
        )
        x_titulo = (settings.LARGURA - label_titulo.get_width()) // 2
        self.jogo.screen.blit(label_titulo, (x_titulo, self.titulo_y))

        # --- OPÇÕES ---
        for i, texto in enumerate(self.opcoes):
            cor = self.cor_selecionada if i == self.selecionado else self.cor_normal
            label_sombra = self.fonte_opcoes.render(texto, True, self.cor_sombra)
            label = self.fonte_opcoes.render(texto, True, cor)
            y = self.y_opcoes_base + i * self.espacamento_opcoes
            x = self.opcoes_pos_x[i]
            self.jogo.screen.blit(
                label_sombra, (x + self.sombra_dx, y + self.sombra_dy)
            )
            self.jogo.screen.blit(label, (x, y))

        # --- RODAPÉ ---
        if self.rodape_ativo:
            footer = "PRESSIONE ENTER"
            label_footer = self.fonte_footer.render(footer, True, self.cor_footer)
            label_footer_sombra = self.fonte_footer.render(
                footer, True, self.cor_sombra
            )
            x_footer = (settings.LARGURA - label_footer.get_width()) // 2

            padding_x = 10
            padding_y = 6
            rect_x = x_footer - padding_x
            rect_y = self.y_footer - padding_y
            rect_w = label_footer.get_width() + 2 * padding_x
            rect_h = label_footer.get_height() + 2 * padding_y

            if self.footer_area_salva is None:
                self.footer_area_salva = self.jogo.screen.subsurface(
                    (rect_x, rect_y, rect_w, rect_h)
                ).copy()

            if not self.footer_visivel:
                self.jogo.screen.blit(self.footer_area_salva, (rect_x, rect_y))
            else:
                self.jogo.screen.blit(
                    label_footer_sombra,
                    (x_footer + self.sombra_dx, self.y_footer + self.sombra_dy),
                )
                self.jogo.screen.blit(label_footer, (x_footer, self.y_footer))

        # --- ONDULAÇÃO CURTA ---
        if self.aplicar_ondulacao:
            tempo_ms = pygame.time.get_ticks()
            if (tempo_ms % self.ciclo_ondulacao) < self.duracao_ondulacao:
                frame = self.jogo.screen.copy()
                frame = aplicar_ondulacao(frame, tempo_ms / 1000.0)
                self.jogo.screen.blit(frame, (0, 0))

        pygame.display.flip()
