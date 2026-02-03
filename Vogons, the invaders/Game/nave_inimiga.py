import arcade 
from base import Base

class Nave_inimiga(arcade.Sprite):
    
    #classe que controla a decida da nave inimiga
    def __init__(self, imagem, zoom):
        super().__init__(imagem, zoom)


    def update(self):
        # movimento da nave
        self.center_y -= 1 #velocidade que desce
        if self.center_y < 135:
            print("oie")
        
    def kill(self):
        self.remove_from_sprite_lists()

