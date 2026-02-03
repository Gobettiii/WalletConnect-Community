import arcade
import os
from tiro import Tiro
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
TAMANHO_DO_TIRO = 0.8 

MOVIMENTACAO_DA_NAVE = 7

class Nave(arcade.Sprite):

    def __init__(self, imagem, zoom, esquerda, direita):
        super().__init__(imagem, zoom)  
        self.movimentacao_esquerda = esquerda
        self.movimentacao_direita = direita
        self.center_y = 123
        self.center_x = 400
        self.contador_de_tiros = 10
    
        
    def on_key_press(self, key, modifiers):

        if key == self.movimentacao_esquerda:
            self.change_x = -MOVIMENTACAO_DA_NAVE

        if key == self.movimentacao_direita:
            self.change_x = MOVIMENTACAO_DA_NAVE
                
        if key == arcade.key.SPACE: #se apertar o espaço vai gerar o tiro
            #Criando o sprite do tiro
            if self.contador_de_tiros > 0:
                self.contador_tiro()
                return self.atirar()
                
    def on_key_release(self, key, modifiers):
        if key == self.movimentacao_esquerda:
            self.change_x = 0
        if key == self.movimentacao_direita:
            self.change_x = 0 

    def atirar(self):
        TIRO = Tiro(DIRETORIO_ATUAL + "/img/tiro.png", TAMANHO_DO_TIRO,
        self.center_x, self.top) #adciona o sprite para a classe Naveinimiga
        return TIRO

    def contador_tiro(self):
        self.contador_de_tiros -= 1

    def get_contador_de_tiro(self):
        return self.contador_de_tiros
    
    def nov0s_tiros(self):
        self.contador_de_tiros +=13
