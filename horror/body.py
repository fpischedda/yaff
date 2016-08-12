class Body:
    """
    Represents the status of the body, each part of the body has a name and a
    value representing its status 1 = perferctly fine, 0 = unavailale
    """

    def __init__(self, parts=None):
        if parts is not None:
            self.boyd_parts = parts.copy()
        else:
            self.body_parts = {}

    def status(self):
        """return the average body status"""
        total = len(self.body_parts)

        if total <= 0:
            return 0

        return sum((p for p in self.body_parts.values())) // total
