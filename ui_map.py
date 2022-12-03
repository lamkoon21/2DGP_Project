from pico2d import *
import game_framework
import server
import game_world

class Map:
    def __init__(self):
        self.x, self.y = 960, 540
        self.empty = load_image('image/ui/empty_map.png')
        self.map0 = load_image('image/ui/map0.png')
        self.map1 = load_image('image/ui/map1.png')
        self.map2 = load_image('image/ui/map2.png')
        self.map3 = load_image('image/ui/map3.png')
        self.map4 = load_image('image/ui/map4.png')
        self.map5 = load_image('image/ui/map5.png')
        self.map6 = load_image('image/ui/map6.png')
        self.map7 = load_image('image/ui/map7.png')
    
    def draw(self):
        self.empty.draw(960,540)
        if server.visit[0] == 1: self.map0.clip_draw(0, 0, 450, 172, 740, 699)
        if server.visit[1] == 1: self.map1.clip_draw(0, 0, 176, 80, 828, 573)
        if server.visit[2] == 1: self.map2.clip_draw(0, 0, 149, 47, 666, 556)
        if server.visit[3] == 1: self.map3.clip_draw(0, 0, 141, 37, 987, 566)
        if server.visit[4] == 1: self.map4.clip_draw(0, 0, 179, 42, 1147, 568)
        if server.visit[5] == 1: self.map5.clip_draw(0, 0, 150, 53, 1311, 568)
        if server.visit[6] == 1: self.map6.clip_draw(0, 0, 117, 160, 1320, 462)
        if server.visit[7] == 1: self.map7.clip_draw(0, 0, 89, 83, 1364, 340)
            

map = None

def enter():
    global map
    map = Map()
    
def exit():
    global map
    del map
    server.bgm.set_volume(128)
    
    
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
    server.bgm.set_volume(128)
    
def draw_world():
    global map
    
    for game_object in game_world.all_objects():
        game_object.draw()
    
    map.draw()