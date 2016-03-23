import pyglet
from yaff.director import Director
from yaff.contrib.scenes import SplashScene
from game_scene import GameScene


window = pyglet.window.Window()
director = Director(window,
                    startup_scene=SplashScene(next_scene_class=GameScene))

pyglet.clock.schedule(director.on_update)

if __name__ == '__main__':
    pyglet.app.run()
