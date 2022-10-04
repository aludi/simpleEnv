import mesa
import math
import random
from colour import Color

class Patch(mesa.Agent):
    def __init__(self, unique_id, model, acidic):
        super().__init__(unique_id, model)
        self.value = acidic
        self.node_name = "acidic"
        self.birthday = model.schedule.time

    def set_value(self, value):
        self.value = value

class Flower1(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.node_name = "f1"
        self.value = 1
        self.birthday = model.schedule.time

class Flower2(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.node_name = "f2"
        self.value=1
        self.birthday = model.schedule.time

class Walker(mesa.Agent):
    def __init__(self, unique_id, model, blind, taste):
        super().__init__(unique_id, model)
        self.see = blind
        self.taste = taste

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


