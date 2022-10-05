import mesa
from agents import Walker, Patch, Flower1, Flower2
import random
import bn
from ruleModel import Knowledge_Structure
from statistics import Statistics
from colour import Color


class SimpleEnv(mesa.Model):
    """A simple model of an economy where agents exchange currency at random.
    All the agents begin with one unit of currency, and each time step can give
    a unit of currency to another agent. Note how, over time, this produces a
    highly skewed distribution of wealth.
    """

    def __init__(self, N, width=10, height=10, model="M1"):
        self.i = 0
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.model = model
        self.Ks = Knowledge_Structure(self.model)
        self.statistics = Statistics(self)
        self.update_world()
        #self.create_agents()
        self.running = True
        self.statistics.collect_statistics()

    def create_agents(self):
        self.walkerAgents = []
        x = 0
        while x < self.num_agents:
            a = Walker(self.i, self, True, True)
            self.i += 1
            self.schedule.add(a)
            self.walkerAgents.append(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def agent_movement(self):
        for agents in self.walkerAgents:
            agents.move()

    def update_world(self):
        self.statistics.rezero_item_dict()
        for (contents, x, y) in self.grid.coord_iter():
            new_facts, changed_facts, unchanged_facts = self.Ks.forward_chaining_from_contents(contents)
            for (attribute, value) in new_facts:
                if attribute == "acidic":
                    a = Patch(self.i, self, value)
                    self.i += 1
                    self.schedule.add(a)
                    self.grid.place_agent(a, (x, y))
                elif attribute == "f1":
                    if value != 0:
                        a = Flower1(self.i, self)
                        self.i += 1
                        self.schedule.add(a)
                        self.grid.place_agent(a, (x, y))
                elif attribute == "f2":
                    if value != 0:
                        a = Flower2(self.i, self)
                        self.i += 1
                        self.schedule.add(a)
                        self.grid.place_agent(a, (x, y))
                else:
                    print("no idea what you're doing!")
            del_list = []
            for (attribute, value) in changed_facts:
                for item in contents:
                    if attribute == "acidic" and type(item) == Patch:
                        item.set_value(value)
                    elif attribute == "f1" and type(item) == Flower1:
                        if value == 0:
                            del_list.append(item)
                    elif attribute == "f2" and type(item) == Flower2:
                        if value == 0:
                            del_list.append(item)
            for item in del_list:
                self.grid.remove_agent(item)
                self.schedule.remove(item)
            self.statistics.counting(new_facts+changed_facts+unchanged_facts)

    def step(self):
        self.update_world()
        #self.agent_movement()
        self.schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()
