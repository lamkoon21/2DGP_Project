from pico2d import *
import constant_value
from background import FixedBackground as Background
import server
import game_framework
import game_world
import player
from enemy import Crawlid, Husk, Vengefly
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
            
crawlid = []
husk = []
vengefly = []

def enter():
    server.background = Background()
    server.background.select_map = 1
    server.background.image = load_image('image/map/map1.png')
    server.background.w = server.background.image.w
    server.background.h = server.background.image.h
    game_world.add_object(server.background, 0)
    
    server.bgm = load_music('music/bgm/main.wav')
    server.bgm.repeat_play()
    
    set_knight(3150, 2575) 
    
    with open('enemy_data.json','r') as f:
        enemy_list = json.load(f)
        crawlid_data = enemy_list['stage1']['crawlid']
        for i in crawlid_data:
            crawlid.append(Crawlid(i['x'], i['y'], i['dir'], i['range_x1'], i['range_x2']))
            game_world.add_collision_pairs(server.knight, crawlid, 'knight:crawlid')
            game_world.add_collision_pairs(server.spike, crawlid, 'spike:crawlid')
            game_world.add_objects(crawlid, 1)
        husk_data = enemy_list['stage1']['husk']
        for i in husk_data:
            husk.append(Husk(i['x'], i['y'], i['dir'], i['range_x1'], i['range_x2']))
            game_world.add_collision_pairs(server.knight, husk, 'knight:husk')
            game_world.add_collision_pairs(server.spike, husk, 'spike:husk')
            game_world.add_objects(husk, 1)
        vengefly_data = enemy_list['stage1']['vengefly']
        for i in vengefly_data:
            vengefly.append(Vengefly(i['x'], i['y'], i['dir'], i['range_x1'], i['range_x2']))
            game_world.add_collision_pairs(server.knight, vengefly, 'knight:vengefly')
            game_world.add_collision_pairs(server.spike, vengefly, 'spike:vengefly')
            game_world.add_objects(vengefly, 1)
            
        
        
    
    with open('wall_data.json', 'r') as f:
        wall_list = json.load(f)
        wall_data = wall_list['stage1']
        for o in wall_data:
            wall = Wall(o['x1'], o['y1'], o['x2'], o['y2'])
            game_world.add_object(wall, 0)
            game_world.add_collision_pairs(server.knight, wall, 'knight:wall')
            game_world.add_collision_pairs(crawlid, wall, 'crawlid:wall')
            game_world.add_collision_pairs(husk, wall, 'husk:wall')
            game_world.add_collision_pairs(vengefly, wall, 'vengefly:wall')
    
    
    # init 2660   
    
        
            
            
    
def exit():
    game_world.clear()
    
    
def update():
    server.background.update()
    server.knight.collide_bottom = False
    server.knight.collide_top = False
    server.knight.collide_left = False
    server.knight.collide_right = False
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            # print('COLLISION', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)
            
    for game_object in game_world.all_objects():
        game_object.update()
        
def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()    
        
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
    server.knight = player.Knight(x, y, 5, 0, 0)
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

