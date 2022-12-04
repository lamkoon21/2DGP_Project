from pico2d import draw_rectangle, load_font
import server

class Savebench:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.left, self.bottom, self.right, self.top = 0, 0, 0, 0
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        
        self.font = load_font('font.ttf', 32)
        self.write = False
        
        
    def update(self):
        self.left, self.top = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        self.right, self.bottom = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom
        
        if server.knight.x < self.x2 and server.knight.x > self.x1:
            self.write = True
        else: self.write = False

    def draw(self):
        if server.collide_box:
            draw_rectangle(*self.get_bb())
        
        if self.write:
            self.font.draw((self.left+ self.right) / 2 - 80, self.top + 100, f'SAVE POINT', (255,255,255))
        
    def get_bb(self):
        return self.left, self.bottom, self.right, self.top
    
    def handle_collision(self, other, group):
        pass