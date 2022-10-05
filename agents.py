import mesa
import csv
import math
import random
from colour import Color
from collections import defaultdict
import bn

class Patch(mesa.Agent):
    def __init__(self, unique_id, model, acidic):
        super().__init__(unique_id, model)
        self.item_class = "object"
        self.value = acidic
        self.node_name = "acidic"
        self.birthday = model.schedule.time

    def set_value(self, value):
        self.value = value

class Flower1(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.item_class = "object"
        self.node_name = "f1"
        self.value = 1
        self.birthday = model.schedule.time

class Flower2(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.item_class = "object"
        self.node_name = "f2"
        self.value=1
        self.birthday = model.schedule.time

class Walker(mesa.Agent):
    def __init__(self, unique_id, model, blind, taste, name):
        super().__init__(unique_id, model)
        self.item_class = "agent"
        self.node_name = "walker"
        self.agent_name = name
        self.value = 1
        self.see = blind
        self.taste = taste
        self.observation = []
        self.domain_knowledge = []

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def observe(self, iter):
        dict_obs = defaultdict(dict)
        for item in iter:
            if item.item_class != "agent":
                dict_obs[item.pos][item.node_name] = item.value
                self.domain_knowledge.append(item.node_name)    # the agent now knows that this class of object exists
        for pos_key in dict_obs.keys():
            d = dict_obs[pos_key]
            for obj in self.domain_knowledge:
                if obj not in d.keys():
                    d[obj] = 0
            self.observation.append(d)

        with open(f"out/agent_data/{self.model.model}_{self.agent_name}.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.observation[0].keys(), extrasaction='ignore')
            writer.writeheader()
            for data in self.observation:
                writer.writerow(data)


    def create_bn(self):
        bn.generate_agent_BN(self.model.model, self.agent_name)






