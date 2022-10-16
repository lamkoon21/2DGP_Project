from pico2d import *
import game_framework
import ingame

class Map:
    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('image/ui/map.png')


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYUP:
            if event.key == pico2d.SDLK_TAB:
                game_framework.pop_state(ingame)



def pause():
    pass

def resume():
    pass