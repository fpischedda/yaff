import pyglet


default_map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?()@:/'., "


class BitmapFont:

    def __init__(self, image_path, width, height, font_map=default_map):
        image = pyglet.resource.image(image_path)
        self.grid = pyglet.image.ImageGrid(image, 1, image.width//width)
        texture = self.grid.get_texture()
        pyglet.gl.glTexParameteri(texture.target,
                                  pyglet.gl.GL_TEXTURE_MAG_FILTER,
                                  pyglet.gl.GL_NEAREST)
        pyglet.gl.glTexParameteri(texture.target,
                                  pyglet.gl.GL_TEXTURE_MIN_FILTER,
                                  pyglet.gl.GL_NEAREST)
        self.width = width
        self.height = height
        self.font_map = font_map

    def get_image(self, letter, fallback='?'):

        if letter in self.font_map:
            return self.grid[self.font_map.find(letter)]
        else:
            return self.grid[self.font_map.find(fallback)]
