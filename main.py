import pico2d
import game_framework
import ingame
import title

class bgm:
    def __init__(self):
        self.title = pico2d.load_music('music/bgm/title.wav')
        self.main = pico2d.load_music('music/bgm/main.wav')
        self.boss = pico2d.load_music('music/bgm/boss.wav')

pico2d.open_canvas(1920, 1080, True, True)
game_framework.run(ingame)
pico2d.close_canvas()