from pico2d import *
import game_framework
import title

class Control:
    def __init__(self):
        self.image = load_image('image/title/control.png')
    
    def update(self):
        pass
        
    def draw(self):
        self.image.draw(960, 540)

def handle_events():
    global control
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, pico2d.SDLK_RETURN):
            title.title.confirm.play()
            game_framework.pop_state()    
        elif (event.type, event.key) == (SDL_KEYDOWN, pico2d.SDLK_ESCAPE):
            title.title.confirm.play()
            game_framework.pop_state()
                                    
                                    
control = None

def enter():
    global control
    control = Control()
    
def exit():
    global control
    del control

def update():
    title.title.update()
    control.update()
    
def draw():
    clear_canvas()
    draw_title()
    update_canvas()
    
def pause():
    global control
    control = Control()

def resume():
    global control
    del control
    
def draw_title():
    global control
    title.title.draw()
    control.draw()