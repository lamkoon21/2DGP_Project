import pico2d
import game_framework
import ingame

pico2d.open_canvas(1920, 1080, False, True)
game_framework.run(ingame)
pico2d.close_canvas