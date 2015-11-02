from lib.room import Room


class Game:

    def __init__(self):

        self.rooms = [
            Room('living room', 20, 10),
            Room('bathroom', 10, 10),
            Room('bedroom', 15, 8)
        ]

        self.persons = []

    def add_person(self, person):
        self.persons.append(person)

    def update(self, dt):

        for r in self.rooms:
            r.update(dt)
