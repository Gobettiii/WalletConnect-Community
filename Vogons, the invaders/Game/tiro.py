import arcade

VELOCIDADE_DO_TIRO = 4  #velocidade do tiro

class Tiro(arcade.Sprite):

    def __init__(self, imagem, zoom, center_x, local_de_saida):
        super().__init__(imagem, zoom)
        self.angle = 90
        self.center_x = center_x
        self.top = local_de_saida


    def locomocao(self):
        self.top += VELOCIDADE_DO_TIRO
        return self.top
    

    def update(self):
        self.locomocao()
    