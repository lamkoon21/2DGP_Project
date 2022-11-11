from pico2d import *
import game_framework
import ingame

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Title:
    def __init__(self):
        self.frame = 0.0
        self.background = load_image('image/title/title_background.png')
        self.logo = load_image('image/title/title_name.png')
        self.pointer = load_image('image/title/title_pointer.png')
        self.font = load_font('font.ttf', 50)
        self.bgm = load_music('music/bgm/title.wav')
        self.select = load_music('music/ui/title_select.wav')
        self.confirm = load_music('music/ui/ui_confirm.wav')
        self.bgm.set_volume(128)
        self.select.set_volume(128)
        self.confirm.set_volume(128)
        self.bgm.repeat_play()
    
    def update(self):
        if int(self.frame) < 10:
            self.frame = (self.frame + 11 * ACTION_PER_TIME * game_framework.frame_time * 1.5) % 11
        
    def draw(self):
        self.background.clip_draw(0, 100, 2040, 1330, 960, 540, 1920, 1080)
        self.logo.draw(960, 750)
        self.pointer.clip_draw(int(self.frame) * 99, 0, 99, 72, 800, 500 - select * 100, 70, 50)
        self.pointer.clip_composite_draw(int(self.frame) * 99, 0, 99, 72, 0, 'h', 1100, 500 - select * 100, 70, 50)
        self.font.draw(861, 400, '게임 시작', (255, 255, 255))
        self.font.draw(861, 300, '조작 방법', (255, 255, 255))
        self.font.draw(861, 200, '게임 종료', (255, 255, 255))

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
                        title.frame = 0
                        if select == 1:
                            select = 3
                        else:
                            select -= 1
                        input = True
                        title.select.play()
                    case pico2d.SDLK_DOWN:
                        title.frame = 0
                        if select == 3:
                            select = 1
                        else:
                            select += 1
                        input = True
                        title.select.play()
                    case pico2d.SDLK_RETURN:
                        input = True
                        title.confirm.play()
                    case pico2d.SDLK_ESCAPE:
                        game_framework.quit()
        elif event.type == SDL_KEYUP:
            if input == True:
                match event.key:
                    case pico2d.SDLK_UP:
                        input = False
                    case pico2d.SDLK_DOWN:
                        input = False
                    case pico2d.SDLK_RETURN:
                        input = False
                        match select:
                            case 1:
                                delay(1.3)
                                game_framework.change_state(ingame)
                            case 2:
                                pass
                            case 3:
                                game_framework.quit()
                                    
                                    
title = None
frame = None
input = False
select = None

def enter():
    global title, frame, select, input
    title = Title()
    frame = 0
    input = False
    select = 1
    
def exit():
    global title
    del title

def update():
    title.update()
    
def draw():
    clear_canvas()
    title.draw()
    update_canvas()
    
def pause():
    pass

def resume():
    pass   