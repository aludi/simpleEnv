import mesa
import math
import random
from colour import Color



class WalkAgent(mesa.Agent):
    """An agent walking to a town."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.goal = None
        r = Color("#660000")
        o = Color("#f44336")
        color_list = list(o.range_to(r, 20))
        self.color = random.choice(color_list).hex

class Patch(mesa.Agent):
    def __init__(self, unique_id, model, acidic):
        super().__init__(unique_id, model)
        self.value = acidic
        self.node_name = "acidic"


class Flower1(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Flower2(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)