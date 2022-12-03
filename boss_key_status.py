from pico2d import *
import game_framework
import game_world
from constant_value import *
import server

class Bosskey_status:
    def __init__(self, x, y, num):
        self.status1 = load_image('image/map/boss_key_status1.png')
        self.status2 = load_image('image/map/boss_key_status2.png')
        self.status3 = load_image('image/map/boss_key_status3.png')
        self.status4 = load_image('image/map/boss_key_status4.png')
        self.effect = load_image('image/map/key_piece_glow.png')
        self.x, self.y = x, y
        self.frame = 0
        self.num = num
          
    def update(self):
        self.frame = (self.frame + 6 * ACTION_PER_TIME * game_framework.frame_time * 0.65) % 6

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
            
        self.effect.clip_draw(200 * int(self.frame), 0, 200, 200, cx, cy)
        match self.num:
            case 0:
                self.status1.clip_draw(0, 0, 120, 163, cx, cy)
            case 1:
                self.status2.clip_draw(0, 0, 113, 150, cx, cy)
            case 2:
                self.status3.clip_draw(0, 0, 113, 150, cx, cy)
            case 3:
                self.status4.clip_draw(0, 0, 113, 150, cx, cy)
        
    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        return cx - 50, cy - 50, cx + 50, cy + 50
    
    def handle_collision(self, other, group):
        pass