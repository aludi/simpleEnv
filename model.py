import mesa
from agents import WalkAgent, Patch, Flower1, Flower2
import random
import bn
from itertools import chain, combinations, product
from ruleModel import Knowledge_Structure
from colour import Color






class SimpleEnv(mesa.Model):
    """A simple model of an economy where agents exchange currency at random.
    All the agents begin with one unit of currency, and each time step can give
    a unit of currency to another agent. Note how, over time, this produces a
    highly skewed distribution of wealth.
    """

    def __init__(self, N=0, width=10, height=10):
        i = 0
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.Ks = Knowledge_Structure("M1")
        self.item_dict = self.init_item_dict()
        for (contents, x, y) in self.grid.coord_iter():
            cell_contents = self.Ks.forward_chaining()
            for (attribute, value) in cell_contents:
                if attribute == "acidic":
                    a = Patch(i, self, value)
                elif attribute == "f1":
                    a = Flower1(i, self)
                elif attribute == "f2":
                    a = Flower2(i, self)
                else:
                    print("no idea what you're doing!")
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                i += 1
            self.counting(cell_contents)
        self.running = True
        self.collect_statistics()



    def init_item_dict(self):
        C = {}
        get_combos = []
        valuations = list(product([0,1], repeat=len(self.Ks.domain.keys())))
        keys = list(self.Ks.domain.keys())
        for val in valuations:
            new_key = []
            for i in range(0, len(keys)):
                s = keys[i] + "=" + str(val[i])
                new_key.append(s)
            C[tuple(new_key)] = 0
        return C

    def collect_statistics(self):
        #print(self.item_dict)
        total = self.grid.width*self.grid.height
        sum = 0
        for key in self.item_dict.keys():
            print(f"{key}  :  {(self.item_dict[key]/total)*100}")
            sum += (self.item_dict[key]/total)*100
        print(sum)

    def counting(self, cell_item):
        d = {}
        keys = list(self.Ks.domain.keys())
        # assume that nothing is found:
        for key in keys:
            d[key] = 0
        for (name, val) in cell_item:
            d[name] = val
        # convert d to relevant string format
        l = []
        for key in d.keys():
            l.append(f"{key}={str(d[key])}")
        # then update statistics
        self.item_dict[tuple(l)] += 1



    def step(self):
        self.schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()