from lib.room import Room
from lib.forniture import Forniture


class Game:

    def __init__(self):

        self.rooms = [
            Room('living room', 20, 10),
            Room('bathroom', 10, 10),
            Room('bedroom', 15, 8)
        ]

        forniture = Forniture("window", 50, 50, 0)

        self.rooms[0].add_forniture(forniture, 10, 100)

        self.persons = []

    def add_person(self, person):
        self.persons.append(person)

    def update(self, dt):

        for r in self.rooms:
            r.update(dt)
