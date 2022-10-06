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
        self.agent_names = ["alice", "bob", "carol"]    # consistency
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.model = model
        self.Ks = Knowledge_Structure(self.model)
        self.domain = self.Ks.domain
        self.rules = self.Ks.render_rules()
        self.causes = self.Ks.render_arcs()
        self.statistics = Statistics(self)
        self.update_world()
        self.create_agents()
        self.prediction_dict = self.create_prediction_dict()
        self.running = True
        self.statistics.collect_statistics()


    def create_prediction_dict(self):
        d = {}
        for a in self.walkerAgents:
            d[a.agent_name] = 0
        d["grounded"] = 0
        return d

    def create_agents(self):
        self.walkerAgents = []
        it = 0
        while it < self.num_agents:
            a = Walker(self.i, self, True, True, self.agent_names[it])
            self.i += 1
            self.schedule.add(a)
            self.walkerAgents.append(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            it += 1


    def agent_movement(self):
        for agents in self.walkerAgents:
            agents.move()

    def update_agents(self):
        #self.agent_movement()
        for agent in self.walkerAgents:
            iter = self.grid.iter_neighbors(agent.pos, True, True, radius=1)
            agent.observe(iter)
            agent.create_bn()


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



    def prediction(self):
        print("Running tournament")
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        pos = (x, y) # is a random position
        # draw randomly from domain
        event_to_predict = random.choice(list(self.Ks.domain.keys()))
        print(f"\t Selected {event_to_predict} randomly to be predicted")
        val_dict = {}
        c = self.grid.get_cell_list_contents(pos)
        correct_result = 0
        for item in c:
            if item.node_name != event_to_predict:
                val_dict[item.node_name] = item.value
            else:
                correct_result = item.value

        for all_items in self.domain.keys():
            if all_items not in val_dict.keys():
                if all_items != event_to_predict:
                    val_dict[all_items] = 0

        print(f"\t correct result... {event_to_predict} = {correct_result}")
        print(val_dict)

        for agent in self.walkerAgents:
            P_0, P_1 = bn.predict_output(event_to_predict, val_dict, agent.bn_file)    # predict output per agent
            print(f"\t Agent {agent.agent_name} predicts {event_to_predict} with a probability of {round(P_1, 3)}, "
                  f"({int(int(round(P_1, 0)) == correct_result)})")
            self.prediction_dict[agent.agent_name] += int(int(round(P_1, 0)) == correct_result)

        grounded_bn = f"output_bns/ground_{self.model}.net"
        P_0, P_1 = bn.predict_output(event_to_predict, val_dict, grounded_bn)  # predict output per agent
        print(f"\t Grounded BN predicts {event_to_predict} with a probability of {round(P_1, 3)},"
              f" ({int(int(round(P_1, 0)) == correct_result)})")
        self.prediction_dict["grounded"] += int(int(round(P_1, 0)) == correct_result)

    def step(self):
        self.update_world()
        self.update_agents()
        self.prediction()
        self.schedule.step()
        print(self.prediction_dict)

    def run_model(self, n):
        for i in range(n):
            self.step()
