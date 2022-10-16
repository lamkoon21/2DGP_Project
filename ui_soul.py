from pico2d import *
import player

class Soul:
    def __init__(self):
        self.x, self.y = 240, 935
        self.hp_x, self.hp_y = 250, 955
        self.image = load_image('image/ui/Soul.png')
        self.fill = 0
        self.full_soul = None
        self.soul = 0
        self.hp = 0
    
    def update(self):
        if self.soul == 9:
            self.full_soul = True
        else:
            self.full_soul = False
            
        self.fill = self.soul * 12
        
    def draw(self):
        if self.full_soul:
            self.image.clip_draw(160, 250, 125, 125, self.x - 55, self.y - 14)
        else:
            self.image.clip_draw(15, 250, 125, 125, self.x - 55, self.y - 16)
            self.image.clip_draw(15, 105, 125, 125, self.x - 55, self.y - 132 + self.fill)
            
        self.image.clip_draw(10, 385, 245, 160, self.x, self.y)
        
        i = 0
        
        while(i < self.hp):
            self.image.clip_draw(19, 28, 41, 52, self.hp_x + (60 * (i + 1)), self.hp_y)
            i += 1
            
        while(i < self.hp + (5 - self.hp)):
            self.image.clip_draw(73, 28, 42, 52, self.hp_x + (60 * (i + 1)), self.hp_y)
            i += 1