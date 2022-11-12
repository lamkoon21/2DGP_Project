from pico2d import *
import game_framework
import game_world
import player
import enemy
import ui_soul
import ui_map
import back_floor
from constant_value import *
from background import FixedBackground as Background

floor = None
knight = None
spike = None
soul = None
crawlids = []
husks = []
vengeflies = []
background = None
bgm = None

collide_box = False

def handle_events():
    global knight
    global collide_box
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_TAB):
            if knight.idle:
                knight.frame = 0
                knight.jump = False
                knight.fall = False
                knight.dash = False
                knight.attack = False
                knight.attack_2 = False
                knight.damage = False
                knight.map_open = True
                game_framework.push_state(ui_map)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_EQUALS):
            if collide_box: collide_box = False
            else: collide_box = True
        else:
            knight.handle_events(event)

def enter():
    global knight, floor, crawlids, husks, vengeflies, background, bgm
    background = Background()
    bgm = load_music('music/bgm/main.wav')
    bgm.repeat_play()
    game_world.add_object(background, 0)
    floor = back_floor.Floor()
    game_world.add_object(floor, 0)
    
    set_crawlid(1700, BOTTOM, 1000, RIGHT)
    set_husk(1400, BOTTOM, 900, 1600)
    set_vengefly(1600, 750, 1200, 1700)
    game_world.add_objects(crawlids, 1)
    game_world.add_objects(husks, 1)
    game_world.add_objects(vengeflies, 1)
    
    set_knight(400, BOTTOM)
    
    game_world.add_collision_pairs(knight, crawlids, 'knight:crawlid')
    game_world.add_collision_pairs(knight, husks, 'knight:husk')
    game_world.add_collision_pairs(knight, vengeflies, 'knight:vengefly')
    game_world.add_collision_pairs(spike, crawlids, 'spike:crawlid')
    game_world.add_collision_pairs(spike, husks, 'spike:husk')
    game_world.add_collision_pairs(spike, vengeflies, 'spike:vengefly')
    game_world.add_collision_pairs(knight, floor, 'knight:floor')
    game_world.add_collision_pairs(crawlids, floor, 'knight:floor')
    game_world.add_collision_pairs(husks, floor, 'knight:floor')
    game_world.add_collision_pairs(vengeflies, floor, 'knight:floor')
    
def exit():
    game_world.clear()
    
    
def update():
    for game_object in game_world.all_objects():
        game_object.update()
        
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLISION', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)
    
        
def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()
        
def pause():
    pass

def resume():
    pass
        
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    
    return True



        
# set objects
    
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
    global knight, soul, spike
    knight = player.Knight()
    knight.x = x
    knight.y = y
    spike = player.Spike()
    soul = ui_soul.Soul()
    soul.hp = knight.hp
    soul.soul = knight.soul
    game_world.add_object(knight, 1)
    game_world.add_object(spike, 1)
    game_world.add_object(soul, 2)

