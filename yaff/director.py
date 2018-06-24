import collections


class Director:
    def __init__(self, window, startup_scene=None):

        self.window = window
        window.push_handlers(self)
        self.scenes = collections.deque()
        if startup_scene is not None:
            self.push_scene(startup_scene)

    def send_close_window_event(self):
        self.window.dispatch_event('on_close')

    def current_scene(self):
        try:
            return self.scenes[-1]
        except IndexError:
            return None

    def prepare_next_scene(self, scene_class, *args, **kwargs):
        if scene_class is not None:
            self.replace_scene(scene_class(*args, **kwargs))
        else:
            self.send_close_window_event()

    def replace_scene(self, scene):
        old_scene = self.pop_scene()
        self.push_scene(scene)
        return old_scene

    def pop_scene(self):
        try:
            return self.scenes.pop()
        except IndexError:
            return None

    def push_scene(self, scene):
        self.scenes.append(scene)
        scene.set_director(self)

    def on_update(self, dt):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene, 'on_update'):
            current_scene.on_update(dt)

    def on_key_press(self, symbol, modifier):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene,
                                                 'on_key_press'):
            current_scene.on_key_press(symbol, modifier)

    def on_key_release(self, symbol, modifier):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene,
                                                 'on_key_release'):
            current_scene.on_key_release(symbol, modifier)

    def on_mouse_motion(self, *args, **kwargs):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene,
                                                 'on_mouse_motion'):
            current_scene.on_mouse_motion(*args, **kwargs)

    def on_mouse_press(self, x, y, button, modifiers):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene,
                                                 'on_mouse_press'):
            current_scene.on_mouse_motion(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene,
                                                 'on_mouse_release'):
            current_scene.on_mouse_motion(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene,
                                                 'on_mouse_drag'):
            current_scene.on_mouse_motion(x, y, dx, dy, buttons, modifiers)

    def on_draw(self):
        current_scene = self.current_scene()
        if current_scene is not None and hasattr(current_scene, 'on_draw'):
            current_scene.on_draw(self.window)
