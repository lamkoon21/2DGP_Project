from pico2d import *
import server
from constant_value import ex

class FixedBackground:
    
    def __init__(self):
        self.map0 = load_image('image/map/map0.png')
        self.map1 = load_image('image/map/map1.png')
        self.map2 = None
        self.map3 = None
        self.map4 = None
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.select_map = 0
        self.w = 0
        self.h = 0


    def draw(self):
        match self.select_map:
            case 0:
                self.map0.clip_draw_to_origin(
                self.window_left, self.window_bottom, 
                self.canvas_width, self.canvas_height, 0, 0)
            case 1:
                self.map1.clip_draw_to_origin(
                self.window_left, self.window_bottom, 
                self.canvas_width, self.canvas_height, 0, 0, 1920, 1080)
            case 2:
                self.map2.clip_draw_to_origin(
                self.window_left, self.window_bottom, 
                self.canvas_width, self.canvas_height, 0, 0)
            case 3:
                self.map3.clip_draw_to_origin(
                self.window_left, self.window_bottom, 
                self.canvas_width, self.canvas_height, 0, 0)
            case 4:
                self.map4.clip_draw_to_origin(
                self.window_left, self.window_bottom, 
                self.canvas_width, self.canvas_height, 0, 0)

    def update(self):
        match self.select_map:
            case 0:
                self.w = self.map0.w
                self.h = self.map0.h
            case 1:
                self.w = self.map1.w
                self.h = self.map1.h
            case 2:
                self.w = self.map2.w
                self.h = self.map2.h
            case 3:
                self.w = self.map3.w
                self.h = self.map3.h
            case 4:
                self.w = self.map4.w
                self.h = self.map4.h
        
        self.window_left = clamp(0, int(server.knight.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.canvas_height//2, self.h - self.canvas_height - 1)

    def handle_event(self, event):
        pass
    
class TileBackground:
    
    def __init__(self):
        # self.map0 = [ load_image('image/map/map0_%d.png' % x) for x in range(3)]
        # self.map0 = [ [ load_image('image/map/output/map0_%d.png' % (x, y)) for x in range(5)] for y in range(2)]
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.select_map = 0
        self.w = 0
        self.h = 0
        

    def update(self):
        match self.select_map:
            case 0:
                self.w = self.map1.w * 5
                self.h = self.map1.h * 2

    def draw(self):
        self.window_left = clamp(0, int(server.knight.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.canvas_height//2, self.h - self.canvas_height - 1)
        
        tile_left = self.window_left // 800
        tile_right = (self.window_left + self.canvas_width) // 800
        left_offset = self.window_left % 800
        
        tile_bottom = self.window_bottom // 600
        tile_top = (self.window_bottom + self.canvas_height) // 600
        bottom_offset = self.window_bottom % 600
        
        for ty in range(tile_bottom, tile_top + 1):
            for tx in range(tile_left, tile_right + 1):
                self.tiles[ty][tx].draw_to_origin(-left_offset + (tx - tile_left) * 1920, -bottom_offset + (ty - tile_bottom) * 1080)
        pass
