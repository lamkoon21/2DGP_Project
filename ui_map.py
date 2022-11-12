from pico2d import *
import game_framework
import ingame
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
    ingame.knight, ingame.soul, ingame.husks, ingame.crawlids, ingame.vengeflies
    
    
    ingame.soul.hp = ingame.knight.hp
    ingame.soul.soul = ingame.knight.soul
    ingame.knight.update()
    ingame.soul.update()
    
    # for crawlid in ingame.crawlids:
    #     crawlid.update()
    
    # for husk in ingame.husks:
    #     husk.update()
    #     husk.find_x = ingame.knight.x
    #     husk.find_y = ingame.knight.y
    
    # for vengefly in ingame.vengeflies:
    #     vengefly.update()
    #     vengefly.find_x = ingame.knight.x
    #     vengefly.find_y = ingame.knight.y

def draw():
    clear_canvas()
    draw_world()
    update_canvas()
    
def handle_events():
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYUP, pico2d.SDLK_TAB):
            ingame.knight.frame = 0
            ingame.knight.map_open = False
            ingame.knight.map_close = True
            game_framework.pop_state()
        else:
            ingame.knight.handle_events(event)

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