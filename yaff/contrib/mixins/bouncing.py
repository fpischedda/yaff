def axis_diff(direction, rect_start, rect_finish,
              boundaries_start, boundaries_finish):
    """
    detects if an segment is outside its boundaries and returns the
    difference between segment and boundary; if the segment is inside
    boundaries returns 0
    """

    if direction < 0:
        if rect_start < boundaries_start:
            return rect_start - boundaries_start
    elif direction > 0:
        if rect_finish > boundaries_finish:
            return rect_finish - boundaries_finish

    return 0


class BouncingMixin:
    """
    mixin that define boundaries within which the object can move
    exposes check_boundaries method in order to detect when the object
    is outside of the bounding box defined in the constructor
    """

    def __init__(self, boundaries, *args, **kwargs):

        super(BouncingMixin, self).__init__(*args, **kwargs)

        self.boundaries = boundaries

    def check_boundaries(self, direction, rect):
        """
        returns a new direction with its components "sign flipped"
        if a bounce occurs
        :param tuple direction: the original direction
        :param tuple rect: bounding box of the bouncing object
        :return tuple: a tuple
        """

        d = direction
        b = self.boundaries
        diff = (axis_diff(d[0], rect[0], rect[2], b[0], b[2]),
                axis_diff(d[1], rect[1], rect[3], b[1], b[3]))

        return diff
