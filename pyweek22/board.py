"""
Board abstraction class
a board is a matrix of widht X height tiles
the board tiles can be of type FLOOR or WALL
the board tiles can be rotated by column or by row
"""
import random


class Board:

    TILE_FLOOR = 0
    TILE_WALL = 1
    TILE_PLAYER_1 = 2
    TILE_PLAYER_2 = 3

    def __init__(self, width=5, height=5, max_walls=10):

        self.width = width
        self.height = height
        self.tiles = {(row, col): self.TILE_FLOOR
                      for row in range(height)
                      for col in range(width)}

        for i in range(max_walls):
            pos = (random.randint(0, width - 1),
                   random.randint(0, height - 1))
            self.tiles[pos] = self.TILE_WALL

        self.tiles[(0, 0)] = self.TILE_PLAYER_1
        self.tiles[(height - 1, width - 1)] = self.TILE_PLAYER_2

    def get_tile_at(self, row, column):
        """
        returns the tile at the row column position
        """
        try:
            return self.tiles[(row, column)]
        except:
            raise IndexError

    def set_tile_at(self, row, column, tile):
        """
        sets the tile at the specified position
        """
        pos = (row, column)
        if pos in self.tiles:
            self.tiles[(row, column)] = tile
        raise IndexError

    def slide_colum_up(self, column):
        first = self.tiles[(0, column)]

        for i in range(self.height-1):
            self.tiles[(i, column)] = self.tiles[(i + 1, column)]
        self.tiles[(self.height - 1, column)] = first

    def slide_colum_down(self, column):
        last = self.tiles[(self.height - 1, column)]

        for i in range(1, self.height):
            self.tiles[(i, column)] = self.tiles[(i - 1, column)]
        self.tiles[(0, column)] = last

    def slide_row_left(self, row):
        first = self.tiles[(row, 0)]

        for i in range(self.width - 1):
            self.tiles[(row, i)] = self.tiles[(row, i + 1)]
        self.tiles[(row, self.width - 1)] = first

    def slide_row_right(self, row):
        last = self.tiles[(row, self.width - 1)]

        for i in range(1, self.width):
            self.tiles[(row, i)] = self.tiles[(row, i - 1)]
        self.tiles[(row, 0)] = last

    def rotate_block_left(self, row, column):
        temp = self.tiles[(row, column)]
        self.tiles[(row, column)] = self.tiles[(row, column + 1)]
        self.tiles[(row, column + 1)] = self.tiles[(row + 1, column + 1)]
        self.tiles[(row + 1, column + 1)] = self.tiles[(row + 1, column)]
        self.tiles[(row + 1, column)] = temp

    def rotate_block_right(self, row, column):
        temp = self.tiles[(row, column)]
        self.tiles[(row, column)] = self.tiles[(row + 1, column)]
        self.tiles[(row + 1, column)] = self.tiles[(row + 1, column + 1)]
        self.tiles[(row + 1, column + 1)] = self.tiles[(row, column + 1)]
        self.tiles[(row, column + 1)] = temp
