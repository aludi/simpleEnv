import random



class Event:
    def __init__(self, name, o1, o2):
        self.name = name
        self.outcome1 = o1
        self.outcome2 = o2

class Rule:
    def __init__(self, antecedent, consequent, probability):
        (self.a_nn, self.a_val) = antecedent
        (self.c_nn, self.c_val) = consequent
        self.p = probability
        self.rule_name = f"{self.a_nn}:{self.a_val} --> {self.c_nn}:{self.c_val}"


class Knowledge_Structure:
    def __init__(self, model):
        if model == "M1":
            self.domain = domain(model)
            self.rules = rules(model)

    def forward_chaining(self):
        facts_found = []
        rules_fired = []
        flag = 1
        while flag == 1:
            flag = 0
            for rule in self.rules:
                if facts_found == [] and rule.a_nn == "":
                    if random.random() <= rule.p:
                        facts_found.append((rule.c_nn, rule.c_val))
                    else:
                        complement_val = self.find_complement(rule.c_nn, rule.c_val)
                        facts_found.append((rule.c_nn, complement_val))
                    rules_fired.append(rule)
                else:
                    if (rule.a_nn, rule.a_val) in facts_found and rule not in rules_fired:
                        rules_fired.append(rule)
                        if random.random() <= rule.p:
                            facts_found.append((rule.c_nn, rule.c_val))
                            flag = 1
            return facts_found

    def find_complement(self, name, outcome):   # only works for binary
        if outcome == self.domain[name].outcome1:
            return self.domain[name].outcome2
        else:
            return self.domain[name].outcome1

def domain(model):
    D = {}
    if model == "M1":
        D_list = [("acidic", 1, 0), ("f1", 0, 1), ("f2", 0, 1)]
        for (name, o1, o2) in D_list:
            D[name] = Event(name, o1, o2)

    else:
        D = {}
    return D

def rules(model):
    KB = []
    if model == "M1":    # acidic --> f1, base --> f2
        KB.append(Rule(("",""), ("acidic", 1), 0.8))
        KB.append(Rule(("acidic", 1), ("f1", 1), 0.9))
        KB.append(Rule(("acidic",0), ("f2", 1), 0.9))
        KB.append(Rule(("acidic",1), ("f2", 1), 0.1))
        KB.append(Rule(("acidic",0), ("f1", 1), 0.1))
    else:
        pass
    return KB