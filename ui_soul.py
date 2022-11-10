from pico2d import *
import player
import ingame

class Soul(player.Knight):
    def __init__(self):
        self.x, self.y = 240, 935
        self.hp_x, self.hp_y = 250, 955
        self.image = load_image('image/ui/Soul.png')
        self.fill = 0
        self.full_soul = None
    
    def update(self):
        if ingame.knight.soul < 9:
            self.full_soul = False
            self.fill = ingame.knight.soul * 12
        else:
            self.full_soul = True

    def draw(self):
        if self.full_soul:
            self.image.clip_draw(160, 250, 125, 125, self.x - 55, self.y - 14)
        else:
            self.image.clip_draw(15, 250, 125, 125, self.x - 55, self.y - 16)
            self.image.clip_draw(15, 105, 125, 125, self.x - 55, self.y - 132 + self.fill)
            
        self.image.clip_draw(10, 385, 245, 160, self.x, self.y)
        
        i = 0
        while(i < ingame.knight.hp):
            self.image.clip_draw(19, 28, 41, 52, self.hp_x + (60 * (i + 1)), self.hp_y)
            i += 1
            
        while(i < ingame.knight.hp + (5 - ingame.knight.hp)):
            self.image.clip_draw(73, 28, 42, 52, self.hp_x + (60 * (i + 1)), self.hp_y)
            i += 1