from pico2d import *
import server
from constant_value import *
import game_framework
import game_world

class Crawlid:
    image_l = None
    image_r = None
    move_sound = None
    death_sound = None
    font = None
    def __init__(self, x, y, dir, range_x1, range_x2):
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        if  Crawlid.image_l == None:
            Crawlid.image_l = load_image('image/enemy/Crawlid_L.png')
        if  Crawlid.image_r == None:
            Crawlid.image_r = load_image('image/enemy/Crawlid_R.png')
        if Crawlid.move_sound == None:
            Crawlid.move_sound = load_wav('music/enemy/crawlid.wav')
            Crawlid.move_sound.set_volume(80)
        if Crawlid.death_sound == None:
            Crawlid.death_sound = load_wav('music/enemy/enemy_death.wav')
        if Crawlid.font == None:
            Crawlid.font = load_font('font.ttf', 16)
        self.move = True
        self.range_x1, self.range_x2 = range_x1, range_x2
        self.turn = False
        self.fall = False
        self.range = True
        self.damage = False
        self.damage_back = 0
        self.hp = 2
        self.gravity = 0
        self.dead = False
        self.dead_back = None
        
        self.move_play = False
        
        self.collide_bottom = False
        self.collide_top = False
        self.collide_left = False
        self.collide_right = False
    
    def update(self):        
        if self.dead:
            if int(self.frame) < 1:
                self.frame = (self.frame + 2 * ACTION_PER_TIME * game_framework.frame_time) % 2
                
            if self.dead_back == None:
                self.death_sound.play()
                self.dead_back = 3
            elif self.dead_back > 0:
                self.gravity += 0.5
                self.x += (self.dead_back * 2) * server.knight.face_dir
                self.y += (self.dead_back * 2) - self.gravity
            if self.dead_back == 0:
                self.hp = -1
                    
        elif self.damage_back > 0:
            self.x += server.knight.face_dir * 10
            self.damage_back -= 1
                
        elif self.turn:
            if self.x < self.range_x1:
                    self.x = self.range_x1
            elif self.x > self.range_x2:
                    self.x = self.range_x2
                                
            self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
            
            if int(self.frame) == 2:
                self.turn = False
                self.move = True
                self.frame = 0
                self.dir *= -1
                
        elif self.move:
            if server.knight.x > self.x - 1000 and server.knight.x < self.x + 1000:
                if self.move_play == False:
                    # self.move_sound.play()
                    self.move_play = True
                pass
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.x += self.dir * 4
            
        if self.fall:
            self.gravity += G
            self.y += (FALL_G - self.gravity)
                
        range_check(self)
        hp_check(self)
        fall_check(self)
            
    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        
        if server.collide_box:
            draw_rectangle(*self.get_bb())
            self.font.draw(cx, cy + 60, f'(HP: {self.hp})', (255, 255, 0))
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(345 - int(self.frame) * 130, 0, 140, 90, cx, cy - 20)
            elif self.turn:
                self.image_r.clip_draw(380 - int(self.frame) * 97, 259, 94, 80, cx, cy - 20)
            elif self.move:
                self.image_r.clip_draw(360 - int(self.frame) * 119, 365, 115, 80, cx, cy - 20)
            else:
                self.image_r.clip_draw(360 - int(self.frame) * 119, 365, 115, 80, cx, cy - 20)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(int(self.frame) * 125, 0, 135, 90, cx, cy - 20)
            elif self.turn:
                self.image_l.clip_draw(int(self.frame) * 97 + 3, 259, 94, 80, cx, cy - 20)
            elif self.move:
                self.image_l.clip_draw(int(self.frame) * 119 + 3, 365, 115, 80, cx, cy - 20)
            else:
                self.image_l.clip_draw(int(self.frame) * 119 + 3, 365, 115, 80, cx, cy - 20)
                
    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 50, cy - 60, cx + 50, cy + 20
    
    def handle_collision(self, other, group):
        if group == 'crawlid:wall':
            collide_wall(self,other,-50,-60,50,20)  
        
        if self.dead == False:         
            if group == 'spike:crawlid':
                if server.knight.attack:
                    if self.damage == False:
                        self.hp -= 1
                        self.damage_back = 5
                        self.damage = True
                else:
                    self.damage = False
      
