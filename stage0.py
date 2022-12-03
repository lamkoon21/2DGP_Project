from pico2d import *
from background import FixedBackground as Background
import server
import game_framework
import game_world
from player import Knight, Spike
from gate import Gate
import ui_soul
import ui_map
from wall import Wall
from boss_key import Bosskey
from save_bench import Savebench

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
                game_framework.push_state(ui_map)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_EQUALS):
            if server.collide_box: server.collide_box = False
            else: server.collide_box = True
        else:
            server.knight.handle_events(event)

front_image = None

def enter():
    print('stage0')
    
    set_knight('stage0')
    
    server.background = Background()
    server.background.image = load_image('image/map/stage0.png')
    game_world.add_object(server.background, 0)
    server.background.update()
    
    global front_image
    front_image = Background()
    front_image.image = load_image('image/map/stage0_front.png')
    game_world.add_object(front_image, 0)
    front_image.update()
    
    save_bench = Savebench(7390, 635, 7550, 555)
    game_world.add_object(save_bench, 0)
    game_world.add_collision_pairs(server.knight, save_bench, 'knight:save_bench')
    
    if server.knight.boss_key < 3 and server.key_in_stage[0] == 0:
        global boss_key
        boss_key = Bosskey(14240, 440)
        boss_key.image = load_image('image/map/key_piece%d.png' %(server.knight.boss_key + 1))
        game_world.add_object(boss_key, 1)
        game_world.add_collision_pairs(server.knight, boss_key, 'knight:boss_key')
    
    server.bgm = load_music('music/bgm/stage0.wav')
    server.bgm.repeat_play()
    
    set_wall('stage0')
    
    set_gate('stage0')
    
    server.visit[0] = 1
    server.current_stage = 0
            

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
        
    if server.current_stage == 1:
        import stage1
        game_framework.change_state(stage1)
        
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
    
def set_knight(s):
    with open('knight_data.json', 'r') as f:
        knight_data = json.load(f)
    with open('stage_data.json', 'r') as f:
        stage_data = json.load(f)
        
    if server.current_stage == 'respawn1':
        server.knight = Knight(stage_data[s]['respawn']['x'], stage_data[s]['respawn']['y'], stage_data[s]['respawn']['face_dir'], knight_data['move'], knight_data['hp'], knight_data['soul'], knight_data['boss_key'])
    elif server.pre_stage == -1:
        server.knight = Knight(stage_data[s]['start']['x'], stage_data[s]['start']['y'], stage_data[s]['start']['face_dir'], knight_data['move'], knight_data['hp'], knight_data['soul'], knight_data['boss_key'])
    elif server.pre_stage == 1:
        server.knight = Knight(stage_data[s]['gate1']['x'], stage_data[s]['gate1']['y'], stage_data[s]['gate1']['face_dir'], knight_data['move'], knight_data['hp'], knight_data['soul'], knight_data['boss_key'])
         
    server.spike = Spike()
    server.spike.x = server.knight.x
    server.spike.y = server.knight.y
    server.soul = ui_soul.Soul()
    server.soul.hp = server.knight.hp
    server.soul.soul = server.knight.soul
    game_world.add_object(server.knight, 1)
    game_world.add_object(server.spike, 1)
    game_world.add_object(server.soul, 2)
    
def set_wall(s):
    with open('wall_data.json', 'r') as f:
        wall_list = json.load(f)
        wall_data = wall_list[s]
        for o in wall_data:
            wall = Wall(o['x1'], o['y1'], o['x2'], o['y2'])
            game_world.add_object(wall, 0)
            game_world.add_collision_pairs(server.knight, wall, 'knight:wall')
            
def set_gate(s): 
    with open('gate_data.json', 'r') as f:
        gate_list = json.load(f)
        gate_data = gate_list[s]
        for o in gate_data:
            gate = Gate(o['stage'], o['index'], o['x1'], o['y1'], o['x2'], o['y2'])
            game_world.add_object(gate, 0)
            game_world.add_collision_pairs(server.knight, gate, 'knight:gate')