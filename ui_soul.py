from pico2d import *
import player
import server

class Soul(player.Knight):
    def __init__(self):
        self.x, self.y = 240, 935
        self.hp_x, self.hp_y = 250, 955
        self.image = load_image('image/ui/Soul.png')
    
    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(15, 250, 125, 125, self.x - 55, self.y - 16)
        
        if server.knight.soul < 9:
            self.image.clip_draw(132 * server.knight.soul - 132, 120, 132, 132, self.x - 58, self.y - 35)
        else:
            self.image.clip_draw(160, 250, 125, 125, self.x - 55, self.y - 14)
            
        
        
        
            
        self.image.clip_draw(10, 385, 245, 160, self.x, self.y)
        
        i = 0
        while(i < server.knight.hp):
            self.image.clip_draw(19, 28, 41, 52, self.hp_x + (60 * (i + 1)), self.hp_y)
            i += 1
            
        while(i < server.knight.hp + (5 - server.knight.hp)):
            self.image.clip_draw(73, 28, 42, 52, self.hp_x + (60 * (i + 1)), self.hp_y)
            i += 1