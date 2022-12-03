from pico2d import *
from constant_value import *
import server
import game_framework
import game_world
import random
from wall import Wall


class Knight:
    def __init__(self, x, y, face_dir, move, hp, soul, boss_key):
        self.x, self. y = x, y
        self.frame = 0
        self.dir = 0
        self.face_dir = face_dir
        self.image_l = load_image('image/knight/knight_L.png')
        self.image_r = load_image('image/knight/knight_R.png')
        self.dash_effect = load_image('image/knight/dash_effect.png')
        self.attack_effect = load_image('image/knight/attack_effect.png')
        self.no_damage = load_image('image/knight/no_damage.png')
        self.fade_out = load_image('image/knight/fade_out.png')
        self.move_sound = load_wav('music/knight/step.wav')
        self.move_sound.set_volume(80)
        self.jump_sound = load_wav('music/knight/jump.wav')
        self.fall_sound = load_wav('music/knight/falling.wav')
        self.land_sound = load_wav('music/knight/land.wav')
        self.dash_sound = load_wav('music/knight/dash.wav')
        self.damage_sound = load_wav('music/knight/damage.wav')
        self.attack_sound1 = load_wav('music/knight/sword_1.wav')
        self.attack_sound2 = load_wav('music/knight/sword_2.wav')
        self.attack_sound3 = load_wav('music/knight/sword_3.wav')
        self.attack_sound4 = load_wav('music/knight/sword_4.wav')
        self.attack_sound5 = load_wav('music/knight/sword_5.wav')
        self.hit_sound = load_wav('music/enemy/enemy_damage.wav')
        self.save_sound = load_wav('music/ui/save.wav')
        self.death_sound = load_music('music/knight/death.wav')
        self.font = load_font('font.ttf', 16)
        self.idle = False
        self.move = move
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
        self.dead = False
        
        self.collide_bottom = False
        self.collide_top = False
        self.collide_left = False
        self.collide_right = False
        
        self.enter_boss = False
        self.save = False
        
        self.damage_time = 50
        self.no_dmg_time = 100
        self.damage_back = None
        
        self.dash_count = 0
        
        self.gravity = 0.0
        self.hp = hp
        self.soul = soul
        self.boss_key = boss_key
    
    def update(self):
        
        if self.dead:
            self.hp = -1
            self.death_sound.play()
            if int(self.frame) < 9:
                self.frame = (self.frame + 10 * ACTION_PER_TIME * game_framework.frame_time / 2) % 10
            else:
                delay(1)
                with open('knight_data.json', 'r') as f:
                    data = json.load(f)
                    data["hp"] = 5
                    data["soul"] = 0
                with open('knight_data.json', 'w') as f:
                    json.dump(data, f, indent="\t")
                    
                if server.save_point == 1:
                    server.current_stage = 'respawn1'
                elif server.save_point == 2:
                    server.current_stage = 'respawn2'
                else:
                    server.current_stage = 'respawn2_boss'
            
        
        # action status
        elif self.damage:
            self.damage_time -= 1
            if self.damage_time == 0:
                with open('knight_data.json', 'r') as f:
                    data = json.load(f)
                    data["hp"] = self.hp
                with open('knight_data.json', 'w') as f:
                    json.dump(data, f, indent="\t")
                self.frame = 0
                self.face_dir = self.dir
                self.damage_time = 50
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
                        if self.soul < 9: self.soul += 1
                        with open('knight_data.json', 'r') as f:
                            data = json.load(f)
                            data["soul"] = self.soul
                        with open('knight_data.json', 'w') as f:
                            json.dump(data, f, indent="\t")
                        self.hit_sound.play()
                    self.attack_count = False
                    self.frame = 0
                    
            else:
                self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time * 2) % 5
                    
                if int(self.frame) == 4:
                    self.attack = False
                    self.attack_2 = True
                    if self.attack_count:
                        if self.soul < 9: self.soul += 1
                        with open('knight_data.json', 'r') as f:
                            data = json.load(f)
                            data["soul"] = self.soul
                        with open('knight_data.json', 'w') as f:
                            json.dump(data, f, indent="\t")
                        self.hit_sound.play()
                    self.attack_count = False
                    self.frame = 0
                    
                    
            if self.move:
                self.x += self.dir * 6
                self.face_dir = self.dir
            
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
                self.face_dir = self.dir
                
            self.gravity += G
            self.y += (FALL_G - self.gravity)
                
        elif self.jump:
            if int(self.frame) < 7:
                self.frame = (self.gravity // 4) % 8
            else:
                self.frame = 7
                
            if self.move:
                self.x += self.dir * 6
                self.face_dir = self.dir
                
            if self.y + (FALL_G - self.gravity) > 0:
                self.gravity += G
                self.y += (FALL_G - self.gravity)
            else:
                self.jump = False
                self.fall = True
                # self.fall_sound.play()
        
        elif self.heal:
            if self.dead == False and self.soul > 2 and self.hp < 5:
                self.soul -= 3
                self.hp += 1
            self.heal = False
            
        elif self.move:
            if self.dash == False:
                self.face_dir = self.dir
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
                self.x += self.dir * 6
                
        if self.dash:
            if self.damage == False:
                self.jump = False
            
                if int(self.frame) < 10 and self.fall == False:
                    self.frame = (self.frame + 11 * ACTION_PER_TIME * game_framework.frame_time) % 11
                    self.x += int(self.face_dir * (-((int(self.frame) % 11) - 3) ** 2 + 40) * 0.6)
                elif int(self.frame) == 10:
                    self.dash = False
                        
                        
        if self.move == False and self.fall == False and self.jump == False \
            and self.dash == False and self.attack == False and self.attack_2 == False \
            and self.damage == False and self.dead == False:
                self.idle = True
        else:
            self.idle = False
            
        if self.no_dmg:
            self.no_dmg_time -= 1
            if self.damage_back == None:
                self.damage_back = 15
            if self.damage_back > 0:
                self.x -= self.face_dir * self.damage_back
                self.y += self.damage_back
                self.damage_back -= 1
            
            if self.no_dmg_time == 0:
                self.no_dmg = False
                self.no_dmg_time = 100
                self.damage_back = None
                
        if self.dash == False and self.jump == False:
            if self.collide_bottom == False and self.collide_top == False:
                if self.fall == False:
                    self.gravity = FALL_G
                self.fall = True
            else:
                if self.fall == False:
                    self.dash_count = 0
                self.fall = False
                
        if self.hp == 0:
            self.dead = True
            self.frame = 0
   
    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
                
        if self.face_dir == 1:
            if self.damage:
                self.image_r.clip_draw(5, 560, 130, 130, cx, cy)
            elif self.attack:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 415, 120, 130, cx - 20, cy, 120 * ex, 130 * ex)
                if int(self.frame) < 2 or 5 < int(self.frame) < 7:
                    self.attack_effect.clip_composite_draw(0, 0, 160, 120, 0, 'h', cx + self.face_dir * 80, cy, 220 * ex, 165 * ex)
                elif int(self.frame) < 4 or 5 < int(self.frame) < 9:
                    self.attack_effect.clip_composite_draw(160, 0, 140, 120, 0, 'h', cx + self.face_dir * 80, cy, 220 * ex, 165 * ex)
            elif self.fall:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 101, 120, cx, cy, 101 * ex, 120 * ex)        
            elif self.dash:
                self.image_r.clip_draw(int(self.frame) * 280, 290, 280, 126, cx - 95, cy, 280 * ex, 126 * ex)
                if 0 < int(self.frame) < 6:
                    self.dash_effect.clip_composite_draw(int(self.frame) * 360, 0, 360, 220, 0, 'h', cx + self.face_dir * - 200, cy - 20, 360 * ex, 220 * ex)
            elif self.jump:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 145, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.map_open:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.map_close:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.move:
                self.image_r.clip_draw(int(self.frame) * 128 + 138, 15, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.idle:
                self.image_r.clip_draw(10, 15, 101, 120, cx, cy, 101 * ex, 120 * ex)    
            else:
                self.image_r.clip_draw(10, 15, 101, 120, cx, cy, 101 * ex, 120 * ex)
                
        else:
            if self.damage:
                self.image_r.clip_composite_draw(5, 560, 130, 130, 0, 'h', cx, cy, 130, 130)
            elif self.attack:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 415, 120, 130, cx + 40, cy, 120 * ex, 130 * ex)
                if int(self.frame) < 2 or 5 < int(self.frame) < 7:
                    self.attack_effect.clip_composite_draw(0, 0, 160, 120, 0, '', cx + self.face_dir * 60, cy, 220 * ex, 165 * ex)
                elif int(self.frame) < 4 or 5 < int(self.frame) < 9:
                    self.attack_effect.clip_composite_draw(160, 0, 140, 120, 0, '', cx + self.face_dir * 60, cy, 220 * ex, 165 * ex)
            elif self.fall:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.dash:
                self.image_l.clip_draw(3025 - int(self.frame) * 280, 290, 280, 126, cx + 120, cy, 280 * ex, 126 * ex)
                if 0 < int(self.frame) < 6:
                    self.dash_effect.clip_composite_draw(int(self.frame) * 360, 0, 360, 220, 0, '', cx + self.face_dir * - 220, cy - 20, 360 * ex, 220 * ex)
            elif self.jump:
                self.image_l.clip_draw(3180 - 10 - int(self.frame) * 128, 145, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.map_open:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.map_close:
                self.image_r.clip_draw(int(self.frame) * 128 + 10, 898, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.move:
                self.image_l.clip_draw(3180 - 138 - int(self.frame) * 128, 15, 101, 120, cx, cy, 101 * ex, 120 * ex)
            elif self.idle:
                self.image_l.clip_draw(3170, 15, 101, 120, cx, cy , 101 * ex, 120 * ex)
            else:
                self.image_l.clip_draw(3170, 15, 101, 120, cx, cy , 101 * ex, 120 * ex)
                
        if self.no_dmg:
            self.no_damage.clip_draw(0, 0, 127, 125, cx + 10, cy, 200 * ex, 200 * ex)
        
        if server.collide_box:
            draw_rectangle(*self.get_bb())
            self.font.draw(cx, cy + 80, f'(x: {self.x}, y: {self.y})', (255, 255, 0))




    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
                if event.key != pico2d.SDLK_x:
                    self.attack_2 = False
                match event.key:
                    case pico2d.SDLK_LEFT:     # left
                        if self.move == False:
                            self.dir = -1
                            if self.damage == False: 
                                if self.dash == False: self.face_dir = self.dir
                            self.move = True
                        else:
                            self.move = False
                            
                    case pico2d.SDLK_RIGHT:    # right
                        if self.move == False:
                            self.dir = 1
                            if self.damage == False: 
                                if self.dash == False: self.face_dir = self.dir
                            self.move = True
                        else:
                            self.move = False
                            
                    case pico2d.SDLK_z:        # jump
                        if self.jump == False and self.dash == False:
                            if self.frame != 0:
                                self.frame = 0
                            self.jump = True
                            if self.damage == False: 
                                self.jump_sound.play()
                                
                    case pico2d.SDLK_x:        # attack
                        if self.attack == False and self.dash == False:
                            if self.frame != 0:
                                self.frame = 0
                            self.attack = True
                            if self.damage == False: 
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
                                if self.damage == False: 
                                    self.dash_sound.play()
                                    
                    case pico2d.SDLK_a:        # heal
                        if self.idle or self.move:
                            if self.heal == False:
                                self.heal = True
                    
                    case pico2d.SDLK_UP:
                        if server.current_stage == 2 and self.boss_key == 3:
                            self.enter_boss = True
                        if server.current_stage == 0 or server.current_stage == 6:
                            self.save = True
                                
                with open('knight_data.json', 'r') as f:
                    data = json.load(f)
                    data["move"] = self.move
                with open('knight_data.json', 'w') as f:
                    json.dump(data, f, indent="\t")
                            
        elif event.type == SDL_KEYUP:
            self.idle = True
            match event.key:
                    case pico2d.SDLK_LEFT:     # left
                        if self.move == True:
                            self.move = False
                        else:
                            self.dir = 1
                            # if self.damage == False: 
                                # if self.y == bottom:
                                #     self.move_sound.repeat_play()
                            self.move = True
                            
                    case pico2d.SDLK_RIGHT:    # right
                        if self.move == True:
                            self.move = False
                        else:
                            self.dir = -1
                            # if self.damage == False: 
                                # if self.y == bottom:
                                #     self.move_sound.repeat_play()
                            self.move = True
                            
                    case pico2d.SDLK_z:
                        if self.jump == True and self.gravity < FALL_G:
                            if self.gravity < 5:
                                self.gravity = FALL_G - 5
                            else: self.gravity = FALL_G
                    
                    case pico2d.SDLK_UP:
                        if server.current_stage == 2:
                            self.enter_boss = False
                        if server.current_stage == 0 or server.current_stage == 6:
                            self.save = False
                            
            with open('knight_data.json', 'r') as f:
                data = json.load(f)
                data["move"] = self.move
            with open('knight_data.json', 'w') as f:
                json.dump(data, f, indent="\t")
                        
    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        
        if self.face_dir == 1: return cx - 20, cy - 60, cx + 33, cy + 40
        else: return cx - 15, cy - 60, cx + 38, cy + 40
        
    def handle_collision(self, other, group):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        
        if self.face_dir == 1:
            left, bottom, right, top = cx - 20, cy - 60, cx + 33, cy + 40
        else:
            left, bottom, right, top = cx - 15, cy - 60, cx + 38, cy + 40
        match group:
            case 'knight:wall':
                if other.top > bottom and other.top - bottom < 50:
                    if self.fall or self.jump:
                        self.frame = 0
                        self.gravity = 0
                        self.fall = False
                        self.jump = False
                        # self.land_sound.play()
                    self.y = other.y1 + 60
                    
                elif other.bottom < top and top - other.bottom < 50:
                    if self.fall or self.jump:
                        self.frame = 0
                        self.gravity = FALL_G
                        self.fall = False
                        self.jump = False
                        # self.fall_sound.play()
                    self.y = other.y2 - 60
                    
                if other.top - bottom > 30 or other.bottom - top > 50:
                    if other.right > left and other.right - left < 50:
                        self.x += self.dir * 6
                        if self.face_dir == 1:
                            self.x = other.x2 + 20
                        else: 
                            self.x = other.x2 + 15
                    
                    elif other.left < right and right - other.left < 50:
                        self.x += self.dir * 6
                        if self.face_dir == 1: 
                            self.x = other.x1 - 33
                        else: 
                            self.x = other.x1 - 38
                    
                    
                if self.y == other.y1 + 60:
                    self.collide_bottom = True
                if self.y == other.y2 - 60:
                    self.collide_top = True
                if self.x == other.x2 + 23 or self.x == other.x2 + 15:
                    self.collide_left = True
                if self.x == other.x1 - 33 or self.x == other.x2 - 43:
                    self.collide_right = True
                    
            case 'knight:gate':
                stage, index = other.stage, other.index
                with open('knight_data.json', 'r') as f:
                    data = json.load(f)
                match stage:
                    case 0:
                        server.pre_stage = 0
                        if index == 1:
                            server.current_stage = 1
                    case 1:
                        server.pre_stage = 1
                        if index == 1:
                            server.current_stage = 0
                        if index == 2:
                            server.current_stage = 2
                        if index == 3:
                            server.current_stage = 3
                    case 2:
                        server.pre_stage = 2
                        if index == 1:
                            server.current_stage = 1
                        if index == 2:
                            if self.enter_boss:
                                server.current_stage = 'boss'
                    case 3:
                        server.pre_stage = 3
                        if index == 1:
                            server.current_stage = 1
                        if index == 2:
                            server.current_stage = 4
                    case 4:
                        server.pre_stage = 4
                        if index == 1:
                            server.current_stage = 3
                        if index == 2:
                            server.current_stage = 5
                    case 5:
                        server.pre_stage = 5
                        if index == 1:
                            server.current_stage = 4
                        if index == 2:
                            server.current_stage = 6
                    case 6:
                        server.pre_stage = 6
                        if index == 1:
                            server.current_stage = 5
                        if index == 2:
                            server.current_stage = 7
                    case 7:
                        server.pre_stage = 7
                        if index == 1:
                            server.current_stage = 6
                    case 'boss':
                        server.pre_stage = 'boss'
                        server.current_stage = 2
                    
                    
            case 'knight:crawlid':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                            self.damage_sound.play()
            case 'knight:husk':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                            self.damage_sound.play()
                            
            case 'knight:vengefly':
                if other.dead == False:
                    if self.damage == False and self.no_dmg == False:
                        if self.hp > 0:
                            self.hp -= 1
                            self.damage = True
                            self.gravity = 10
                            self.damage_sound.play()
            case 'knight:thorn':
                if self.damage == False and self.no_dmg == False:
                    if self.hp > 0:
                        self.hp -= 1
                        self.damage = True
                        self.gravity = 10
                        self.damage_sound.play()
                    else: 
                        self.dead = True
                        self.frame = 0
                        
            case 'knight:boss_key':
                self.boss_key += 1
                with open('knight_data.json', 'r') as f:
                    data = json.load(f)
                    data["boss_key"] = self.boss_key
                with open('knight_data.json', 'w') as f:
                    json.dump(data, f, indent="\t")
            
            case 'knight:save_bench':
                if self.save:
                    if server.current_stage == 0 and server.save_point != 1:
                        server.save_point = 1
                        self.save_sound.play()
                    elif server.current_stage == 6 and server.save_point != 2:
                        server.save_point = 2
                        self.save_sound.play()
    
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
        self.x, self.y = 0, 0
        self.hit_sound = load_wav('music/enemy/enemy_damage.wav')

        
    def update(self):
        self.x, self.y = server.knight.x - server.background.window_left, server.knight.y - server.background.window_bottom
    
    def draw(self):
        if server.collide_box:
            draw_rectangle(*self.get_bb())
    
    def get_bb(self):        
        if server.knight.face_dir == 1: 
            return self.x, self.y - 40, self.x + 140, self.y + 40
        else: 
            return self.x - 140, self.y - 40, self.x, self.y + 40
        
    def handle_collision(self, other, group):
        if server.knight.attack and other.dead == False:
            if group == 'spike:crawlid':
                server.knight.attack_count = True
                
            if group == 'spike:husk':
                    server.knight.attack_count = True
                    
            if group == 'spike:vengefly':
                    server.knight.attack_count = True
