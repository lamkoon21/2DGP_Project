from pico2d import *
import ingame
import game_framework

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
        self.dead = False
        
        self.damage_time = 150
        self.no_dmg_time = 300
        
        self.dash_count = 0
        
        self.gravity = 0.0
        self.hp = 5
        self.soul = 0
    
    def update(self):
        # action status
        if self.damage:
            
            
            self.frame = 0
            
            self.damage_time -= 1
            if self.damage_time == 0:
                self.damage = False 
                self.no_dmg = True
                self.damage_time = 150
                
        elif self.attack:
            if self.attack_2:
                self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5 + 5
                if int(self.frame) == 9:
                    self.attack = False
                    self.attack_2 = False
                    self.frame = 0
            else:
                self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5
                if int(self.frame) == 4:
                    self.attack = False
                    self.attack_2 = True
                    self.frame = 0
                    
            if self.move:
                self.x += self.dir * 4
            
            if self.fall or self.jump:
                self.gravity += 0.2
                self.y += (10 - self.gravity)
            else:
                # self.x += self.dir * -1
                pass
                
        elif self.fall:
            if int(self.frame) < 7:
                self.frame = (self.gravity // 4) % 8 + 4
            else:
                self.frame = 7
                
            if self.move:
                self.x += self.dir * 4
                        
            self.gravity += 0.2
            self.y += (10 - self.gravity)
                
        elif self.jump:
            if int(self.frame) < 7:
                self.frame = (self.gravity // 4) % 8
            else:
                self.frame = 7
                
            if self.move:
                self.x += self.dir * 4
                
            if self.y + (30 - self.gravity) > 0:
                self.gravity += 0.2
                self.y += (10 - self.gravity)
            else:
                self.jump = False
                self.fall = True    
            
        elif self.move:
            if self.dash == False:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
                self.x += self.dir * 4
                
        if self.no_dmg:
            self.no_dmg_time -= 1
            if self.no_dmg_time == 0:
                self.no_dmg = False
                self.no_dmg_time = 300
                
        if self.dash:
            if self.damage == False:
                self.jump = False
            
                if int(self.frame) < 10 and self.fall == False:
                    self.frame = (self.frame + 11 * ACTION_PER_TIME * game_framework.frame_time) % 11
                    self.x += int(self.dir * (-((int(self.frame) % 11) - 3) ** 2 + 40) * 0.35)
                else:
                    if self.y > BOTTOM:
                        if self.fall == False:
                            self.frame = 0
                            self.gravity = 10
                            self.fall = True
                    if self.y <= BOTTOM:
                        self.frame = 0
                        self.dash = False
                        self.dash_count = 0
                        
                        
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
            if ingame.collide_box:
                draw_rectangle(*self.get_bb())
            if self.damage:
                self.image_r.clip_draw(int(self.frame) * 128 + 5, 560, 130, 130, self.x, self.y)
            elif self.attack:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 415, 125, 130, self.x - 20, self.y)
            elif self.fall:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 100, 120, self.x, self.y)        
            elif self.dash:
                self.image_r.clip_draw(int(self.frame) * 280, 290, 280, 125, self.x - 95, self.y)
            elif self.jump:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 100, 120, self.x, self.y)
            elif self.move:
                self.image_r.clip_draw(int(self.frame) * 128 + 138, 15, 100, 120, self.x, self.y)
            else:
                self.image_r.clip_draw(10, 15, 100, 120, self.x, self.y)
                
        elif self.dir == -1:
            if ingame.collide_box:
                draw_rectangle(*self.get_bb())
            if self.damage:
                self.image_r.clip_draw(int(self.frame) * 128 + 5, 560, 130, 130, self.x, self.y)
            elif self.attack:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 415, 125, 130, self.x + 40, self.y)
            elif self.fall:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 100, 120, self.x, self.y)
            elif self.dash:
                self.image_l.clip_draw(3025 - int(self.frame) * 280, 290, 280, 125, self.x + 120, self.y)
            elif self.jump:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 100, 120, self.x, self.y)
            elif self.move:
                self.image_l.clip_draw(3180 - 138 - int(self.frame) * 128, 15, 100, 120, self.x, self.y)
            else:
                self.image_l.clip_draw(3170, 15, 100, 120, self.x, self.y)
    
    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
                if event.key != pico2d.SDLK_x:
                    self.attack_2 = False
                match event.key:
                    case pico2d.SDLK_LEFT:     # left
                        if self.move == False:
                            self.dir = -1
                            self.move = True
                        else:
                            self.move = False
                    case pico2d.SDLK_RIGHT:    # right
                        if self.move == False:
                            self.dir = 1
                            self.move = True
                        else:
                            self.move = False
                    case pico2d.SDLK_z:        # jump
                        if self.jump == False:
                            if self.frame != 0:
                                self.frame = 0
                            self.jump = True
                    case pico2d.SDLK_x:        # attack
                        if self.soul < 9:
                            self.soul += 1
                        if self.dash == False and self.attack == False:
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
                        self.move = True
                case pico2d.SDLK_RIGHT:    # right
                    if self.move == True:
                        self.move = False
                    else:
                        self.dir = -1
                        self.move = True
                        
    def get_bb(self):
        if self.dir == 1: return self.x - 23, self.y - 60, self.x + 33, self.y + 58
        else: return self.x - 15, self.y - 60, self.x + 43, self.y + 58
        
    def handle_collision(self, other, group):
        match group:
            case 'knight:crawlid':
                if self.damage == False and self.no_dmg == False:
                    if self.hp > 0:
                        self.hp -= 1
                    else: self.dead = True
                    self.damage = True
            case 'knight:husk':
                if self.damage == False and self.no_dmg == False:
                    if self.hp > 0:
                        self.hp -= 1
                    else: self.dead = True
                    self.damage = True
            case 'knight:vengefly':
                if self.damage == False and self.no_dmg == False:
                    if self.hp > 0:
                        self.hp -= 1
                    else: self.dead = True
                    self.damage = True
    
    