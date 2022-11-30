from pico2d import *
import game_framework
import server
import game_world

class Map:
    def __init__(self):
        self.x, self.y = 960, 540
        self.image = load_image('image/ui/Fragment_04.png')
        
    def draw(self):
        self.image.draw(960, 540)

map = None

def enter():
    global map
    map = Map()
    
def exit():
    global map
    del map
    
    
def update():
    server.soul.hp = server.knight.hp
    server.soul.soul = server.knight.soul
    server.knight.update()
    server.soul.update()
    
    # for crawlid in server.crawlids:
    #     crawlid.update()
    
    # for husk in server.husks:
    #     husk.update()
    #     husk.find_x = server.knight.x
    #     husk.find_y = server.knight.y
    
    # for vengefly in server.vengeflies:
    #     vengefly.update()
    #     vengefly.find_x = server.knight.x
    #     vengefly.find_y = server.knight.y

def draw():
    clear_canvas()
    draw_world()
    update_canvas()
    
def handle_events():
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYUP, pico2d.SDLK_TAB):
            server.knight.frame = 0
            server.knight.map_open = False
            server.knight.map_close = True
            game_framework.pop_state()
        else:
            server.knight.handle_events(event)

def pause():
    global map
    map = Map()

def resume():
    global map
    del map
    
def draw_world():
    global map
    
    for game_object in game_world.all_objects():
        game_object.draw()
    
    map.draw()