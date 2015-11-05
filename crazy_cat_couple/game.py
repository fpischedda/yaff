import json
import pyglet.resource
from lib.room import Room
from lib.forniture import Forniture


def load_from_json(filename):
    """load Forniture definition form a json file"""

    with pyglet.resource.file(filename, 'rt') as file:

        definitions = json.loads(file.read())

        forniture = {item["name"]: Forniture(**item)
                     for item in definitions["definitions"]}

    return forniture


class Game:

    def __init__(self):

        self.forniture = load_from_json("res/forniture/forniture.json")

        self.rooms = [
            Room('living room', 20, 10),
            Room('bathroom', 10, 10),
            Room('bedroom', 15, 8)
        ]

        self.rooms[0].add_forniture(self.forniture['window'], 10, 100)

        self.persons = []

    def add_person(self, person):
        self.persons.append(person)

    def update(self, dt):

        for r in self.rooms:
            r.update(dt)
