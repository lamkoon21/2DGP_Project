import pico2d
import game_framework
import ingame
import title

pico2d.open_canvas(1920, 1080, True, True)
game_framework.run(title)
pico2d.close_canvas()