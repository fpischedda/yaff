from transitions import Machine
from property import DynamicProperty


class Human(Machine):

    def __init__(self, name, sex, age, **options):

        states = ['idle', 'walking', 'eating', 'talking']
        transitions = [
            {'trigger': 'rest', 'source': '*', 'dest': 'idle'},
            {'trigger': 'eat', 'source': '*', 'dest': 'eating'},
            {'trigger': 'talk', 'source': '*', 'dest': 'talking'}
        ]

        super(Human, self).__init__(model=self, states=states,
                                    transitions=transitions,
                                    initial='idle')

        self.name = name
        self.sex = sex
        self.age = age

        self.properties = {
            'energy': DynamicProperty(name='energy',
                                      initial_cost=100,
                                      min_value=0,
                                      max_value=100,
                                      decay_by_sec=0.01,
                                      gain_by_sec=0.01),
            'stress': DynamicProperty(name='stress',
                                      initial_value=0,
                                      min_value=0,
                                      max_value=100,
                                      decay_by_sec=0.01,
                                      gain_by_sec=0.01)
        }

        opts = dict(Human.DEFAULT_OPTIONS, **options)
        self.__dict__.update(opts)

    def update(self, dt):
        for p in self.properties.values():
            p.decay(dt)
