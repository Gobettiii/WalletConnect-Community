import random #para os inimigos surgirem em qualquer lugar da tela
import arcade #funçoes do jogo
import math #para calcular o angulo do tiro
import os
from nave_inimiga import Nave_inimiga
from base import Base
from nave import Nave
from tiro import Tiro
from boss import Boss

#tamanho da tela e titulo do jogo
SCREEN_WIDTH = 800 #eixo x
SCREEN_HEIGHT = 600 #eixo y
SCREEN_TITLE = "Vogons, the invaders" #titulo 

#Variaveis da nave
TAMANHO_DA_NAVE = 0.7 #tamanho da nave

#Variaveis da nave inimiga
TAMANHO_DA_NAVE_INIMIGA = 0.2 #tamanho da nave inimiga

#diretorio para as imagens
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

PAGINA_1 = 1
PAGINA_2 = 2
PAGINA_3 = 3
PAGINA_4 = 4
PAGINA_5 = 5
RODAR_JOGO = 6
GAME_OVER = 7

class Jogo(arcade.Window):

    def __init__(self):
        # Inicialização da janela 
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
       
        self.vida_base = 100
       #Lista de sprites
        self.lista_nave = None
        self.lista_inimigo = None
        self.lista_boss = None
        self.lista_tiro = None
        self.player_sprite = None
        self.tiro_list_boss = None
        
        #determina se o jogo está apto a continuar
        self.vida = True
        
        #variaveis dos pontos
        self.pontuacao = 0 #definir a pontuação inicial

        #variavel do rank
        self.cont_rank = 0

        #contadores
        self.contador_inimigo = 0  #do while do spawn da nave 
       
        #sumir o mouse
        self.set_mouse_visible(False)

        #temporizador do jogo
        self.tempo = 0.0 #definor o valor inicial do tempo  
        self.segundos = 0 #definor o valor inicial do segundos
        self.seg = 0
        self.minutos = 0 #definindo o valor inicial para minutos
        
        #inimigo
        self.QUANTIDADE_DE_INIMIGOS = 1 #total de inimigos iniciais
        self.novos_inimigos_a_cada_horda = 1 #inimigos novos a cada horda
        self.contador_novos_inimigos = 0
        self.contador_boss = 0
        self.contador_tiro_boss = 0
        self.cont_vida = 3
        
        #horda
        self.horda = 0 #definor o valor inicial da horda
        self.contador_horda = 0
        self.pontuaca0_max = 0


    def setup(self):
        #def para definir as coisas 

        # Adcionar os sprites a lista de sprites
        self.lista_nave = arcade.SpriteList() #sprite da nave
        self.lista_inimigo = arcade.SpriteList() #sprite da nave inimiga
        self.lista_tiro = arcade.SpriteList() #sprite do tiro
        self.lista_boss = arcade.SpriteList() #sprite da nave inimiga
        self.tiro_list_boss = arcade.SpriteList() #sprite do tiro do boss
        
        #definindo a imagem de fundo
        self.background = arcade.load_texture(DIRETORIO_ATUAL +                
                                            "/img/fundo.jpg") 

        # Definindo a nave
        self.player_sprite = Nave(DIRETORIO_ATUAL + "/img/nave.png",
                                TAMANHO_DA_NAVE,
                                arcade.key.LEFT, arcade.key.RIGHT)
                                #definindo a imagem da nave 
        #imagem da nave sendo adcionada na lista de sprites
        self.lista_nave.append(self.player_sprite)

        #interface
        self.stats_do_jogo = PAGINA_1 #começar a inicialização pela primeira pagina
        self.instructions = [] #lista em que vai receber as imagens

        texture = arcade.load_texture(DIRETORIO_ATUAL+"/img/ex1.png") #recebendo as imagens
        self.instructions.append(texture) #colocando na lista

        texture = arcade.load_texture(DIRETORIO_ATUAL+"/img/ex2.png") #recebendo as imagens
        self.instructions.append(texture) #colocando na lista
        
        texture = arcade.load_texture(DIRETORIO_ATUAL+"/img/ex3.png") #recebendo as imagens
        self.instructions.append(texture) #colocando na lista

        texture = arcade.load_texture(DIRETORIO_ATUAL+"/img/ex4.png") #recebendo as imagens
        self.instructions.append(texture) #colocando na lista

        texture = arcade.load_texture(DIRETORIO_ATUAL+"/img/ex5.png") #recebendo as imagens
        self.instructions.append(texture) #colocando na lista

        texture = arcade.load_texture(DIRETORIO_ATUAL+"/img/ex6.png") #recebendo as imagens
        self.instructions.append(texture) #colocando na lista
    
    def draw_instructions_page(self, page_number):
       #aqui vai ser desenhada na tela as imagens de instrução do jogo

        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
           
    def draw_game_over(self):
        #aqui será desenhada a tela de game over

        #imagem de game over
        self.draw_instructions_page(5)

        output = f"{self.pontuacao} "
        arcade.draw_text(output, 590, 505, arcade.color.WHITE, 30)

        output = f" {self.pontuaca0_max}"
        arcade.draw_text(output, 655, 161, arcade.color.WHITE, 25)

    def salvar(self):
        #def que salva a pontuação do jogador
        self.cont_rank += 1
        arquivo_pontuacao = open(DIRETORIO_ATUAL+ "/dados.txt", 'a')
        linha = str(self.pontuacao) + "\n"
        arquivo_pontuacao.write(linha)
        arquivo_pontuacao.close()
        
    def rank(self):
        #def que pega a melhor pontuação
        arquivo_pontuacao = open(DIRETORIO_ATUAL+ "/dados.txt", 'r')
        palavras = []

        for linha in arquivo_pontuacao:
            linha = linha.strip("\n")
            palavras.append(linha)
                
        arquivo_pontuacao.close()

        lista = [float(i) for i in palavras]

        self.pontuaca0_max = max(lista)

    def on_draw(self):
       #gerencia as telas

        arcade.start_render()

        # cria a janela(com o plano de fundo)    
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT 
                                    // 2,SCREEN_WIDTH, 
                                    SCREEN_HEIGHT, self.background)   
                                                           
        # executando os sprites na tela
        
        if self.stats_do_jogo == PAGINA_1:
            self.draw_instructions_page(0) #executa o primeiro elemento da lista

        elif self.stats_do_jogo == PAGINA_2:
            self.draw_instructions_page(1) #executa o segundo elemento da lista

        elif self.stats_do_jogo == PAGINA_3:
            self.draw_instructions_page(2) #executa o terceiro elemento da lista

        elif self.stats_do_jogo == PAGINA_4:
            self.draw_instructions_page(3) #executa o quarto elemento da lista

        elif self.stats_do_jogo == PAGINA_5:
            self.draw_instructions_page(4) #executa o quinto elemento da lista

        elif self.stats_do_jogo == RODAR_JOGO: 
            self.draw_game() #roda o jogo

        else: #game over
            
            self.draw_game()
            self.draw_game_over()

        if self.stats_do_jogo == RODAR_JOGO:
            #tempo de jogo
            #tempo de jogo
            self.minutos = int(self.tempo) // 60 #calculo para formar os minutos
            self.segundos = int(self.tempo) % 60#calculo para formar os segundos
        
           
            output = f"Sua pontuação: {self.pontuacao}" #texto da pontuação
            #texto para o tempo de jogo
            
            output1 = f"Tempo jogando: {self.minutos:02d}:{self.segundos:02d}" 
            output2 = f"Horda: {self.horda:02d}" #texto para as hordas
            output3 = f"Base: {self.vida_base:02d}%"
            output4 = f"Tiros disponíveis: {self.contador_de_tiros:02d}"
            output5 = f"vida: {self.cont_vida:02d}"

            #definindo o texto da pontuação
            arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14) 
            #definindo na tela texto da horda
            arcade.draw_text(output2, 680, 576, arcade.color.WHITE, 14)
            #definindo na tela texto do tempo jogado
            arcade.draw_text(output1, 10, 576, arcade.color.WHITE, 14) 
            #definindo na tela texto da vida da base
            arcade.draw_text(output3, 680, 20, arcade.color.WHITE, 14) 
            #definindo na tela texto contador de tiros
            arcade.draw_text(output4, 350, 576, arcade.color.WHITE, 14) 
            #definindo na tela texto contador de vidas
            arcade.draw_text(output5, 350, 13, arcade.color.WHITE, 14) 
      
    def draw_game(self):
        # desenhando os sprites na tela

        self.lista_inimigo.draw() #sprite do inimigo
        self.lista_tiro.draw() #sprite do tiro
        self.lista_nave.draw() #sprite da nave
        self.lista_boss.draw()
        self.tiro_list_boss.draw() #sprite do tiro do boss
        
    def on_mouse_press(self, x, y, button, modifiers):
        #altera ao longo dos clicks
        if self.stats_do_jogo == PAGINA_1:
            self.stats_do_jogo = PAGINA_2

        elif self.stats_do_jogo == PAGINA_2:
            self.stats_do_jogo = PAGINA_3
        
        elif self.stats_do_jogo == PAGINA_3:
            self.stats_do_jogo = PAGINA_4

        elif self.stats_do_jogo == PAGINA_4:
            self.stats_do_jogo = PAGINA_5
        
        elif self.stats_do_jogo == PAGINA_5:
            self.setup()
            self.stats_do_jogo = RODAR_JOGO
       
        elif self.stats_do_jogo == GAME_OVER:
            #reseta as informaçoes
            self.vida = True
            self.horda = 0
            self.contador_de_tiros = self.player_sprite.get_contador_de_tiro()
            Base.dar_vida_base(self)
            self.tempo = 0
            self.setup()
            self.stats_do_jogo = RODAR_JOGO
            self.pontuacao = 0
            self.QUANTIDADE_DE_INIMIGOS = 1
            self.cont_rank = 0
            self.cont_vida = 3
        
    def on_key_press(self, key, modifiers):
    
        if self.vida == True:
        #Movimentação pelo teclado
            for player in self.lista_nave:
                verificador = player.on_key_press(key, modifiers)
                if verificador is not None:
                    #imagem do tiro sendo adcionada na lista de sprites
                    self.lista_tiro.append(verificador) 
           
    def on_key_release(self, key, modifiers):
        #serve para parar de andar quando soltar o botão

        for player in self.lista_nave:
            player.on_key_release(key, modifiers)
    
    def update(self, delta_time):
        #logica do jogo
        
        if self.cont_vida <= 0: #conferir se o ainda pode jogar
            self.vida = False
        
        if self.vida == False:
            if self.cont_rank < 1:
                self.salvar()
            self.stats_do_jogo = GAME_OVER

        if self.vida == True and self.stats_do_jogo == RODAR_JOGO: #enquanto o player tiver vida vai rodar
            
            self.tempo += delta_time #recebe o tempooo
            self.rank()

            #para não sair da tela 
            if self.player_sprite.center_x < 35:
                self.player_sprite.center_x = 35

            if self.player_sprite.center_x > 765:
                self.player_sprite.center_x = 765

            #tiros disponiveis
            self.contador_de_tiros = self.player_sprite.get_contador_de_tiro()
            
            for nave in self.lista_inimigo: #confere todas as naves
                if nave.center_y < 20: #se a posição for igual a 0
                    nave.kill() #tira da tela
                    self.vida_base = Base.set_vida_base(self)
                    print(self.vida_base)
                    self.vida = Base.validador_de_vida(self)
                    
            if int(self.segundos) != 0 and int(self.segundos) != 20  and +\
            int(self.segundos) != 40 and self.vida == True:
                #if para nao bugar na hora de spawn
                if int(self.segundos) % 4 == 0:
                    #zerar as variaveis para a nao bugar
                    self.contador_inimigo = 0#contador volta ao seu numero original
                    self.contador_horda = 0 #contador volta ao seu numero original
                    #contador volta ao seu numero original
                    self.contador_novos_inimigos = 0 
                    self.contador_boss = 0

                if int(self.segundos) % 5  == 0: #a cada 5s 
                    while self.contador_horda < 1:
                        self.horda += 1
                        self.contador_horda += 1 #adcionará para para o if parar
                               
                    while self.QUANTIDADE_DE_INIMIGOS > self.contador_inimigo: 
                        #gera a quantidade de inimigos definidos
                        nave_inimiga = Nave_inimiga(DIRETORIO_ATUAL + 
                                                    "/img/nave_inimiga.png", 
                                                    TAMANHO_DA_NAVE_INIMIGA)
                        #definindo a imagem da nave inimiga

                        sobreposicao = [1] #lista para ser comparada com lista
                        while len(sobreposicao) !=0:
                            #posição dos inimigos(Vão ser adcionados aleatoriamente)
                            nave_inimiga.center_x = random.randrange(SCREEN_WIDTH) 
                            nave_inimiga.center_y = random.randrange(480, 
                            SCREEN_HEIGHT) 
                            #verifica para não nascer duas naves juntas
                            sobreposicao = arcade.check_for_collision_with_list(nave_inimiga, 
                                                                                self.lista_inimigo)
                        #imagem da nave inimiga sendo adcionada na lista de sprites
                        self.lista_inimigo.append(nave_inimiga) 
                        #contador para não gerar mais do que foi definido
                        self.contador_inimigo +=1 
                        
                        if int(self.segundos) % 15 == 0: #a cada 15s
                            if self.contador_novos_inimigos < 1:
                                #a quantidade de inimigos recebe mais x inimigos
                                self.QUANTIDADE_DE_INIMIGOS += +\
                                self.novos_inimigos_a_cada_horda 
                                #serve para repetir apenas uma vez
                                self.contador_novos_inimigos += 1
                                self.player_sprite.nov0s_tiros()    
                    
                            while self.contador_boss < 1:
                                self.contador_boss += 1
                                boss = Boss(DIRETORIO_ATUAL + "/img/boss.png", TAMANHO_DA_NAVE_INIMIGA) 
                                self.lista_boss.append(boss)
                                
                self.seg = self.segundos
    
            #atualizando os sprites 
            self.lista_inimigo.update() #atualizar o sprite do inimigo
            self.lista_tiro.update() #atualizar o sprite do tiro
            self.lista_nave.update()
            self.lista_boss.update()
            self.tiro_list_boss.update() #atualizar o sprite do tiro
            for TIRO in self.lista_tiro: #confirmação do tiro
                
                #verifica se acertou o alvo
                TIRO_ACERTADO = arcade.check_for_collision_with_list(TIRO, 
                                                                self.lista_inimigo)
                TIRO_ACERTADO3 = arcade.check_for_collision_with_list(TIRO, self.lista_boss)#verifica se acertou o alvo

                for nave_inimiga in TIRO_ACERTADO:
                    if nave_inimiga.center_y > 135:
                        #se matar sera adcionado mais um ponto 
                        nave_inimiga.kill() #inimigo sumindo da tela
                        self.pontuacao += 1 #mais um ponto
                        TIRO.kill()
                if len(TIRO_ACERTADO3) > 0:
                    TIRO.kill()
                for boss in TIRO_ACERTADO3: #se matar sera adcionado mais um ponto
                    boss.kill() #inimigo sumindo da tela
                    self.pontuacao += 10 #mais um ponto 

                if TIRO.bottom > self.width or TIRO.top < 0 or TIRO.right < 0 or +\
                TIRO.left > self.width: #tirar a bala da tela se sair da tela
                    TIRO.kill() #tira


            for boss in self.lista_boss: #funçoes do boss

                start_x = boss.center_x #de onde o tiro vem(posição do boss) X
                start_y = boss.center_y #de onde o tiro vem(posição do boss) Y

                dest_x = self.player_sprite.center_x #mira do boss (no player) X
                dest_y = self.player_sprite.center_y #mira do boss (no player) Y

                x_diff = dest_x - start_x #destino do tiro X
                y_diff = dest_y - start_y #destino do tiro Y
                angle = math.atan2(y_diff, x_diff) #angulo do tiro
                boss.angle = math.degrees(angle)-90 #calculo do angulo
                    
                self.contador_tiro_boss += 1 #velociade que atira 
                    
                if self.contador_tiro_boss % 60 == 0: #a cada 1s
                    tiro2 = arcade.Sprite(DIRETORIO_ATUAL+"/img/tiro_boss.png") #recebe o sprite de tiro do boss
                    tiro2.center_x = start_x #posição de onde saira o tiro X
                    tiro2.center_y = start_y #posição de onde saira o tiro Y

                    tiro2.angle = math.degrees(angle)  #ccalcular o angulo do tiro 
                    tiro2.change_x = math.cos(angle) * 3.5 #velocidade tiro X
                    tiro2.change_y = math.sin(angle) * 3.5 #velocidade tiro Y

                    self.tiro_list_boss.append(tiro2) #entra na list

            for tiro2 in self.tiro_list_boss: #confirmação do tiro

                TIRO_ACERTADO2 = arcade.check_for_collision_with_list(tiro2, self.lista_nave)#verifica se acertou o alvo
                
                for self.player_sprite in TIRO_ACERTADO2: #se matar sera adcionado mais um ponto
                    tiro2.kill()#tirar o tiro da tela
                    self.cont_vida -= 1
                               
def main():
    #chamando o jogo
    game = Jogo()
    game.setup()
    arcade.run()

main()