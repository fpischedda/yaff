import pyglet
from yaff.conf import settings
from yaff.director import Director


def run(startup_scene, app=pyglet.app):
    window = pyglet.window.Window(**settings.WINDOW_OPTIONS)
    director = Director(window,
                        startup_scene=startup_scene)

    pyglet.clock.schedule(director.on_update)
    app.run()
