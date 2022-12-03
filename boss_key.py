from pico2d import *
import game_framework
import game_world
from constant_value import *
import server

class Bosskey:
    def __init__(self, x, y):
        self.image = None
        self.effect = load_image('image/map/key_piece_glow.png')
        self.x, self.y = x, y
        self.frame = 0
          
    def update(self):
        self.frame = (self.frame + 6 * ACTION_PER_TIME * game_framework.frame_time * 0.65) % 6

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        if server.collide_box:
            draw_rectangle(*self.get_bb())
            
        self.effect.clip_draw(200 * int(self.frame), 0, 200, 200, cx, cy)
        self.image.clip_draw(0, 0, 150, 150, cx, cy)
        
    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        return cx - 50, cy - 50, cx + 50, cy + 50
    
    def handle_collision(self, other, group):
        if group == 'knight:boss_key':
            game_world.remove_object(self)
            if server.current_stage == 0:
                server.key_in_stage[0] = 1
            elif server.current_stage == 3:
                server.key_in_stage[1] = 1
            elif server.current_stage == 6:
                server.key_in_stage[2] = 1