import pyglet
from yaff.conf import settings
from yaff.director import Director


def run(startup_scene, app=pyglet.app,
        additional_resource_path=None):
    window = pyglet.window.Window(**settings.WINDOW_OPTIONS)
    director = Director(window,
                        startup_scene=startup_scene)

    if isinstance(additional_resource_path, str):
        pyglet.resource.path.append(additional_resource_path)
    elif hasattr(additional_resource_path, '__iter__'):
        pyglet.resource.path.extend(additional_resource_path)

    pyglet.clock.schedule(director.on_update)
    app.run()
