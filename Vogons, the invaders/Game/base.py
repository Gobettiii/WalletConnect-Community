import random
import arcade


class Base():
    
    def __init__(self):
        self.vida_base = 100
        self.vida = True


    def set_vida_base(self):
        self.vida_base -= random.randrange(10,20)
        return self.vida_base


    def validador_de_vida(self):
        if self.vida_base <= 0:
            return False
        else:
            return True
    def dar_vida_base(self):
        self.vida_base = 100
