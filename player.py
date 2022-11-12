from pico2d import *
from constant_value import *
import ingame
import game_framework
import game_world
import random


class Knight:
    def __init__(self):
        self.x, self. y = None, None
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.image_l = load_image('image/knight/knight_L.png')
        self.image_r = load_image('image/knight/knight_R.png')
        self.dash_effect = load_image('image/knight/dash_effect.png')
        self.attack_effect = load_image('image/knight/attack_effect.png')
        self.no_damage = load_image('image/knight/no_damage.png')
        self.move_sound = load_music('music/knight/step.wav')
        self.move_sound.set_volume(80)
        self.jump_sound = load_music('music/knight/jump.wav')
        self.fall_sound = load_music('music/knight/falling.wav')
        self.land_sound = load_music('music/knight/land.wav')
        self.dash_sound = load_music('music/knight/dash.wav')
        self.damage_sound = load_music('music/knight/damage.wav')
        self.attack_sound1 = load_music('music/knight/sword_1.wav')
        self.attack_sound2 = load_music('music/knight/sword_2.wav')
        self.attack_sound3 = load_music('music/knight/sword_3.wav')
        self.attack_sound4 = load_music('music/knight/sword_4.wav')
        self.attack_sound5 = load_music('music/knight/sword_5.wav')
        self.hit_sound = load_music('music/enemy/enemy_damage.wav')
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
        self.heal = False
        
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
                        self.hit_sound.play()
                    self.attack_count = False
                    self.frame = 0
                    
            else:
                self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5
                    
                if int(self.frame) == 4:
                    self.attack = False
                    self.attack_2 = True
                    if self.attack_count:
                        self.soul += 1
                        self.hit_sound.play()
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
                self.fall_sound.play()
        
        elif self.heal:
            if self.dead == False and self.soul > 2 and self.hp < 5:
                self.soul -= 3
                self.hp += 1
            self.heal = False
            
        elif self.move:
            if self.dash == False:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
                self.x += self.dir * 6
                
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
            
        if self.no_dmg:
            self.no_dmg_time -= 1
            if self.no_dmg_time == 0:
                self.no_dmg = False
                self.no_dmg_time = 200
            
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
            self.fall_sound.stop()
            self.land_sound.play()
        elif self.y > BOTTOM and self.dash == False:
            self.fall = True
        elif self.y > TOP:
            self.y = TOP
            self.fall = True
            if self.all == False:
                self.fall_sound.play()
            

   
    def draw(self):
        cx, cy = self.x - ingame.background.window_left, self.y - ingame.background.window_bottom
        
        if self.face_dir == 1:
            if self.damage:
                self.image_r.clip_draw(5, 560, 130, 130, cx, cy)
            elif self.attack:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 415, 120, 130, cx - 20, cy)
                if int(self.frame) < 2 or 5 < int(self.frame) < 7:
                    self.attack_effect.clip_composite_draw(0, 0, 160, 120, 0, 'h', cx + self.face_dir * 80, cy, 220, 165)
                elif int(self.frame) < 4 or 5 < int(self.frame) < 9:
                    self.attack_effect.clip_composite_draw(160, 0, 140, 120, 0, 'h', cx + self.face_dir * 80, cy, 220, 165)
            elif self.fall:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 101, 120, cx, cy)        
            elif self.dash:
                self.image_r.clip_draw(int(self.frame) * 280, 290, 280, 126, cx - 95, cy)
                if 0 < int(self.frame) < 6:
                    self.dash_effect.clip_composite_draw(int(self.frame) * 360, 0, 360, 220, 0, 'h', cx + self.face_dir * - 200, cy - 20, 360, 220)
            elif self.jump:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 101, 120, cx, cy)
            elif self.map_open:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy)
            elif self.map_close:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy)
            elif self.move:
                self.image_r.clip_draw(int(self.frame) * 128 + 138, 15, 101, 120, cx, cy)
            elif self.idle:
                self.image_r.clip_draw(10, 15, 101, 120, cx, cy)    
            else:
                self.image_r.clip_draw(10, 15, 101, 120, cx, cy)
                
        elif self.face_dir == -1:
            if self.damage:
                self.image_r.clip_composite_draw(5, 560, 130, 130, 0, 'h', cx, cy, 130, 130)
            elif self.attack:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 415, 120, 130, cx + 40, cy)
                if int(self.frame) < 2 or 5 < int(self.frame) < 7:
                    self.attack_effect.clip_composite_draw(0, 0, 160, 120, 0, '', cx + self.face_dir * 60, cy, 220, 165)
                elif int(self.frame) < 4 or 5 < int(self.frame) < 9:
                    self.attack_effect.clip_composite_draw(160, 0, 140, 120, 0, '', cx + self.face_dir * 60, cy, 220, 165)
            elif self.fall:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 101, 120, cx, cy)
            elif self.dash:
                self.image_l.clip_draw(3025 - int(self.frame) * 280, 290, 280, 126, cx + 120, cy)
                if 0 < int(self.frame) < 6:
                    self.dash_effect.clip_composite_draw(int(self.frame) * 360, 0, 360, 220, 0, '', cx + self.face_dir * - 220, cy - 20, 360, 220)
            elif self.jump:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 101, 120, cx, cy)
            elif self.map_open:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy)
            elif self.map_close:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy)
            elif self.move:
                self.image_l.clip_draw(3180 - 138 - int(self.frame) * 128, 15, 101, 120, cx, cy)
            elif self.idle:
                self.image_l.clip_draw(3170, 15, 101, 120, cx, cy)
            else:
                self.image_l.clip_draw(3170, 15, 101, 120, self.x, cy)
                
        if self.no_dmg:
            self.no_damage.clip_draw(0, 0, 127, 125, cx, cy, 200, 200)
        
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
                            self.move_sound.repeat_play()
                        else:
                            self.move = False
                            self.move_sound.stop()
                    case pico2d.SDLK_RIGHT:    # right
                        if self.move == False:
                            self.dir = 1
                            if self.damage == False: self.face_dir = self.dir
                            self.move = True
                            self.move_sound.repeat_play()
                        else:
                            self.move = False
                            self.move_sound.stop()
                    case pico2d.SDLK_z:        # jump
                        if self.jump == False and self.dash == False:
                            if self.frame != 0:
                                self.frame = 0
                            self.jump = True
                            self.jump_sound.play()
                    case pico2d.SDLK_x:        # attack
                        if self.attack == False and self.dash == False:
                            if self.frame != 0:
                                self.frame = 0
                            self.attack = True
                            Knight.attack_sound(self)
                    case pico2d.SDLK_c:        # dash
                        if self.dash == False:
                            if self.dash_count < 1:
                                if self.frame != 0:
                                    self.frame = 0
                                self.jump = False
                                self.fall = False
                                self.dash_count += 1
                                self.dash = True
                                self.dash_sound.play()
                    case pico2d.SDLK_a:
                        if self.idle or self.move:
                            if self.heal == False:
                                self.heal = True
                            
        elif event.type == SDL_KEYUP:
            self.idle = True
            match event.key:
                    case pico2d.SDLK_LEFT:     # left
                        if self.move == True:
                            self.move = False
                            self.move_sound.stop()
                        else:
                            self.dir = 1
                            if self.damage == False: self.face_dir = self.dir
                            self.move = True
                            self.move_sound.repeat_play()
                    case pico2d.SDLK_RIGHT:    # right
                        if self.move == True:
                            self.move = False
                            self.move_sound.stop()
                        else:
                            self.dir = -1
                            if self.damage == False: self.face_dir = self.dir
                            self.move = True
                            self.move_sound.repeat_play()
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
                            self.damage_sound.play()
                        else: self.dead = True
            case 'knight:husk':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                            self.damage_sound.play()
                        else: self.dead = True
            case 'knight:vengefly':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                            self.damage_sound.play()
                        else: self.dead = True
    
    def attack_sound(self):
        if self.attack:
            n = random.randint(1, 5)
            
            match n:
                case 1: self.attack_sound1.play()
                case 2: self.attack_sound2.play()
                case 3: self.attack_sound3.play()
                case 4: self.attack_sound4.play()
                case 5: self.attack_sound5.play()
                    




                    
class Spike:
    def __init__(self):
        self.x, self.y = ingame.knight.x, ingame.knight.y
        self.hit_sound = load_music('music/enemy/enemy_damage.wav')

        
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
            if group == 'spike:crawlid':
                ingame.knight.attack_count = True
                
            if group == 'spike:husk':
                    ingame.knight.attack_count = True
                    
            if group == 'spike:vengefly':
                    ingame.knight.attack_count = True