class Husk:
    image_l = None
    image_r = None
    move_sound = None
    find_sound = None
    death_sound1 = None
    death_sound2 = None
    font = None
    def __init__(self, x, y, dir, range_x1, range_x2):
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        if Husk.image_l == None:
            Husk.image_l = load_image('image/enemy/Husk_L.png')
        if Husk.image_r == None:
            Husk.image_r = load_image('image/enemy/Husk_R.png')
        if Husk.move_sound == None:
            Husk.move_sound = load_wav('music/enemy/husk_step.wav')
            Husk.move_sound.set_volume(80)
        if Husk.death_sound1 == None:
            Husk.death_sound1 = load_wav('music/enemy/enemy_death.wav')
        if Husk.death_sound2 == None:
            Husk.death_sound2 = load_wav('music/enemy/husk_death.wav')
        if Husk.font == None:
            Husk.font = load_font('font.ttf', 16)
        self.move = True
        self.range_x1, self.range_x2 = range_x1, range_x2
        self.range = True
        self.turn = False
        self.fall = False
        self.find = False
        self.attack = False
        self.attack_range = 150
        self.damage = False
        self.damage_back = 0
        self.hp = 3
        self.gravity = 0
        self.dead = False
        self.dead_back = None
        self.move_play = False
        self.find_play = False
        
        self.collide_bottom = False
        self.collide_top = False
        self.collide_left = False
        self.collide_right = False
    
    def update(self):

        if self.dead:
            if int(self.frame) < 7:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
                
            if self.dead_back == None:
                self.death_sound1.play()
                self.death_sound2.play()
                self.dead_back = 3
            elif self.dead_back > 0:
                self.gravity += 0.5
                self.x += (self.dead_back * 2) * server.knight.face_dir
                self.y += (self.dead_back * 2) - self.gravity
            if self.dead_back == 0:
                self.hp = -1
                
        elif self.move:
            if server.knight.x > self.x - 1000 and server.knight.x < self.x + 1000:
                if self.move_play == False:
                    # self.move_sound.play()
                    self.move_play = True
                pass
            self.frame = (self.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7
            self.x += self.dir * 2
        
        if self.dead:
            pass
        
        elif self.damage_back > 0:
            self.x += server.knight.face_dir * 10
            self.damage_back -= 1
        
        elif self.find:
            self.move = False
            if self.attack == False:
    
                if int(self.frame) < 3:
                    self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                    
                else:
                    self.find = False
                    self.attack = True
                    self.frame = 0
        
        elif self.turn:
            if self.range:
                if self.x < self.range_x1:
                    self.x = self.range_x1
                elif self.x > self.range_x2:
                    self.x = self.range_x2
                    
            self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
            
            if int(self.frame) == 2:
                self.turn = False
                self.move = True
                self.frame = 0
                self.dir *= -1
                
            if self.attack:
                self.attack = False
                self.move = True
                    
        elif self.attack:
            
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.x += self.dir * 5.5
            
            if self.dir == 1:
                if server.knight.y - 50 > self.y + 50 or server.knight.y + 50 < self.y - 50 or server.knight.x < self.x or server.knight.x > self.x + 350:
                    if self.attack_range > 0:
                        self.attack_range -= abs(self.dir * 2)
                    else:
                        self.frame = 0
                        self.move = True
                        self.attack = False
                        self.attack_range = 150
            else:
                if server.knight.y - 50 > self.y + 50 or server.knight.x < self.x - 350 or server.knight.x > self.x:
                    if self.attack_range > 0:
                        self.attack_range -= abs(self.dir * 2)
                    else:
                        self.frame = 0
                        self.move = True
                        self.attack = False
                        self.attack_range = 150 
                        
        if self.fall:
            self.gravity += G
            self.y += (FALL_G - self.gravity)
            
        # attack range
        if self.find == False and self.attack == False:
            if server.knight.y - 50 < self.y + 50:
                if server.knight.x > self.x - 400 and server.knight.x < self.x + 400:
                    if self.dir == 1:
                        if server.knight.x < self.x:
                            self.dir = -1
                        self.find = True
                        self.range = False
                        self.frame = 0
                    elif self.dir == -1:
                        if server.knight.x > self.x:
                            self.dir = 1
                        self.find = True
                        self.range = False
                        self.frame = 0
                
        if self.find == False and self.attack == False:
            range_check(self)
        hp_check(self)
        fall_check(self)
            
    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        
        if server.collide_box:
            draw_rectangle(*self.get_bb())
            self.font.draw(cx, cy + 80, f'(HP: {self.hp})', (255, 255, 0))
            
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(975 - int(self.frame) * 140, 0, 140, 120, cx, cy - 5)
            elif self.turn:
                self.image_r.clip_draw(1009 - int(self.frame) * 105, 715, 105, 128, cx, cy)
            elif self.find:
                self.image_r.clip_draw(1002 - int(self.frame) * 118, 555, 110, 135, cx, cy)
            elif self.attack:
                self.image_r.clip_draw(990 - int(self.frame) * 125, 410, 125, 125, cx, cy)
            elif self.move:
                self.image_r.clip_draw(997 - int(self.frame) * 118, 865, 115, 127, cx, cy)
            else:
                self.image_r.clip_draw(997 - int(self.frame) * 118, 865, 115, 127, cx, cy)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(int(self.frame) * 140, 0, 140, 120, cx, cy - 5)
            elif self.turn:
                self.image_l.clip_draw(int(self.frame) * 105 + 5, 715, 105, 128, cx, cy)
            elif self.find:
                self.image_l.clip_draw(int(self.frame) * 118 + 3, 555, 110, 135, cx, cy)
            elif self.attack:
                self.image_l.clip_draw(int(self.frame) * 124 + 3, 410, 125, 125, cx, cy)
            elif self.move:
                self.image_l.clip_draw(int(self.frame) * 118 + 3, 865, 115, 130, cx, cy)
            else:
                self.image_l.clip_draw(int(self.frame) * 118 + 3, 865, 115, 130, cx, cy)
                
    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 50, cy - 60, cx + 50, cy + 60
    
    def handle_collision(self, other, group):
        if group == 'husk:wall':
            collide_wall(self,other,-50, -60, 50, 60)
        
        if self.dead == False:
            if group == 'spike:husk':
                damage_check(self)
    
class Vengefly:
    image_l = None
    image_r = None
    find_sound = None
    death_sound = None
    font = None
    def __init__(self, x, y, dir, range_x1, range_x2):
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        self.dir_y = 0.0
        if Vengefly.image_l == None:
            Vengefly.image_l = load_image('image/enemy/Vengefly_L.png')
        if Vengefly.image_r == None:
            Vengefly.image_r = load_image('image/enemy/Vengefly_R.png')
        if Vengefly.find_sound == None:
            Vengefly.find_sound = load_wav('music/enemy/vengefly_find.wav')
        if Vengefly.death_sound == None:
            Vengefly.death_sound = load_wav('music/enemy/enemy_death.wav')
        if Vengefly.font == None:
            Vengefly.font = load_font('font.ttf', 16)
        self.move = True
        self.range_x1, self.range_x2 = range_x1, range_x2
        self.range = True
        self.turn = False
        self.fall = False
        self.find = False
        self.find_play = False
        self.attack = False
        self.damage = False
        self.damage_back = 0
        self.hp = 2
        self.gravity = 0
        self.dead = False
        self.dead_back = None
        
        self.collide_bottom = False
        self.collide_top = False
        self.collide_left = False
        self.collide_right = False
    
    def update(self):
        
        self.cx = self.x - server.background.window_left
        self.cy = self.y - server.background.window_bottom
        
        if self.dead:
            if int(self.frame) < 2:
                self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
                
            if self.dead_back == None:
                self.death_sound.play()
                self.dead_back = 3
            elif self.dead_back > 0:
                self.gravity += 0.5
                self.x += (self.dead_back * 2) * server.knight.face_dir
                self.y += (self.dead_back * 2) - self.gravity
            if self.dead_back == 0:
                self.hp = -1
                
        elif self.turn:
            if self.range:
                if self.x < self.range_x1:
                    self.x = self.range_x1
                elif self.x > self.range_x2:
                    self.x = self.range_x2
                    
            self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time * 1.5) % 3
            
            if int(self.frame) == 2:
                self.turn = False
                self.move = True
                self.frame = 0
                self.dir *= -1
                
            if self.attack:
                self.attack = False
                self.move = True
                
        elif self.move:                
            self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
            self.x += self.dir * 5
            
        if self.dead:
            pass
        
        elif self.damage_back > 0:
            self.x += server.knight.face_dir * 10
            self.damage_back -= 1
        
        elif self.find:
            if self.find_play == False:
                self.find_sound.play()
                self.find_play = True
            
            self.move = False
            if self.attack == False:
                
                if int(self.frame) < 3:
                    self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                
                else:
                    self.find = False
                    self.turn = False
                    self.move = False
                    self.attack = True
                    self.frame = 0
                    
        elif self.attack:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                
            if self.dir == 1:
                if server.knight.x < self.x:
                    self.dir = -1
            elif self.dir == -1:
                if server.knight.x > self.x:
                    self.dir = 1
                    
            if server.knight.y < self.y:
                self.dir_y = -1
            elif server.knight.y > self.y:
                self.dir_y = 1
                
            
            self.x += self.dir * 5
            if self.x + (300 * self.dir) < server.knight.x:
                self.y += self.dir_y * 3.5
            
        # attack range
        if self.find == False and self.attack == False:
            if server.knight.y + 30 > self.y - 400 and server.knight.y + 30 < self.y + 400:
                if server.knight.x > self.x - 400 and server.knight.x < self.x + 400:
                    self.find = True
                    self.range = False
                    self.frame = 0
            
        if self.fall:
            self.gravity += G
            self.y += (FALL_G - self.gravity)
                
        if self.find == False and self.attack == False:
            range_check(self)
        hp_check(self)
        if self.dead:
            fall_check(self)
            
    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        
        if server.collide_box:
            draw_rectangle(*self.get_bb())
            self.font.draw(cx, cy + 80, f'(HP: {self.hp})', (255, 255, 0))
            
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(455 - int(self.frame) * 150, 0, 150, 110, cx, cy - 25)
            elif self.turn:
                self.image_r.clip_draw(485 - int(self.frame) * 110, 465, 110, 140, cx, cy)
            elif self.find:
                self.image_r.clip_draw(470 - int(self.frame) * 160, 285, 160, 160, cx, cy)
            elif self.attack:
                self.image_r.clip_draw(460 - int(self.frame) * 150, 130, 150, 140, cx, cy)
            elif self.move:
                self.image_r.clip_draw(485 - int(self.frame) * 120, 635, 115, 140, cx, cy)
            else:
                self.image_r.clip_draw(485 - int(self.frame) * 120, 635, 115, 140, cx, cy)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(int(self.frame) * 150, 0, 150, 110, cx, cy - 25)
            elif self.turn:
                self.image_l.clip_draw(int(self.frame) * 110, 465, 115, 140, cx, cy)
            elif self.find:
                self.image_l.clip_draw(int(self.frame) * 150, 285, 150, 160, cx, cy)
            elif self.attack:
                self.image_l.clip_draw(int(self.frame) * 145, 130, 150, 140, cx, cy)
            elif self.move:
                self.image_l.clip_draw(int(self.frame) * 120 + 5, 635, 115, 140, cx, cy)
            else:
                self.image_l.clip_draw(int(self.frame) * 120 + 5, 635, 115, 140, cx, cy)
                
    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 50, cy - 60, cx + 50, cy + 50
        
    def handle_collision(self, other, group):
        if group == 'vengefly:wall':
            collide_wall(self,other,-50, -60, 50, 50)  
        if self.dead == False:
            if group == 'spike:vengefly':
                damage_check(self)
                

