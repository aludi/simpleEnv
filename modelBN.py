import mesa
from agents import WalkAgent, Patch, Flower1, Flower2
import random
import bn

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

        self.global_info = {"acidic & flower1": 0,
                            "acidic & flower2": 0,
                            "not acidic & flower1": 0,
                            "not acidic & flower2": 0
                            }

        for (contents, x, y) in self.grid.coord_iter():
            bn.find_parents("acidic")
            p = Patch(i, self, bn.find_outcome("acidic", {}))
            self.schedule.add(p)
            self.grid.place_agent(p, (x, y))
            i += 1

            list_parents = bn.find_parents("flower1")

            print("parents : ", list_parents)
            flower1 = bn.find_outcome("flower1", {p.node_name : p.value})
            if flower1 == "t":
                f1 = Flower1(i, self)
                self.schedule.add(f1)
                self.grid.place_agent(f1, (x, y))
                i += 1
                if p.value == "t":
                    self.global_info["acidic & flower1"] += 1
                else:
                    self.global_info["not acidic & flower1"] += 1

            list_parents = bn.find_parents("flower2")
            print("parents : ", list_parents)

            flower2 = bn.find_outcome("flower2", {p.node_name : p.value})
            if flower2 == "t":
                f2 = Flower2(i, self)
                self.schedule.add(f2)
                self.grid.place_agent(f2, (x, y))
                i += 1

                if p.value == "t":
                    self.global_info["acidic & flower2"] += 1
                else:
                    self.global_info["not acidic & flower2"] += 1


        total = width*height
        sum = 0
        for key in self.global_info.keys():
            print(key, "  :  ", self.global_info[key]/total)
            sum += self.global_info[key]/total
        print(sum)



        # Create agents
        for i in range(self.num_agents):
            a = WalkAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            a.goal = random.choice(self.towns)

        self.running = True



    def step(self):
        self.schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()