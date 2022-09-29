import mesa
from agents import WalkAgent, Patch, Flower1, Flower2
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

    def __init__(self, N=0, width=10, height=10, model="M1"):
        i = 0
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.model = model
        self.Ks = Knowledge_Structure(self.model)
        self.statistics = Statistics(self)
        for (contents, x, y) in self.grid.coord_iter():
            cell_contents = self.Ks.forward_chaining()
            for (attribute, value) in cell_contents:
                if attribute == "acidic":
                    a = Patch(i, self, value)
                    i += 1
                    self.schedule.add(a)
                    self.grid.place_agent(a, (x, y))
                elif attribute == "f1":
                    if value != 0:
                        a = Flower1(i, self)
                        i += 1
                        self.schedule.add(a)
                        self.grid.place_agent(a, (x, y))
                elif attribute == "f2":
                    if value != 0:
                        a = Flower2(i, self)
                        i += 1
                        self.schedule.add(a)
                        self.grid.place_agent(a, (x, y))
                else:
                    print("no idea what you're doing!")
            self.statistics.counting(cell_contents)
        self.running = True
        self.statistics.collect_statistics()

    def step(self):
        self.schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()