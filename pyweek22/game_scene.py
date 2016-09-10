import pyglet
from yaff.scene import Scene
from .board import Board


class GameScene(Scene):

    UI_MODE_NONE = 0
    UI_MODE_ROW_SLIDE_LEFT = 1
    UI_MODE_ROW_SLIDE_RIGHT = 2
    UI_MODE_COL_SLIDE_UP = 3
    UI_MODE_COL_SLIDE_DOWN = 4
    UI_MODE_ROTATE_LEFT = 5
    UI_MODE_ROTATE_RIGHT = 6

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        self.board = Board(10, 10, 40)

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')
        self.tiles = [
            pyglet.resource.image('res/images/tiles/floor.jpg'),
            pyglet.resource.image('res/images/tiles/wall.png'),
            pyglet.resource.image('res/images/tiles/player_1.jpg'),
            pyglet.resource.image('res/images/tiles/player_2.jpg'),
        ]

        self.ui_mode = self.UI_MODE_NONE
        self.change_ui_mode_keys = {
            pyglet.window.key._1: self.UI_MODE_ROW_SLIDE_LEFT,
            pyglet.window.key._2: self.UI_MODE_ROW_SLIDE_RIGHT,
            pyglet.window.key._3: self.UI_MODE_COL_SLIDE_UP,
            pyglet.window.key._4: self.UI_MODE_COL_SLIDE_DOWN,
            pyglet.window.key._5: self.UI_MODE_ROTATE_LEFT,
            pyglet.window.key._6: self.UI_MODE_ROTATE_RIGHT,
        }

        self.ui_mode_keys = {
            self.UI_MODE_NONE: set(),
            self.UI_MODE_COL_SLIDE_UP: {pyglet.window.key.LEFT,
                                        pyglet.window.key.RIGHT},
            self.UI_MODE_COL_SLIDE_DOWN: {pyglet.window.key.LEFT,
                                          pyglet.window.key.RIGHT},
            self.UI_MODE_ROW_SLIDE_LEFT: {pyglet.window.key.UP,
                                          pyglet.window.key.DOWN},
            self.UI_MODE_ROTATE_RIGHT: {pyglet.window.key.UP,
                                        pyglet.window.key.DOWN},
            self.UI_MODE_ROTATE_LEFT: {pyglet.window.key.LEFT,
                                       pyglet.window.key.RIGHT,
                                       pyglet.window.key.UP,
                                       pyglet.window.key.DOWN},
            self.UI_MODE_ROTATE_RIGHT: {pyglet.window.key.LEFT,
                                        pyglet.window.key.RIGHT,
                                        pyglet.window.key.UP,
                                        pyglet.window.key.DOWN},
        }

        tile_width = 32
        tile_height = 32
        board_width = self.board.width * tile_width
        board_height = self.board.height * tile_height
        self.ui_mode_pointers = [
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, tile_width, board_height, tile_width, board_height, 0),
            (0, 0, 0, tile_width, board_height, tile_width, board_height, 0),
            (0, 0, 0, board_width, tile_height, board_width, tile_height, 0),
            (0, 0, 0, board_width, tile_height, board_width, tile_height, 0),
            (0, 0, 2 * tile_width, 0, 2 * tile_width, 2 * tile_height,
             0, 2 * tile_height),
            (0, 0, 2 * tile_width, 0, 2 * tile_width, 2 * tile_height,
             0, 2 * tile_height),
        ]

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.select_pos = [0, 0]

    def on_key_press(self, symbol, modifier):
        return False

    def fix_pos_on_change(self):
        if self.ui_mode == self.UI_MODE_ROW_SLIDE_LEFT or \
           self.ui_mode == self.UI_MODE_ROW_SLIDE_RIGHT:
            self.select_pos[1] = 0

        elif self.ui_mode == self.UI_MODE_COL_SLIDE_UP or \
             self.ui_mode == self.UI_MODE_COL_SLIDE_DOWN:
            self.select_pos[0] = 0

        elif self.ui_mode == self.UI_MODE_ROTATE_LEFT or \
             self.ui_mode == self.UI_MODE_ROTATE_RIGHT:

            if self.select_pos[0] > self.board.height - 2:
                self.select_pos[0] = self.board.height - 2
            if self.select_pos[1] > self.board.width - 2:
                self.select_pos[1] = self.board.width - 2

    def apply_move(self):
        if self.ui_mode == self.UI_MODE_ROW_SLIDE_LEFT:
            self.board.slide_row_left(self.select_pos[0])
        elif self.ui_mode == self.UI_MODE_ROW_SLIDE_RIGHT:
            self.board.slide_row_left(self.select_pos[0])

        elif self.ui_mode == self.UI_MODE_COL_SLIDE_UP:
            self.board.slide_colum_up(self.select_pos[1])
        elif self.ui_mode == self.UI_MODE_COL_SLIDE_DOWN:
            self.board.slide_colum_down(self.select_pos[1])
        elif self.ui_mode == self.UI_MODE_ROTATE_LEFT:
            self.board.rotate_block_left(self.select_pos[0],
                                         self.select_pos[1])
        elif self.ui_mode == self.UI_MODE_ROTATE_RIGHT:
            self.board.rotate_block_right(self.select_pos[0],
                                          self.select_pos[1])

    def on_key_release(self, symbol, modifier):
        if symbol in self.change_ui_mode_keys:
            self.ui_mode = self.change_ui_mode_keys[symbol]
            self.fix_pos_on_change()
            return True

        if symbol == pyglet.window.key.SPACE:
            self.apply_move()
        elif symbol in self.ui_mode_keys[self.ui_mode]:
            right_limit = self.board.width - 1
            down_limit = self.board.height - 1

            if self.ui_mode == self.UI_MODE_ROTATE_LEFT or \
               self.ui_mode == self.UI_MODE_ROTATE_RIGHT:
                right_limit -= 1
                down_limit -= 1

            if symbol == pyglet.window.key.LEFT and self.select_pos[1] > 0:
                self.select_pos[1] -= 1

            if symbol == pyglet.window.key.RIGHT and \
               self.select_pos[1] < right_limit:
                self.select_pos[1] += 1

            if symbol == pyglet.window.key.DOWN and self.select_pos[0] > 0:
                self.select_pos[0] -= 1

            if symbol == pyglet.window.key.UP and \
               self.select_pos[0] < down_limit:
                self.select_pos[0] += 1

        return False

    def on_update(self, dt):
        pass

    def draw_selection(self):
        rect = self.ui_mode_pointers[self.ui_mode]
        pos = (self.select_pos[1] * self.tile_width,
               self.select_pos[0] * self.tile_height)
        vertices = [rect[0] + pos[0], rect[1] + pos[1],
                    rect[2] + pos[0], rect[3] + pos[1],
                    rect[4] + pos[0], rect[5] + pos[1],
                    rect[6] + pos[0], rect[7] + pos[1]]

        pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2i', vertices))

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)

        for pos, tile in self.board.tiles.items():
            self.tiles[tile].blit(pos[1] * 32, pos[0] * 32)

        if self.ui_mode != self.UI_MODE_NONE:
            self.draw_selection()
