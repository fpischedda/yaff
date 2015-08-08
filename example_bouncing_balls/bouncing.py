def axis_diff(direction, rect_start, rect_finish,
              boundaries_start, boundaries_finish):

    if direction < 0:
        if rect_start < boundaries_start:
            return rect_start - boundaries_start
    elif direction > 0:
        if rect_finish > boundaries_finish:
            return rect_finish - boundaries_finish

    return 0


class Bouncing:

    def __init__(self, boundaries, starting_direction=[1, 1], *args, **kwargs):

        super(Bouncing, self).__init__(*args, **kwargs)

        self.boundaries = boundaries
        self.direction = starting_direction

    def update_direction(self, rect):

        d = self.direction
        b = self.boundaries
        diff = (axis_diff(d[0], rect[0], rect[2], b[0], b[2]),
                axis_diff(d[1], rect[1], rect[3], b[1], b[3]))

        if diff[0] != 0:
            d[0] = -d[0]

        if diff[1] != 0:
            d[1] = -d[1]

        return diff
