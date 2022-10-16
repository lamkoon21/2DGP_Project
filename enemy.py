from lib2to3.pgen2.token import LEFTSHIFT
from turtle import Turtle
from pico2d import *
import ingame

BOTTOM = 400
TOP = 1050
LEFT = 30
RIGHT = 1890

class Crawlid:
    def __init__(self):
        self.x, self. y = None, None
        self.frame = 0
        self.dir = 1
        self.image_l = load_image('image/enemy/Crawlid_L.png')
        self.image_r = load_image('image/enemy/Crawlid_R.png')
        self.turn = False
        self.move = True
        self.move_time = 3
        self.range_x1, self.range_x2 = None, None
        self.damage = False
        self.hp = 2
        self.gravity = 0
        self.dead = False
        self.dead_back = None
    
    def update(self):
        if self.dead:
            self.hp = -1
            if self.frame < 1:
                self.frame += 1
            
            if self.dead_back == None:
                if self.y > BOTTOM:
                    self.gravity += 1
                    self.y -= self.gravity
                else:
                    self.y = BOTTOM
                    self.gravity = 0
                    self.dead_back = 3
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 1
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= BOTTOM:
                    self.dead_back -= 1
                    self.gravity = 0
                
        elif self.turn:
            if self.x < self.range_x1:
                    self.x = self.range_x1
            elif self.x > self.range_x2:
                    self.x = self.range_x2
                    
            self.move_time -= 1
            
            if self.move_time == 0:
                self.frame += 1
                self.move_time = 3
            
            if self.frame == 2:
                self.turn = False
                self.move = True
                self.frame = 0
                self.dir *= -1
                
        elif self.move:
            self.move_time -= 1
            if self.move_time == 0:
                self.frame = (self.frame + 1) % 4
                self.move_time = 4
            self.x += self.dir * 3
                
        # range    
        if self.x < self.range_x1 or self.x > self.range_x2:
            self.frame = 0
            self.turn = True
            self.move = False
        
        if self.x > RIGHT:
            self.x = RIGHT   
        elif self.x < LEFT:
            self.x = LEFT
        
        if self.y > TOP:
            self.y = TOP
        elif self.y < BOTTOM:
            self.y = BOTTOM
            
        if self.hp == 0:
            self.dead = True
            self.turn = False
            self.move = False
            self.frame = 0
            
    def draw(self):
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(345 - self.frame * 130, 0, 140, 90, self.x, self.y - 20)
            elif self.turn:
                self.image_r.clip_draw(380 - self.frame * 97, 259, 94, 80, self.x, self.y - 20)
            elif self.move:
                self.image_r.clip_draw(360 - self.frame * 119, 365, 115, 80, self.x, self.y - 20)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(self.frame * 125, 0, 135, 90, self.x, self.y - 20)
            elif self.turn:
                self.image_l.clip_draw(self.frame * 97 + 3, 259, 94, 80, self.x, self.y - 20)
                pass
            elif self.move:
                self.image_l.clip_draw(self.frame * 119 + 3, 365, 115, 80, self.x, self.y - 20)
      
