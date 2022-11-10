from pico2d import *
import game_framework
import ingame

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
    
    for crawlid in ingame.crawlids:
        crawlid.update()
    
    for husk in ingame.husks:
        husk.update()
        husk.find_x = ingame.knight.x
        husk.find_y = ingame.knight.y
    
    for vengefly in ingame.vengeflies:
        vengefly.update()
        vengefly.find_x = ingame.knight.x
        vengefly.find_y = ingame.knight.y

def draw():
    clear_canvas()
    draw_world()
    update_canvas()
    
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            ingame.knight.move = False
            ingame.knight.dash = False
            ingame.knight.attack = False
            ingame.knight.jump = False
            ingame.knight.fall = False
            ingame.knight.attack_2 = False
            ingame.knight.idle = True
            
        if event.type == SDL_KEYUP:
            if event.key == pico2d.SDLK_TAB:
                game_framework.pop_state()

def pause():
    global map
    map = Map()

def resume():
    global map
    del map
    
def draw_world():
    global map
    for crawlid in ingame.crawlids:
        crawlid.draw()
    for husk in ingame.husks:
        husk.draw()
    for vengefly in ingame.vengeflies:
        vengefly.draw()
    
    ingame.knight.draw()
    ingame.soul.draw()
    ingame.floor.draw()
    
    map.draw()