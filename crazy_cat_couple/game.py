from lib.room import Room


class Game:

    def __init__(self):

        self.rooms = {
            'living room': Room(20, 10),
            'bathroom': Room(10, 10),
            'bedroom': Room(15, 8)
        }

        self.humans = {}

    def add_person(self, person):
        self.persons[person.name] = person

    def update(self, dt):

        for r in self.rooms.values():
            r.update(dt)