class Husk:
    def __init__(self):
        self.x, self. y = None, None
        self.frame = 0
        self.dir = -1
        self.image_l = load_image('image/enemy/Husk_L.png')
        self.image_r = load_image('image/enemy/Husk_R.png')
        self.turn = False
        self.move = True
        self.move_time = 3
        self.range_x1, self.range_x2 = None, None
        self.find = False
        self.find_time = 10
        self.find_x, self.find_y = 0, 0
        self.attack = False
        self.attack_range = 150
        self.hp = 3
        self.gravity = 0
        self.dead = False
        self.dead_back = None
    
    def update(self):
        if self.dead:
            self.hp = -1
            if self.frame < 7:
                self.frame += 1
                
            if self.dead_back == None:
                if self.y > BOTTOM:
                    self.gravity += 1
                    self.y -= self.gravity
                else:
                    self.y = BOTTOM
                    self.gravity = 0
                    self.dead_back = 3
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 1
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= BOTTOM:
                    self.dead_back -= 1
                    self.gravity = 0
                
        elif self.turn:
            if self.x < self.range_x1:
                self.x = self.range_x1
            elif self.x > self.range_x2:
                self.x = self.range_x2
                    
            self.frame += 1
            
            if self.frame == 2:
                self.turn = False
                self.move = True
                self.frame = 0
                self.dir *= -1
                
            if self.attack:
                self.attack = False
                self.move = True
                
        elif self.move:
            self.move_time -= 1
            if self.move_time == 0:
                self.frame = (self.frame + 1) % 7
                self.move_time = 3
            self.x += self.dir * 5
                
        if self.find:
            self.move = False
            if self.attack == False:
                
                self.move_time -= 1
                
                if self.move_time == 0:
                    if self.frame < 3:
                        self.frame += 1
                    self.move_time = 3
                    
                self.find_time -= 1
                
                if self.find_time == 0:
                    self.find = False
                    self.attack = True
                    self.frame = 0
                    self.find_time = 10
                    
        elif self.attack:
            self.move_time -= 1
            if self.move_time == 0:
                self.frame = (self.frame + 1) % 4
                self.move_time = 3
                
            self.x += self.dir * 10
            if self.find_y - 50 > self.y + 50 or self.find_x < self.x - 350 or self. find_x > self.x + 350:
                    if self.attack_range > 0:
                        self.attack_range -= abs(self.dir * 10)
                    else:
                        self.frame = 0
                        self.move = True
                        self.attack = False
                        self.attack_range = 150
                        
        # attack range
        if self.find == False and self.attack == False:
            if self.find_y - 50 < self.y + 50:
                if self.find_x > self.x - 400 and self. find_x < self.x + 400:
                    if self.dir == 1:
                        if self.find_x < self.x:
                            self.dir = -1
                        self.find = True
                        self.frame = 0
                    elif self.dir == -1:
                        if self.find_x > self.x:
                            self.dir = 1
                        self.find = True
                        self.frame = 0
            
        # range    
        if self.attack == False:
            if self.x < self.range_x1 or self.x > self.range_x2:
                self.frame = 0
                self.turn = True
                self.move = False
        else:
            self.range_x1 = LEFT
            self.range_x2 = RIGHT
        
        if self.x > RIGHT:
            self.x = RIGHT
            self.turn = True
        elif self.x < LEFT:
            self.x = LEFT
            self.turn = True
        
        if self.y > TOP:
            self.y = TOP
        elif self.y < BOTTOM:
            self.y = BOTTOM
            
        if self.hp == 0:
            self.dead = True
            self.turn = False
            self.move = False
            self.frame = 0
            
    def draw(self):
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(975 - self.frame * 140, 0, 140, 120, self.x, self.y)
            elif self.turn:
                self.image_r.clip_draw(1009 - self.frame * 105, 715, 105, 128, self.x, self.y)
            elif self.find:
                self.image_r.clip_draw(1002 - self.frame * 118, 555, 110, 135, self.x, self.y)
            elif self.attack:
                self.image_r.clip_draw(990 - self.frame * 125, 410, 125, 125, self.x, self.y)
            elif self.move:
                self.image_r.clip_draw(997 - self.frame * 118, 865, 115, 127, self.x, self.y)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(self.frame * 140, 0, 140, 120, self.x, self.y)
            elif self.turn:
                self.image_l.clip_draw(self.frame * 105 + 5, 715, 105, 128, self.x, self.y)
            elif self.find:
                self.image_l.clip_draw(self.frame * 118 + 3, 555, 110, 135, self.x, self.y)
            elif self.attack:
                self.image_l.clip_draw(self.frame * 124 + 3, 410, 125, 125, self.x, self.y)
            elif self.move:
                self.image_l.clip_draw(self.frame * 118 + 3, 865, 115, 130, self.x, self.y)

