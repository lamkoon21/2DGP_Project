from pico2d import *
import game_framework
import player
import enemy
import ui_soul
import ui_map

BOTTOM = 400
TOP = 1050
LEFT = 50
RIGHT = 1880

class Floor:
    def __init__(self):
        self.image = load_image('image/map/floor.png')

    def draw(self):
        self.image.draw(1200, 240)
        self.image.draw(0, 240)


def handle_events():
    global knight, running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.quit()
                case pico2d.SDLK_LEFT:     # left
                    knight.attack_2 = False
                    if knight.move == False:
                        knight.dir = -1
                        knight.move = True
                    else:
                        knight.move = False
                case pico2d.SDLK_RIGHT:    # right
                    knight.attack_2 = False
                    if knight.move == False:
                        knight.dir = 1
                        knight.move = True
                    else:
                        knight.move = False
                case pico2d.SDLK_z:        # jump
                    knight.attack_2 = False
                    if knight.jump == False:
                        if knight.frame != 0:
                            knight.frame = 0
                        knight.jump = True
                case pico2d.SDLK_x:        # attack
                    knight.soul += 1
                    if knight.dash == False and knight.attack == False:
                        if knight.frame != 0:
                            knight.frame = 0
                        knight.attack = True
                case pico2d.SDLK_c:        # dash
                    knight.attack_2 = False
                    if knight.dash == False:
                        if knight.frame != 0:
                            knight.frame = 0
                        knight.jump = False
                        knight.fall = False
                        knight.dash = True
                case pico2d.SDLK_TAB:
                    game_framework.push_state(ui_map)
                        
        elif event.type == SDL_KEYUP:
            match event.key:
                case pico2d.SDLK_LEFT:     # left
                    if knight.move == True:
                        knight.move = False
                    else:
                        knight.dir = 1
                        knight.move = True
                case pico2d.SDLK_RIGHT:    # right
                    if knight.move == True:
                        knight.move = False
                    else:
                        knight.dir = -1
                        knight.move = True

floor = None
knight = None
soul = None
crawlids = []
husks = []
vengeflies = []
running = None

def enter():
    global floor, running
    running = True
    
    floor = Floor()
    
    set_knight(400, BOTTOM)
    set_crawlid(1700, BOTTOM, 1000, RIGHT)
    set_husk(1400, BOTTOM, 900, 1600)
    set_vengefly(1400, 750, 1000, 1700)
    
def exit():
    global knight, soul, floor
    global crawlids, husks, vengeflies
    
    del knight
    for husk in husks:
        del husk
    for crawlid in crawlids:
        del crawlids
    for vengefly in vengeflies:
        del vengefly
    del soul
    del floor
    
def update():
    global knight, soul, husk, crawlid
    
    soul.hp = knight.hp
    soul.soul = knight.soul
    knight.update()
    soul.update()
    
    for crawlid in crawlids:
        crawlid.update()
    
    for husk in husks:
        husk.update()
        husk.find_x = knight.x
        husk.find_y = knight.y
    
    for vengefly in vengeflies:
        vengefly.update()
        vengefly.find_x = knight.x
        vengefly.find_y = knight.y
        
def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def draw_world():
    for crawlid in crawlids:
        crawlid.draw()
    for husk in husks:
        husk.draw()
    for vengefly in vengeflies:
        vengefly.draw()
    
    knight.draw()
    soul.draw()
    floor.draw()
    delay(0.03)
    
def set_crawlid(x, y, x1, x2):
    global crawlids
    crawlids.append(enemy.Crawlid())
    crawlids[-1].x = x
    crawlids[-1].y = y
    crawlids[-1].range_x1 = x1
    crawlids[-1].range_x2 = x2
    
def set_husk(x, y, x1, x2):
    global husks
    husks.append(enemy.Husk())
    husks[-1].x = x
    husks[-1].y = y
    husks[-1].range_x1 = x1
    husks[-1].range_x2 = x2
    
def set_vengefly(x, y, x1, x2):
    global vengeflies
    vengeflies.append(enemy.Vengefly())
    vengeflies[-1].x = x
    vengeflies[-1].y = y
    vengeflies[-1].range_x1 = x1
    vengeflies[-1].range_x2 = x2
    
def set_knight(x, y):
    global knight, soul
    knight = player.Knight()
    knight.x = x
    knight.y = y
    soul = ui_soul.Soul()
    soul.hp = knight.hp
    soul.soul = knight.soul
    
def pause():
    pass

def resume():
    pass
