from pico2d import *
import server
from constant_value import ex

class FixedBackground:
    
    def __init__(self):
        self.image = None
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.select_map = 0
        self.w = 0
        self.h = 0


    def draw(self):
        self.image.clip_draw_to_origin(
        self.window_left, self.window_bottom, 
        self.canvas_width, self.canvas_height, 0, 0)
        pass

    def update(self):
        self.w = self.image.w
        self.h = self.image.h
        match self.select_map:
            case 0:
                self.window_left = clamp(0, int(server.knight.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
                self.window_bottom = clamp(0, int(server.knight.y) - self.canvas_height//4, self.h - self.canvas_height - 1)
            case 2:
                self.window_left = clamp(0, int(server.knight.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
                self.window_bottom = clamp(0, int(server.knight.y) - self.canvas_height//4, self.h - self.canvas_height - 1)
            case 3:
                self.window_left = clamp(0, int(server.knight.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
                self.window_bottom = clamp(0, int(server.knight.y) - self.canvas_height//3, self.h - self.canvas_height - 500)
            case 4:
                self.window_left = clamp(0, int(server.knight.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
                self.window_bottom = clamp(0, 700, self.h - self.canvas_height - 500)
            case 5:
                self.window_left = clamp(0, int(server.knight.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
                if int(server.knight.x) < 4200:
                    self.window_bottom = clamp(0, int(server.knight.y) - self.canvas_height//2 + 200, self.h - self.canvas_height - 900)
                else: self.window_bottom = clamp(0, int(server.knight.y) - self.canvas_height//2 + 200, self.h - self.canvas_height - 500)
            case _:
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
