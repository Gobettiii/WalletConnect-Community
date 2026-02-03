import arcade 
from base import Base
from tiro import Tiro
import os
import random


TAMANHO_DO_TIRO = 0.8
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

class Boss(arcade.Sprite):
    
    #classe que controla a decida da nave inimiga
    def __init__(self, imagem, zoom):
        super().__init__(imagem, zoom)
        self.center_x = random.randrange(800) 
        self.center_y = random.randrange(480,600) 


    def update(self):
        # movimento da nave
        self.center_y -= 1 #velocidade que desce


    def kill(self):
        self.remove_from_sprite_lists()
        

