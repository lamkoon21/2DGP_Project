from pico2d import *
from constant_value import *
import ingame

class Floor:
    def __init__(self):
        self.image = load_image('image/map/floor.png')
        
    def update(self):
        pass 

    def draw(self):
        self.image.draw(1200, self.image.h // 2)
        self.image.draw(0, self.image.h // 2)
        self.image.draw(1200, self.image.h)
        self.image.draw(0, self.image.h)
        self.image.draw(1200, 240)
        self.image.draw(0, 240)
        
        if ingame.collide_box:
                draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return 0, 0, 1920, 340
    
    def handle_collision(self, other, group):
        pass