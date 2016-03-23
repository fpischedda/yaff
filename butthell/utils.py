import random
import math
from letter import Letter


def random_color():

    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def spawn_letters(bitmap_font, text, start_x, start_y, batch, boundaries):

    points = len(text)
    if points <= 0:
        return []

    letters = []
    angle = 0
    angle_diff = 360 / points
    for letter in text:
        letter_image = bitmap_font.get_image(letter)
        direction = [math.cos(angle), math.sin(angle)]
        l = Letter(5.0, boundaries,
                   direction,
                   letter_image,
                   batch=batch)
        l.x = start_x
        l.y = start_y

        letters.append(l)
        angle += angle_diff

    return letters
