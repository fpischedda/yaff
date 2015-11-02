from yaff.scene import Scene
from game import Game
from room_render import RoomRender


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        self.game = Game()
        self.room_render = RoomRender(self.game.rooms[0])

    def on_key_release(self, symbol, modifier):
        pass

    def on_key_press(self, symbol, modifier):
        return True

    def on_update(self, dt):
        self.game.update(dt)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.room_render.render()
