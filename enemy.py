from pico2d import *
import server
from constant_value import *
import game_framework
import game_world

class Crawlid:
    image_l = None
    image_r = None
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.dir = 1
        if  Crawlid.image_l == None:
            Crawlid.image_l = load_image('image/enemy/Crawlid_L.png')
        if  Crawlid.image_r == None:
            Crawlid.image_r = load_image('image/enemy/Crawlid_R.png')
        self.move_sound = load_wav('music/enemy/crawlid.wav')
        self.death_sound = load_wav('music/enemy/enemy_death.wav')
        self.move_sound.set_volume(80)
        self.sound_play = False
        self.font = load_font('font.ttf', 16)
        self.turn = False
        self.move = True
        self.attack = False
        self.range_x1, self.range_x2 = None, None
        self.damage = False
        self.damage_back = 0
        self.hp = 2
        self.gravity = 0
        self.dead = False
        self.dead_back = None
    
    def update(self):        
        if self.dead:
            self.hp = -1
            if int(self.frame) < 1:
                self.frame = (self.frame + 2 * ACTION_PER_TIME * game_framework.frame_time) % 2
                
            if self.dead_back == None:
                self.death_sound.play()
                if self.y > bottom:
                    self.gravity += 0.5
                    self.y -= self.gravity
                    self.dead_back = 3
                else:
                    self.y = bottom
                    self.gravity = 0
                    self.dead_back = 3
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 0.5
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= bottom:
                    self.dead_back -= 1
                    self.gravity = 0
                    
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
            if server.knight.x > self.x - 1000 and server.knight.x < self.x + 1000 and self.sound_play == False:
                # self.move_sound.repeat_play()
                self.sound_play = True
            else:
                # self.move_sound.stop()
                pass
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.x += self.dir * 5
                
        range_check(self)
            
        if self.hp == 0:
            self.dead = True
            self.turn = False
            self.move = False
            self.frame = 0
            
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
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.dir = -1
        if Husk.image_l == None:
            Husk.image_l = load_image('image/enemy/Husk_L.png')
        if Husk.image_r == None:
            Husk.image_r = load_image('image/enemy/Husk_R.png')
        self.move_sound = load_wav('music/enemy/husk_step.wav')
        self.attack_sound = load_wav('music/enemy/husk_chase.wav')
        self.find_sound = load_wav('music/enemy/husk_find.wav')
        self.death_sound1 = load_wav('music/enemy/enemy_death.wav')
        self.death_sound2 = load_wav('music/enemy/husk_death.wav')
        self.move_sound.set_volume(80)
        self.move_play = False
        self.find_play = False
        self.attack_play = False
        self.font = load_font('font.ttf', 16)
        self.turn = False
        self.move = True
        self.range_x1, self.range_x2 = None, None
        self.find = False
        self.attack = False
        self.attack_range = 150
        self.damage = False
        self.damage_count = False
        self.damage_back = 0
        self.hp = 3
        self.gravity = 0
        self.dead = False
        self.dead_back = None
    
    def update(self):
        
        self.cx = self.x - server.background.window_left
        self.cy = self.y - server.background.window_bottom
        
         # attack range
        if self.find == False and self.attack == False:
            if server.knight.y - 50 < self.y + 50:
                if server.knight.x > self.x - 400 and server.knight.x < self.x + 400:
                    if self.dir == 1:
                        if server.knight.x < self.x:
                            self.dir = -1
                        self.find = True
                        self.frame = 0
                    elif self.dir == -1:
                        if server.knight.x > self.x:
                            self.dir = 1
                        self.find = True
                        self.frame = 0
        
        if self.dead:
            self.hp = -1
            if int(self.frame) < 7:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
            
            if self.dead_back == None:
                if self.y > bottom:
                    self.gravity += 0.5
                    self.y -= self.gravity
                    self.dead_back = 3
                else:
                    self.y = bottom
                    self.gravity = 0
                    self.dead_back = 3
                self.death_sound1.play()
                # self.death_sound2.play()
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 0.5
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= bottom:
                    self.dead_back -= 1
                    self.gravity = 0
                
        elif self.move:
            if server.knight.x > self.x - 1000 and server.knight.x < self.x + 1000 and self.move_play == False:
                # self.move_sound.repeat_play()
                self.move_play = True
            else:
                # self.move_sound.stop()
                pass
            self.frame = (self.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7
            self.x += self.dir * 2
        
        if self.dead:
            pass
        
        elif self.damage_back > 0:
            self.x += server.knight.face_dir * 10
            self.damage_back -= 1
        
        elif self.find:
            if self.find_play == False:
                # self.find_sound.play()
                self.find_play = True
            
            self.move = False
            if self.attack == False:
    
                if int(self.frame) < 3:
                    self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                    
                else:
                    self.find = False
                    self.attack = True
                    self.frame = 0
        
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
                
            if self.attack:
                self.attack = False
                self.move = True
                    
        elif self.attack:
            if self.attack_play == False:
                # self.attack_sound.play()
                self.attack_play = True
            
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.x += self.dir * 5.5
            
            if self.dir == 1:
                if server.knight.y - 50 > self.y + 50 or server.knight.x < self.x or server.knight.x > self.x + 350:
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
                        
        range_check(self)
            
        if self.hp == 0:
            self.dead = True
            self.turn = False
            self.move = False
            self.frame = 0
            
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
        if self.dead == False:
            if group == 'spike:husk':
                if server.knight.attack:
                    if self.damage == False:
                        self.hp -= 1
                        self.damage_back = 5
                        self.damage = True
                else:
                    self.damage = False
    
class Vengefly:
    image_l = None
    image_r = None
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.dir = -1
        self.dir_y = 0.0
        if Vengefly.image_l == None:
            Vengefly.image_l = load_image('image/enemy/Vengefly_L.png')
        if Vengefly.image_r == None:
            Vengefly.image_r = load_image('image/enemy/Vengefly_R.png')
        self.move_sound = load_wav('music/enemy/vengefly_fly.wav')
        self.find_sound = load_wav('music/enemy/vengefly_find.wav')
        self.death_sound = load_wav('music/enemy/enemy_death.wav')
        self.move_sound.set_volume(80)
        self.font = load_font('font.ttf', 16)
        self.move_play = False
        self.find_play = False
        self.turn = False
        self.move = True
        self.range_x1, self.range_x2 = 0, 0
        self.find = False
        self.attack = False
        self.damage = False
        self.damage_back = 0
        self.hp = 2
        self.gravity = 0
        self.dead = False
        self.dead_back = None
    
    def update(self):
        
        self.cx = self.x - server.background.window_left
        self.cy = self.y - server.background.window_bottom
        
        if self.dead:
            self.hp = -1
            if int(self.frame) < 2:
                self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
            
            if self.dead_back == None:
                if self.y > bottom:
                    self.gravity += 0.5
                    self.y -= self.gravity
                    self.dead_back = 3
                else:
                    self.y = bottom
                    self.gravity = 0
                    self.dead_back = 3
                self.death_sound.play()
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 1
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= bottom:
                    self.dead_back -= 1
                    self.gravity = 0
                
        elif self.turn:
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
            if self.move_play == False:
                # self.move_sound.play()
                self.move_play = True
                
            self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
            self.x += self.dir * 5
            
        if self.dead:
            pass
        
        elif self.damage_back > 0:
            self.x += server.knight.face_dir * 10
            self.damage_back -= 1
        
        elif self.find:
            if self.find_play == False:
                # self.find_sound.play()
                self.find_play = True
            
            self.move = False
            if self.attack == False:
                
                if int(self.frame) < 3:
                    self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                
                else:
                    self.find = False
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
            if self.x + (300 * self.dir) < server.knight.x and self.y - 40 > bottom:
                self.y += self.dir_y * 3.5
            
        # attack range
        if self.find == False and self.attack == False:
            if server.knight.y + 30 > self.y - 400 and server.knight.y + 30 < self.y + 400:
                if server.knight.x > self.x - 400 and server.knight.x < self.x + 400:
                    self.find = True
                    self.frame = 0
            
        range_check(self)
            
        if self.hp == 0:
            self.dead = True
            self.turn = False
            self.move = False
            self.frame = 0
            
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
    
    dmg = False
    
    def handle_collision(self, other, group):
        if self.dead == False:
            if group == 'spike:vengefly':
                if server.knight.attack:
                    if self.damage == False:
                        self.hp -= 1
                        self.damage_back = 5
                        self.damage = True
                else:
                    self.damage = False
                    
def range_check(self):
    
    if self.attack == False:
        if self.x < self.range_x1 or self.x > self.range_x2:
            self.frame = 0
            self.turn = True
            self.move = False
    else:
        self.range_x1 = left
        self.range_x2 = right
    
    if self.x > right:
        self.x = right
        self.turn = True
    elif self.x < left:
        self.x = left
        self.turn = True
        
    if self.y > top:
        self.y = top
    elif self.y < bottom:
        self.y = bottom