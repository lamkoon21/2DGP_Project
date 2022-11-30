from pico2d import draw_rectangle
import server

class Wall:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.left, self.bottom, self.right, self.top = 0, 0, 0, 0
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        
        
    def update(self):
        self.left, self.top = self.x1 - server.background.window_left, self.y1 - server.background.window_bottom
        self.right, self.bottom = self.x2 - server.background.window_left, self.y2 - server.background.window_bottom 

    def draw(self):
        if server.collide_box:
                draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.left, self.bottom, self.right, self.top
    
    def handle_collision(self, other, group):
        pass