from pico2d import *
import constant_value
from background import FixedBackground as Background
import server
import game_framework
import game_world
import player
import enemy
import ui_soul
import ui_map
from wall import Wall

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_TAB):
            if server.knight.idle:
                server.knight.frame = 0
                server.knight.jump = False
                server.knight.fall = False
                server.knight.dash = False
                server.knight.attack = False
                server.knight.attack_2 = False
                server.knight.damage = False
                server.knight.map_open = True
                constant_value.left = 0
                constant_value.bottom = 0
                constant_value.right = 0
                constant_value.top = 0
                game_framework.push_state(ui_map)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_EQUALS):
            if server.collide_box: server.collide_box = False
            else: server.collide_box = True
        else:
            server.knight.handle_events(event)

def enter():
    server.background = Background()
    server.background.select_map = 0
    server.background.w = server.background.map1.w
    server.background.h = server.background.map1.h
        
    server.bgm = load_music('music/bgm/map0.wav')
    server.bgm.repeat_play()
    game_world.add_object(server.background, 0)
    
    # init 2660
    set_knight(2660, constant_value.bottom)
    
    with open('wall_stage0.json', 'r') as f:
        wall_list = json.load(f)
        for o in wall_list:
            wall = Wall(o['x1'], o['y1'], o['x2'], o['y2'])
            game_world.add_object(wall, 0)
            game_world.add_collision_pairs(server.knight, wall, 'knight:wall')
    
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
            
    # print(constant_value.right)
    # print(constant_value.top)
    
        
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
    if bottom_a > top_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    
    return True



        
# set objects
    
def set_knight(x, y):
    server.knight = player.Knight()
    server.knight.x = x
    server.knight.y = y
    server.spike = player.Spike()
    server.spike.x = x
    server.spike.y = y
    server.soul = ui_soul.Soul()
    server.soul.hp = server.knight.hp
    server.soul.soul = server.knight.soul
    game_world.add_object(server.knight, 1)
    game_world.add_object(server.spike, 1)
    game_world.add_object(server.soul, 2)
