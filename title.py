from pico2d import *
import game_framework
import ingame

class Title:
    def __init__(self):
        self.background = load_image('image/title/title_background.png')
        self.name = load_image('image/title/title_name.png')
        self.pointer_l = load_image('image/title/title_pointer_L.png')
        self.pointer_r = load_image('image/title/title_pointer_R.png')
    def draw(self):
        self.background.clip_draw(0, 100, 2040, 1330, 960, 540, 1920, 1080)
        self.name.draw(960, 750)
        



def handle_events():
    global select, input
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if input == False:
                match event.key:
                    case pico2d.SDLK_UP:
                        if select == 1:
                            select = 3
                        else:
                            select += 1
                        input = True
                    case pico2d.SDLK_DOWN:
                        if select == 3:
                            select = 1
                        else:
                            select -= 1
                        input = True
                    case pico2d.SDLK_RETURN:
                        input = False
                    case pico2d.SDLK_ESCAPE:
                        game_framework.quit()
        elif event.type == SDL_KEYUP:
            if input == True:
                match event.key:
                    case pico2d.SDLK_UP:
                        input = True
                    case pico2d.SDLK_DOWN:
                        input = True
                    case pico2d.SDLK_RETURN:
                         match select:
                            case 1:
                                game_framework(ingame)
                            case 3:
                                game_framework.quit()\
                                    
                                    
frame = None
input = False
select = None
title = None
running = False

def enter():
    global title, frame, select, running
    title = Title()
    frame = 0
    select = 1
    running = True
    
def exit():
    global background, name, pointer_L, pointer_R, running
    del background
    del name
    del pointer_L
    del pointer_R

def update():
    # global frame
    # if frame < 10:
    #     frame += 1
    # else:
    #     frame = 0
    pass
    
def draw():
    clear_canvas()
    title.draw()
    update_canvas()
    
def pause():
    pass

def resume():
    pass   