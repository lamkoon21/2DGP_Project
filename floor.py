from pico2d import draw_rectangle
import server

class Floor:
    def __init__(self):
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
          
    def update(self):
        pass 

    def draw(self):
        if server.collide_box:
                draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.x1, self.y1, self.x2, self.y2
    
    def handle_collision(self, other, group):
        pass