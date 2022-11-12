from pico2d import *
import ingame
import game_framework
import game_world

BOTTOM = 400
TOP = 1050
LEFT = 30
RIGHT = 1890

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Crawlid:
    image_l = None
    image_r = None
    def __init__(self):
        self.x, self. y = None, None
        self.frame = 0
        self.dir = 1
        if  Crawlid.image_l == None:
            Crawlid.image_l = load_image('image/enemy/Crawlid_L.png')
        if  Crawlid.image_r == None:
            Crawlid.image_r = load_image('image/enemy/Crawlid_R.png')
        # self.move_sound = load_music('music/enemy/crawlid.wav')
        # self.death_sound = load_music('music/enemy/enemy_death.wav')
        # self.move_sound.set_volume(80)
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
                # self.death_sound.play()
                if self.y > BOTTOM:
                    self.gravity += 0.5
                    self.y -= self.gravity
                    self.dead_back = 3
                else:
                    self.y = BOTTOM
                    self.gravity = 0
                    self.dead_back = 3
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 0.5
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= BOTTOM:
                    self.dead_back -= 1
                    self.gravity = 0
                    
        elif self.damage_back > 0:
            self.x += ingame.knight.face_dir * 10
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
            if ingame.knight.x > self.x - 1000 and ingame.knight.x < self.x + 1000 and self.sound_play == False:
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
        if ingame.collide_box:
            draw_rectangle(*self.get_bb())
            self.font.draw(self.x, self.y + 60, f'(HP: {self.hp})', (255, 255, 0))
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(345 - int(self.frame) * 130, 0, 140, 90, self.x, self.y - 20)
            elif self.turn:
                self.image_r.clip_draw(380 - int(self.frame) * 97, 259, 94, 80, self.x, self.y - 20)
            elif self.move:
                self.image_r.clip_draw(360 - int(self.frame) * 119, 365, 115, 80, self.x, self.y - 20)
            else:
                self.image_r.clip_draw(360 - int(self.frame) * 119, 365, 115, 80, self.x, self.y - 20)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(int(self.frame) * 125, 0, 135, 90, self.x, self.y - 20)
            elif self.turn:
                self.image_l.clip_draw(int(self.frame) * 97 + 3, 259, 94, 80, self.x, self.y - 20)
            elif self.move:
                self.image_l.clip_draw(int(self.frame) * 119 + 3, 365, 115, 80, self.x, self.y - 20)
            else:
                self.image_l.clip_draw(int(self.frame) * 119 + 3, 365, 115, 80, self.x, self.y - 20)
                
    def get_bb(self):
        return self.x - 50, self.y - 60, self.x + 50, self.y + 20
    
    def handle_collision(self, other, group):
        if self.dead == False:
            if group == 'spike:crawlid':
                if ingame.knight.attack:
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
        self.x, self. y = None, None
        self.frame = 0
        self.dir = -1
        if Husk.image_l == None:
            Husk.image_l = load_image('image/enemy/Husk_L.png')
        if Husk.image_r == None:
            Husk.image_r = load_image('image/enemy/Husk_R.png')
        # self.move_sound = load_music('music/enemy/husk_step.wav')
        # self.attack_sound = load_music('music/enemy/husk_chase.wav')
        # self.find_sound = load_music('music/enemy/husk_find.wav')
        # self.death_sound1 = load_music('music/enemy/enemy_death.wav')
        # self.death_sound2 = load_music('music/enemy/husk_death.wav')
        # self.move_sound.set_volume(80)
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
        
         # attack range
        if self.find == False and self.attack == False:
            if ingame.knight.y - 50 < self.y + 50:
                if ingame.knight.x > self.x - 400 and ingame.knight.x < self.x + 400:
                    if self.dir == 1:
                        if ingame.knight.x < self.x:
                            self.dir = -1
                        self.find = True
                        self.frame = 0
                    elif self.dir == -1:
                        if ingame.knight.x > self.x:
                            self.dir = 1
                        self.find = True
                        self.frame = 0
        
        if self.dead:
            self.hp = -1
            if int(self.frame) < 7:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
            
            if self.dead_back == None:
                if self.y > BOTTOM:
                    self.gravity += 0.5
                    self.y -= self.gravity
                    self.dead_back = 3
                else:
                    self.y = BOTTOM
                    self.gravity = 0
                    self.dead_back = 3
                # self.death_sound1.play()
                # self.death_sound2.play()
            elif self.dead_back > 0:
                self.x += (self.dead_back * 2)
                self.gravity += 0.5
                self.y += (self.dead_back * 2) - self.gravity
                if self.y <= BOTTOM:
                    self.dead_back -= 1
                    self.gravity = 0
                
        elif self.move:
            if ingame.knight.x > self.x - 1000 and ingame.knight.x < self.x + 1000 and self.move_play == False:
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
            self.x += ingame.knight.face_dir * 10
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
                if ingame.knight.y - 50 > self.y + 50 or ingame.knight.x < self.x or ingame.knight.x > self.x + 350:
                    if self.attack_range > 0:
                        self.attack_range -= abs(self.dir * 2)
                    else:
                        self.frame = 0
                        self.move = True
                        self.attack = False
                        self.attack_range = 150
            else:
                if ingame.knight.y - 50 > self.y + 50 or ingame.knight.x < self.x - 350 or ingame.knight.x > self.x:
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
        if ingame.collide_box:
            draw_rectangle(*self.get_bb())
            self.font.draw(self.x, self.y + 80, f'(HP: {self.hp})', (255, 255, 0))
            
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(975 - int(self.frame) * 140, 0, 140, 120, self.x, self.y - 5)
            elif self.turn:
                self.image_r.clip_draw(1009 - int(self.frame) * 105, 715, 105, 128, self.x, self.y)
            elif self.find:
                self.image_r.clip_draw(1002 - int(self.frame) * 118, 555, 110, 135, self.x, self.y)
            elif self.attack:
                self.image_r.clip_draw(990 - int(self.frame) * 125, 410, 125, 125, self.x, self.y)
            elif self.move:
                self.image_r.clip_draw(997 - int(self.frame) * 118, 865, 115, 127, self.x, self.y)
            else:
                self.image_r.clip_draw(997 - int(self.frame) * 118, 865, 115, 127, self.x, self.y)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(int(self.frame) * 140, 0, 140, 120, self.x, self.y - 5)
            elif self.turn:
                self.image_l.clip_draw(int(self.frame) * 105 + 5, 715, 105, 128, self.x, self.y)
            elif self.find:
                self.image_l.clip_draw(int(self.frame) * 118 + 3, 555, 110, 135, self.x, self.y)
            elif self.attack:
                self.image_l.clip_draw(int(self.frame) * 124 + 3, 410, 125, 125, self.x, self.y)
            elif self.move:
                self.image_l.clip_draw(int(self.frame) * 118 + 3, 865, 115, 130, self.x, self.y)
            else:
                self.image_l.clip_draw(int(self.frame) * 118 + 3, 865, 115, 130, self.x, self.y)
                
    def get_bb(self):
        return self.x - 50, self.y - 60, self.x + 50, self.y + 60
    
    def handle_collision(self, other, group):
        if self.dead == False:
            if group == 'spike:husk':
                if ingame.knight.attack:
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
        self.x, self. y = None, None
        self.frame = 0
        self.dir = -1
        self.dir_y = 0.0
        if Vengefly.image_l == None:
            Vengefly.image_l = load_image('image/enemy/Vengefly_L.png')
        if Vengefly.image_r == None:
            Vengefly.image_r = load_image('image/enemy/Vengefly_R.png')
        self.move_sound = load_music('music/enemy/vengefly_fly.wav')
        self.find_sound = load_music('music/enemy/vengefly_find.wav')
        self.death_sound = load_music('music/enemy/enemy_death.wav')
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
        if self.dead:
            self.hp = -1
            if int(self.frame) < 2:
                self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
            
            if self.dead_back == None:
                if self.y > BOTTOM:
                    self.gravity += 1
                    self.y -= self.gravity
                else:
                    self.y = BOTTOM
                    self.gravity = 0
                    self.dead_back = 3
                # self.death_sound.play()
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
            self.x += ingame.knight.face_dir * 10
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
                if ingame.knight.x < self.x:
                    self.dir = -1
            elif self.dir == -1:
                if ingame.knight.x > self.x:
                    self.dir = 1
                    
            if ingame.knight.y < self.y:
                self.dir_y = -1
            elif ingame.knight.y > self.y:
                self.dir_y = 1
                
            
            self.x += self.dir * 5
            if self.x + (300 * self.dir) < ingame.knight.x and self.y - 40 > BOTTOM:
                self.y += self.dir_y * 3.5
            
        # attack range
        if self.find == False and self.attack == False:
            if ingame.knight.y + 30 > self.y - 400 and ingame.knight.y + 30 < self.y + 400:
                if ingame.knight.x > self.x - 400 and ingame.knight.x < self.x + 400:
                    self.find = True
                    self.frame = 0
            
        range_check(self)
            
        if self.hp == 0:
            self.dead = True
            self.turn = False
            self.move = False
            self.frame = 0
            
    def draw(self):
        if ingame.collide_box:
            draw_rectangle(*self.get_bb())
            self.font.draw(self.x, self.y + 80, f'(HP: {self.hp})', (255, 255, 0))
            
        if self.dir == 1:
            if self.dead:
                self.image_r.clip_draw(455 - int(self.frame) * 150, 0, 150, 110, self.x, self.y - 25)
            elif self.turn:
                self.image_r.clip_draw(485 - int(self.frame) * 110, 465, 110, 140, self.x, self.y)
            elif self.find:
                self.image_r.clip_draw(470 - int(self.frame) * 160, 285, 160, 160, self.x, self.y)
            elif self.attack:
                self.image_r.clip_draw(460 - int(self.frame) * 150, 130, 150, 140, self.x, self.y)
            elif self.move:
                self.image_r.clip_draw(485 - int(self.frame) * 120, 635, 115, 140, self.x, self.y)
            else:
                self.image_r.clip_draw(485 - int(self.frame) * 120, 635, 115, 140, self.x, self.y)
                
        elif self.dir == -1:
            if self.dead:
                self.image_l.clip_draw(int(self.frame) * 150, 0, 150, 110, self.x, self.y - 25)
            elif self.turn:
                self.image_l.clip_draw(int(self.frame) * 110, 465, 115, 140, self.x, self.y)
            elif self.find:
                self.image_l.clip_draw(int(self.frame) * 150, 285, 150, 160, self.x, self.y)
            elif self.attack:
                self.image_l.clip_draw(int(self.frame) * 145, 130, 150, 140, self.x, self.y)
            elif self.move:
                self.image_l.clip_draw(int(self.frame) * 120 + 5, 635, 115, 140, self.x, self.y)
            else:
                self.image_l.clip_draw(int(self.frame) * 120 + 5, 635, 115, 140, self.x, self.y)
                
    def get_bb(self):
        return self.x - 50, self.y - 60, self.x + 50, self.y + 50
    
    dmg = False
    
    def handle_collision(self, other, group):
        if self.dead == False:
            if group == 'spike:vengefly':
                if ingame.knight.attack:
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