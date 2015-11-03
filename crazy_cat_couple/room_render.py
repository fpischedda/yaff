import pyglet.resource
import pyglet.sprite
import pyglet.graphics


def get_room_wall_image(room):

    filename = 'res/rooms/walls/{}.jpg'.format(room.wall_variant)
    return pyglet.resource.image(filename)


def get_forniture_image(forniture):

    filename = 'res/forniture/{}.png'.format(forniture.name)
    return pyglet.resource.image(filename)


class RoomRender:

    def __init__(self, room):
        self.room = room
        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.foreground_group = pyglet.graphics.OrderedGroup(1)
        self.info_group = pyglet.graphics.OrderedGroup(2)

        self.batch = pyglet.graphics.Batch()

        wall_bg = get_room_wall_image(room)

        self.wall_sprite = pyglet.sprite.Sprite(wall_bg,
                                                x=0, y=0,
                                                batch=self.batch,
                                                group=self.background_group)

        forniture_placements = []
        for e in room.elements:
            elem_img = get_forniture_image(e.forniture)
            fs = pyglet.sprite.Sprite(elem_img,
                                      x=e.x, y=e.y,
                                      batch=self.batch,
                                      group=self.foreground_group)
            forniture_placements.append(fs)

        self.forniture_placements = forniture_placements

        pyglet.text.Label(room.name,
                          font_name='Times New Roman',
                          font_size=16,
                          x=100, y=350,
                          batch=self.batch, group=self.info_group)

    def render(self):
        self.batch.draw()
