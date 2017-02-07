class Scene(object):

    def __init__(self, parent=None):

        self.parent = parent

    def set_director(self, director):
        self.director = director

    def on_draw(self, window):

        window.clear()
