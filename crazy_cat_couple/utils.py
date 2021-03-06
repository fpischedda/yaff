import random
import pyglet


def random_color():

    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def load_gif_animation(path, tex_bin=None):

    tb = tex_bin or pyglet.image.atlas.TextureBin()
    animation = pyglet.image.load_animation(path)
    animation.add_to_texture_bin(tb)

    return animation


def load_grid_animation(path, rows, cols, frame_duration=0.1):

    img = pyglet.resource.image(path)
    grid = pyglet.image.ImageGrid(img, rows, cols)
    return pyglet.image.Animation.from_image_sequence(grid,
                                                      frame_duration,
                                                      True)