class Vengefly:
    def __init__(self):
        self.x, self. y = None, None
        self.frame = 0
        self.dir = -1
        self.dir_y = 0
        self.image_l = load_image('image/enemy/Vengefly_L.png')
        self.image_r = load_image('image/enemy/Vengefly_R.png')
        self.turn = False
        self.move = True
        self.move_time = 3
        self.range_x1, self.range_x2 = 0, 0
        self.find = False
        self.find_x, self.find_y = 0, 0
        self.find_time = 10
        self.attack = False
        self.hp = 2
        self.gravity = 0
        self.dead = False
        self.dead_back = None
    
    def update(self):
        if self.dead:
            self.hp = -1
            if self.frame < 2:
                self.frame += 1
            
            if self.dead_back == None:
                if self.y > BOTTOM:
                    self.gravity += 1
                    self.y -= self.gravity
                else:
                    self.y = BOTTOM
                    self.gravity = 0
                    self.dead_back = 3
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 1
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= BOTTOM:
                    self.dead_back -= 1
                    self.gravity = 0
                
        elif self.turn:
            if self.x < self.range_x1:
                self.x = self.range_x1
            elif self.x > self.range_x2:
                self.x = self.range_x2
                    
            self.frame += 1
            
            if self.frame == 2:
                self.turn = False
                self.move = True
                self.frame = 0
                self.dir *= -1
                
            if self.attack:
                self.attack = False
                self.move = True
                
        elif self.move:
            self.move_time -= 1
            if self.move_time == 0:
                self.frame = (self.frame + 1) % 5
                self.move_time = 3
            self.x += self.dir * 5
            
        if self.find:
            self.move = False
            if self.attack == False:
                
                self.move_time -= 1
                
                if self.move_time == 0:
                    self.move_time = 3
                    if self.frame < 3:
                        self.frame += 1
                    
                self.find_time -= 1
                
                if self.find_time == 0:
                    self.find = False
                    self.attack = True
                    self.frame = 0
                    self.find_time = 10
                    
        elif self.attack:
            self.move_time -= 1
            
            if self.move_time == 0:
                self.frame = (self.frame + 1) % 4
                self.move_time = 3
                
            if self.dir == 1:
                if self.find_x < self.x:
                    self.dir = -1
            elif self.dir == -1:
                if self.find_x > self.x:
                    self.dir = 1
                    
            if self.find_y < self.y:
                self.dir_y = -1
            elif self.find_y > self.y:
                self.dir_y = 1
                
            
            self.x += self.dir * 12
            if self.x + (300 * self.dir) < self.find_x and self.y - 40 > BOTTOM:
                self.y += self.dir_y * 6
            
        # attack range
        if self.find == False and self.attack == False:
            if self.find_y + 30 > self.y - 400 and self. find_y + 30 < self.y + 400:
                if self.find_x > self.x - 400 and self. find_x < self.x + 400:
                    self.find = True
                    self.frame = 0
            
        # range    
        if self.attack == False:
            if self.x < self.range_x1 or self.x > self.range_x2:
                self.frame = 0
                self.turn = True
                self.move = False
        else:
            self.range_x1 = LEFT
            self.range_x2 = RIGHT
            
        if self.x > RIGHT:
            self.x = RIGHT   
        elif self.x < LEFT:
            self.x = LEFT
        
        if self.y > TOP:
            self.y = TOP
        elif self.y < BOTTOM:
            self.y = BOTTOM
            
        if self.hp == 0:
            self.dead = True
            self.turn = False
            self.move = False
            self.frame = 0
            
    def draw(self):
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(455 - self.frame * 150, 0, 150, 110, self.x, self.y - 25)
            elif self.turn:
                self.image_r.clip_draw(485 - self.frame * 110, 465, 110, 140, self.x, self.y)
            elif self.find:
                self.image_r.clip_draw(470 - self.frame * 160, 285, 160, 160, self.x, self.y)
            elif self.attack:
                self.image_r.clip_draw(460 - self.frame * 150, 130, 150, 140, self.x, self.y)
            elif self.move:
                self.image_r.clip_draw(485 - self.frame * 120, 635, 115, 140, self.x, self.y)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(self.frame * 150, 0, 150, 110, self.x, self.y - 25)
            elif self.turn:
                self.image_l.clip_draw(self.frame * 110, 465, 115, 140, self.x, self.y)
            elif self.find:
                self.image_l.clip_draw(self.frame * 150, 285, 150, 160, self.x, self.y)
            elif self.attack:
                self.image_l.clip_draw(self.frame * 145, 130, 150, 140, self.x, self.y)
            elif self.move:
                self.image_l.clip_draw(self.frame * 120 + 5, 635, 115, 140, self.x, self.y)