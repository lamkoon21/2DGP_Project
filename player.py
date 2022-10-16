from pico2d import *
import ingame

BOTTOM = 400
TOP = 1050
LEFT = 30
RIGHT = 1890

class Knight:
    def __init__(self):
        self.x, self. y = None, None
        self.frame = 0
        self.dir = 1
        self.image_l = load_image('image/knight/knight_L.png')
        self.image_r = load_image('image/knight/knight_R.png')
        self.fall = False
        self.move = False
        self.jump = False
        self.dash = False
        self.attack = False
        self.attack_2 = False
        self.damage = False
        self.no_dmg = False
        self.no_dmg_time = 50
        
        self.damage_time = 15
        self.move_time = 3
        
        self.gravity = 0
        self.hp = 5
        self.soul = 0
    
    def update(self):
        # action status
        if self.damage:
            self.fall = False
            self.move = False
            self.jump = False
            self.attack = False
            
            self.frame = 0
            if self.hp > 0:
                self.hp -= 1
            self.damage_time -= 1
            if self.damage_time == 0:
                self.damage = False 
                self.no_dmg = True
                self.damage_time = 15
                
        elif self.no_dmg:
            self.no_dmg_time -= 1
            if self.no_dmg_time == 0:
                self.no_dmg = False
                self.no_dmg_time = 50
                
        elif self.attack:
            if self.attack_2:
                self.frame = (self.frame + 1) % 5 + 5
                if self.frame == 9:
                    self.attack = False
                    self.attack_2 = False
                    self.frame = 0
            else:
                self.frame += 1
                if self.frame == 4:
                    self.attack = False
                    self.attack_2 = True
                    self.frame = 0
                    
            if self.move:
                self.x += self.dir * 10
            
            if self.fall or self.jump:
                self.gravity += 2
                self.y += (25 - self.gravity)
                if self.move:
                    self.x += self.dir * 10
            else:
                # self.x += self.dir * -1
                pass
                
        elif self.fall:
            if self.frame < 7:
                self.frame = (self.gravity // 4) % 8 + 4
            else:
                self.frame = 7
                
            if self.move:
                self.x += self.dir * 10
                        
            self.gravity += 2
            self.y += (25 - self.gravity)
                
        elif self.jump:
            if self.frame < 7:
                self.frame = (self.gravity // 4) % 8
            else:
                self.frame = 7
                
            if self.y + (25 - self.gravity) > 0:
                self.gravity += 2
                self.y += (30 - self.gravity)
            else:
                self.jump = False
                self.fall = True    
            
        elif self.move:
            if self.dash == False:
                self.move_time -= 1
                if self.move_time == 0:
                    self.frame = (self.frame + 1) % 8
                    self.move_time = 3
                self.x += self.dir * 10
                
            
        if self.dash:
            if self.damage == False:
                self.jump = False
            
                if self.frame < 10 and self.fall == False:
                    self.frame += 1
                    self.x += self.dir * (-((self.frame % 11) - 5) ** 2 + 50)  
                else:
                    self.frame = 0
                    if self.y > BOTTOM:
                        self.y -= 10
                        self.fall = True
                    if self.y <= BOTTOM:
                        self.dash = False
                        
                        
        # if ingame.knight.x - 20 <= ingame.husk.x + 50 and ingame.knight.y + 30 <= ingame.husk.y - 50 and ingame.knight.x + 20 >= ingame.husk.x - 50 and ingame.knight.y - 30 >= ingame.husk.y + 50:
        #     if ingame.knight.damage == False and ingame.knight.no_dmg == False:
        #         self.damage = True
            
        # range
        if self.x > RIGHT:
            self.x = RIGHT
        elif self.x < LEFT:
            self.x = LEFT
            
        if self.y < BOTTOM:
            self.frame = 0
            self.gravity = 0
            self.y = BOTTOM
            self.fall = False
            self.jump = False
        elif self.y > BOTTOM and self.dash == False:
            self.fall = True
        elif self.y > TOP:
            self.y = TOP
            self.fall = True
            
    def draw(self):
        if self.dir == 1:
            if self.damage:
                self.image_r.clicp_draw(self.frame * 128 + 5, 560, 130, 130, self.x, self.y)
            elif self.attack:
                self.image_r.clip_draw(self.frame * 128 + 10, 415, 125, 130, self.x - 20, self.y)
            elif self.fall:
                self.image_r.clip_draw(self.frame * 128 + 10, 145, 100, 120, self.x, self.y)        
            elif self.dash:
                self.image_r.clip_draw(self.frame * 280, 290, 280, 125, self.x - 95, self.y)
            elif self.jump:
                self.image_r.clip_draw(self.frame * 128 + 10, 145, 100, 120, self.x, self.y)
            elif self.move:
                self.image_r.clip_draw(self.frame * 128 + 138, 15, 100, 120, self.x, self.y)
            else:
                self.image_r.clip_draw(10, 15, 100, 120, self.x, self.y)
                
        elif self.dir == -1:
            if self.damage:
                self.image_r.clicp_draw(self.frame * 128 + 5, 560, 130, 130, self.x, self.y)
            elif self.attack:
                self.image_l.clip_draw(3180 - 10 - self.frame * 128, 415, 125, 130, self.x + 40, self.y)
            elif self.fall:
                self.image_l.clip_draw(3180 - 10 - self.frame * 128, 145, 100, 120, self.x, self.y)
            elif self.dash:
                    self.image_l.clip_draw(3025 - self.frame * 280, 290, 280, 125, self.x + 120, self.y)
            elif self.jump:
                self.image_l.clip_draw(3180 - 10 - self.frame * 128, 145, 100, 120, self.x, self.y)
            elif self.move:
                self.image_l.clip_draw(3180 - 138 - self.frame * 128, 15, 100, 120, self.x, self.y)
            else:
                self.image_l.clip_draw(3170, 15, 100, 120, self.x, self.y)