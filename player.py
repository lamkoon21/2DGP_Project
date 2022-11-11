from pico2d import *
import ingame
import game_framework
import game_world

BOTTOM = 400
TOP = 1050
LEFT = 30
RIGHT = 1890

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FALL_G = 16
G = 0.5

class Knight:
    def __init__(self):
        self.x, self. y = None, None
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.image_l = load_image('image/knight/knight_L.png')
        self.image_r = load_image('image/knight/knight_R.png')
        self.idle = False
        self.move = False
        self.fall = False
        self.jump = False
        self.dash = False
        self.attack = False
        self.attack_2 = False
        self.attack_count = False
        self.damage = False
        self.no_dmg = False
        self.dead = False
        self.map_open = False
        self.map_close = False
        
        self.damage_time = 100
        self.no_dmg_time = 200
        
        self.dash_count = 0
        
        self.gravity = 0.0
        self.hp = 5
        self.soul = 0
    
    def update(self):
        # action status
        if self.damage:
            self.damage_time -= 1
            if self.damage_time == 0:
                self.frame = 0
                if self.y > BOTTOM: self.gravity = FALL_G
                else: self.gravity = 0
                self.face_dir = self.dir
                self.damage_time = 100
                self.dash = False
                self.dash_count = 0
                self.jump = False
                self.fall = False
                self.attack = False
                self.damage = False
                self.no_dmg = True
                
        elif self.map_open:
            if int(self.frame) < 4:
                self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5
        
        elif self.map_close:
            if int(self.frame) < 7:
                self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5 + 3
            else:
                self.map_close = False
                self.frame = 0
                
        elif self.attack:
            if self.attack_2:
                self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5 + 5
                         
                if int(self.frame) == 9:
                    self.attack = False
                    self.attack_2 = False
                    if self.attack_count:
                        self.soul += 1
                    self.attack_count = False
                    self.frame = 0
                    
            else:
                self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5
                    
                if int(self.frame) == 4:
                    self.attack = False
                    self.attack_2 = True
                    if self.attack_count:
                        self.soul += 1
                    self.attack_count = False
                    self.frame = 0
                    
                    
            if self.move:
                self.x += self.dir * 6
            
            if self.fall or self.jump:
                self.gravity += G
                self.y += (FALL_G - self.gravity)
                
            if self.attack_count:
                self.x += self.dir * -3
                
        elif self.fall:
            if int(self.frame) < 7:
                self.frame = (self.gravity // 4) % 8 + 4
            else:
                self.frame = 7
                
            if self.move:
                self.x += self.dir * 6
                        
            self.gravity += G
            self.y += (FALL_G - self.gravity)
                
        elif self.jump:
            if int(self.frame) < 7:
                self.frame = (self.gravity // 4) % 8
            else:
                self.frame = 7
                
            if self.move:
                self.x += self.dir * 6
                
            if self.y + (FALL_G - self.gravity) > 0:
                self.gravity += G
                self.y += (FALL_G - self.gravity)
            else:
                self.jump = False
                self.fall = True    
            
        elif self.move:
            if self.dash == False:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
                self.x += self.dir * 6
                
        if self.no_dmg:
            self.no_dmg_time -= 1
            if self.no_dmg_time == 0:
                self.no_dmg = False
                self.no_dmg_time = 200
                
        if self.dash:
            if self.damage == False:
                self.jump = False
            
                if int(self.frame) < 10 and self.fall == False:
                    self.frame = (self.frame + 11 * ACTION_PER_TIME * game_framework.frame_time) % 11
                    self.x += int(self.dir * (-((int(self.frame) % 11) - 3) ** 2 + 40) * 0.6)
                else:
                    if self.y > BOTTOM:
                        if self.fall == False:
                            self.frame = 0
                            self.gravity = FALL_G
                            self.fall = True
                    if self.y <= BOTTOM:
                        self.frame = 0
                        self.dash = False
                        self.dash_count = 0
                        
        if self.move == False and self.fall == False and self.jump == False \
            and self.dash == False and self.attack == False and self.attack_2 == False \
            and self.attack_count == False and self.damage == False and self.dead == False:
                self.idle = True
        else:
            self.idle = False
            
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
        if self.face_dir == 1:
            if self.damage:
                self.image_r.clip_draw(5, 560, 130, 130, self.x, self.y)
            elif self.attack:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 415, 126, 130, self.x - 20, self.y)
            elif self.fall:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 101, 120, self.x, self.y)        
            elif self.dash:
                self.image_r.clip_draw(int(self.frame) * 280, 290, 280, 126, self.x - 95, self.y)
            elif self.jump:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 101, 120, self.x, self.y)
            elif self.map_open:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, self.x, self.y)
            elif self.map_close:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, self.x, self.y)
            elif self.move:
                self.image_r.clip_draw(int(self.frame) * 128 + 138, 15, 101, 120, self.x, self.y)
            elif self.idle:
                self.image_r.clip_draw(10, 15, 101, 120, self.x, self.y)    
            else:
                self.image_r.clip_draw(10, 15, 101, 120, self.x, self.y)
                
        elif self.face_dir == -1:
            if self.damage:
                self.image_r.clip_composite_draw(5, 560, 130, 130, 0, 'h', self.x, self.y, 130, 130)
            elif self.attack:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 415, 126, 130, self.x + 40, self.y)
            elif self.fall:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 101, 120, self.x, self.y)
            elif self.dash:
                self.image_l.clip_draw(3025 - int(self.frame) * 280, 290, 280, 126, self.x + 120, self.y)
            elif self.jump:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 101, 120, self.x, self.y)
            elif self.map_open:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, self.x, self.y)
            elif self.map_close:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, self.x, self.y)
            elif self.move:
                self.image_l.clip_draw(3180 - 138 - int(self.frame) * 128, 15, 101, 120, self.x, self.y)
            elif self.idle:
                self.image_l.clip_draw(3170, 15, 101, 120, self.x, self.y)
            else:
                self.image_l.clip_draw(3170, 15, 101, 120, self.x, self.y)
        
        if ingame.collide_box:
                draw_rectangle(*self.get_bb())




    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
                if event.key != pico2d.SDLK_x:
                    self.attack_2 = False
                match event.key:
                    case pico2d.SDLK_LEFT:     # left
                        if self.move == False:
                            self.dir = -1
                            if self.damage == False: self.face_dir = self.dir
                            self.move = True
                        else:
                            self.move = False
                    case pico2d.SDLK_RIGHT:    # right
                        if self.move == False:
                            self.dir = 1
                            if self.damage == False: self.face_dir = self.dir
                            self.move = True
                        else:
                            self.move = False
                    case pico2d.SDLK_z:        # jump
                        if self.jump == False and self.dash == False:
                            if self.frame != 0:
                                self.frame = 0
                            self.jump = True
                    case pico2d.SDLK_x:        # attack
                        if self.attack == False and self.dash == False:
                            if self.frame != 0:
                                self.frame = 0
                            self.attack = True
                    case pico2d.SDLK_c:        # dash
                        if self.dash == False:
                            if self.dash_count < 1:
                                if self.frame != 0:
                                    self.frame = 0
                                self.jump = False
                                self.fall = False
                                self.dash_count += 1
                                self.dash = True
        elif event.type == SDL_KEYUP:
            self.idle = True
            match event.key:
                case pico2d.SDLK_LEFT:     # left
                    if self.move == True:
                        self.move = False
                    else:
                        self.dir = 1
                        if self.damage == False: self.face_dir = self.dir
                        self.move = True
                case pico2d.SDLK_RIGHT:    # right
                    if self.move == True:
                        self.move = False
                    else:
                        self.dir = -1
                        if self.damage == False: self.face_dir = self.dir
                        self.move = True
                case pico2d.SDLK_z:
                    if self.jump == True and self.gravity < FALL_G:
                        if self.gravity < 5:
                            self.gravity = FALL_G - 5
                        else: self.gravity = FALL_G
                        
    def get_bb(self):
        if self.dir == 1: return self.x - 23, self.y - 60, self.x + 33, self.y + 58
        else: return self.x - 15, self.y - 60, self.x + 43, self.y + 58
        
    def handle_collision(self, other, group):
        match group:
            case 'knight:crawlid':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                        else: self.dead = True
            case 'knight:husk':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                        else: self.dead = True
            case 'knight:vengefly':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                        else: self.dead = True




                    
class Spike:
    def __init__(self):
        self.x, self.y = ingame.knight.x, ingame.knight.y
        
    def update(self):
        self.x, self.y = ingame.knight.x, ingame.knight.y
    
    def draw(self):
        if ingame.collide_box:
            draw_rectangle(*self.get_bb())
    
    def get_bb(self):
        if ingame.knight.face_dir == 1: return ingame.knight.x, ingame.knight.y - 40, ingame.knight.x + 120, ingame.knight.y + 40
        else: return ingame.knight.x, ingame.knight.y - 40, ingame.knight.x - 120, ingame.knight.y + 40
        
    def handle_collision(self, other, group):
        if ingame.knight.attack and other.dead == False:
            match group:
                case 'spike:crawlid':
                    ingame.knight.attack_count = True
                case 'spike:husk':
                    ingame.knight.attack_count = True
                case 'spike:vengefly':
                    ingame.knight.attack_count = True