class Thorn:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.left, self.bottom, self.right, self.top = 0, 0, 0, 0
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        
        
    def update(self):
        self.left, self.top = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        self.right, self.bottom = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom 

    def draw(self):
        if server.collide_box:
                draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.left, self.bottom, self.right, self.top
    
    def handle_collision(self, other, group):
        pass






def range_check(self):
    if self.range:
        if self.x < self.range_x1 or self.x > self.range_x2:
            self.frame = 0
            self.turn = True
            self.move = False
            
def hp_check(self):
    if self.hp == 0:
        self.dead = True
        self.turn = False
        self.move = False
        self.frame = 0
            
def fall_check(self):
    if self.collide_bottom == False and self.collide_top == False and self.hp > -1:
        if self.fall == False:
            self.gravity = FALL_G
        self.fall = True
    else:
        self.fall = False
        
def damage_check(self):
    if server.knight.attack:
        if self.damage == False:
            self.hp -= 1
            self.damage_back = 5
            self.damage = True
    else:
        self.damage = False
            
def collide_wall(self, other, l, b, r, t):
    cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
    left, bottom, right, top = cx + l, cy + b, cx + r, cy + t

    if other.top > bottom and other.top - bottom < 50:
        if self.dead:
            if self.dead_back > 0:
                self.dead_back -= 1
                self.gravity = 0
                        
        elif self.fall:
            self.frame = 0
            self.gravity = 0
            self.fall = False
        self.y = other.y1 - b
                    
    elif other.bottom < top and top - other.bottom < 50:
        if self.fall:
            self.frame = 0
            self.gravity = FALL_G
            self.fall = False
            self.jump = False
        self.y = other.y2 - t
                    
    if other.top - bottom > 30 or other.bottom - top > 50:
        if other.right > left and other.right - left < 50:
            self.x = other.x2 - l
            self.turn = True
            self.move = False
                    
        elif other.left < right and right - other.left < 50:
            self.x = other.x1 - r
            self.turn = True
            self.move = False
                    
    if self.y == other.y1 + 60:
        self.collide_bottom = True
    if self.y == other.y2 - 20:
        self.collide_top = True
    if self.x == other.x2 + 50:
        self.collide_left = True
    if self.x == other.x1 - 50:
        self.collide_right = True