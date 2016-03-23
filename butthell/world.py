class Boundaries:

    def __init__(self, width, height, boundaries=None):
        self.width = width
        self.height = height

        if boundaries is not None:
            self.boundaries = boundaries.copy()
        else:
            self.boundaries = (0, 0, width, height)

    def rect_fully_outside(self, rect):
        """
        returns True if rect is fully outside boundaries
        """
        b = self.boundaries
        return rect[0] > b[2] or rect[1] > b[3] \
            or rect[2] < b[0] or rect[3] < b[1]

    def rect_inside(self, rect):
        """
        returns True if rect is fully inside boundaries
        """
        b = self.boundaries
        return rect[0] >= b[0] and rect[1] >= b[1] \
            and rect[2] <= b[2] and rect[3] <= b[3]

    def circle_inside(self, pos, radius):
        """
        returns True if the circle described by pos + radius is inside
        boundaries
        """
        hr = radius / 2
        r = (pos[0] - hr, pos[1] - hr, pos[2] + hr, pos[3] + hr)
        return self.rect_inside(r)

    def circle_fully_inside(self, pos, radius):
        """
        returns True if the circle described by pos + radius is fully outside
        boundaries
        """
        hr = radius / 2
        r = (pos[0] - hr, pos[1] - hr, pos[2] + hr, pos[3] + hr)
        return self.rect_fully_outside(r)
