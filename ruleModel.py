import random
import bn


class Event:
    def __init__(self, name, o1, o2):
        self.name = name
        self.outcome1 = o1
        self.outcome2 = o2

class Rule:
    def __init__(self, antecedent, consequent, probability):
        self.antecedent = antecedent    #list of the shape [(name, value), (name, value)...])
        (self.c_nn, self.c_val) = consequent
        self.p = probability
        list_premise = []
        for (name, value) in self.antecedent:
            list_premise.append(f"{name} : {value}")
        str_premise = ",".join(list_premise)
        self.rule_name = f"{str_premise} --> {self.c_nn}:{self.c_val}"


class Knowledge_Structure:
    def __init__(self, model):
        self.model_name = model
        self.domain = domain(model)
        self.rules = rules(model)
        self.arcs = self.find_causal_structure()
        self.print_arcs()
        print()


    def find_causal_structure(self):
        list_causal = []
        for node in self.domain.keys():
            for rule in self.rules:
                if rule.c_nn == node:
                    for (atr, val) in rule.antecedent:
                        if atr != "":
                            list_causal.append((atr, rule.c_nn))
        unpruned_list = list(dict.fromkeys(list_causal))
        rm_list = []
        for (arc_p, arc_c) in unpruned_list:
            if arc_p == arc_c:
                rm_list.append((arc_p, arc_c))
        for x in rm_list:
            unpruned_list.remove(x)
        #print(unpruned_list)
        return unpruned_list

    def print_arcs(self):
        for (p, c) in self.arcs:
            print(f"{p} -> {c}")

    def forward_chaining_from_contents(self, content_list):
        new_facts = []
        changed_facts = []
        unchanged_facts = []

        rules_fired = []
        if content_list == []:
            for rule in self.rules:
                premise = rule.antecedent
                (first_name, first_value) = premise[0]
                if first_name == "":
                    if random.random() <= rule.p:
                        new_facts.append((rule.c_nn, rule.c_val))
                    else:
                        complement_val = self.find_complement(rule.c_nn, rule.c_val)
                        new_facts.append((rule.c_nn, complement_val))
                    rules_fired.append(rule)
        else:
            for item in content_list:
                if item.item_class is not "agent":
                    unchanged_facts.append((item.node_name, item.value))
            for rule in self.rules:
                premise = rule.antecedent
                premise_true = True
                for p_n in premise:
                    if p_n not in unchanged_facts:
                        premise_true = False
                if premise_true and random.random() <= rule.p:
                    # the conclusion is true, and should be added
                    new_facts.append((rule.c_nn, rule.c_val))

            del_list = []
            for (attr, value) in new_facts:
                if (attr, self.find_complement(attr, value)) in unchanged_facts:
                    unchanged_facts.remove((attr, self.find_complement(attr, value)))
                    changed_facts.append((attr, value))
                if (attr, value) in unchanged_facts:
                    # fact is not new, rule already fired, so this can be rmovied
                    del_list.append((attr, value))
            for item in del_list:
                new_facts.remove(item)


        #print("new facts", new_facts)
        #print("changed facts",changed_facts)
        #print("old facts", unchanged_facts)

        return new_facts, changed_facts, unchanged_facts




    def forward_chaining(self):
        facts_found = []
        rules_fired = []
        flag = 1
        while flag == 1:
            flag = 0
            for rule in self.rules:
                premise = rule.antecedent
                (first_name, first_value) = premise[0]
                if first_name == "":
                    if random.random() <= rule.p:
                        facts_found.append((rule.c_nn, rule.c_val))
                    else:
                        complement_val = self.find_complement(rule.c_nn, rule.c_val)
                        facts_found.append((rule.c_nn, complement_val))
                    rules_fired.append(rule)
                else:
                    premise = rule.antecedent
                    premise_true = True
                    for p_n in premise:
                        if p_n not in facts_found:
                            premise_true = False
                    if premise_true and rule not in rules_fired and (rule.c_nn, rule.c_val) not in facts_found:
                        rules_fired.append(rule)
                        if random.random() <= rule.p:
                            if (rule.c_nn, rule.c_val) not in facts_found:
                                facts_found.append((rule.c_nn, rule.c_val))
                            if (rule.c_nn, self.find_complement(rule.c_nn, rule.c_val)) in facts_found: # by conflict, remove old fact
                                facts_found.remove((rule.c_nn, self.find_complement(rule.c_nn, rule.c_val)))
                            flag = 1
        #print(facts_found)
        return facts_found



    def find_complement(self, name, outcome):   # only works for binary
        if outcome == self.domain[name].outcome1:
            return self.domain[name].outcome2
        else:
            return self.domain[name].outcome1


def domain(model):
    D = {}
    if model in ["M1", "M2", "M3", "M4"]:
        D_list = [("acidic", 1, 0), ("f1", 0, 1), ("f2", 0, 1)]
        for (name, o1, o2) in D_list:
            D[name] = Event(name, o1, o2)
    else:
        D = {}
    return D

def rules(model):
    KB = []
    if model == "M1":   # acid causes some flowers to grow or not # acidic --> f1, base --> f2
        KB.append(Rule([("","")], ("acidic", 1), 0.5))
        KB.append(Rule([("acidic", 1)], ("f1", 1), 0.1))
        KB.append(Rule([("acidic", 0)], ("f1", 1), 0.01))
        KB.append(Rule([("acidic", 1)], ("f2", 1), 0.01))
        KB.append(Rule([("acidic", 0)], ("f2", 1), 0.1))
        # a flower on the wrong ground dies
        KB.append(Rule([("acidic", 1), ("f2", 1)], ("f2", 0), 1))
        KB.append(Rule([("acidic", 0), ("f1", 1)], ("f1", 0), 1))
        # flower has some probability of dying randomly
        KB.append(Rule([("f1", 1)], ("f1", 0), 0.005))
        KB.append(Rule([("f2", 1)], ("f2", 0), 0.005))

    elif model == "M2": # "flowers cause the floor to become acidic or not"
        KB.append(Rule([("", "")], ("acidic", 1), 0.5))
        KB.append(Rule([("", "")], ("f1", 1), 0.25))
        KB.append(Rule([("", "")], ("f2", 1), 0.25))
        KB.append(Rule([("f1", 1)], ("acidic", 1), 1))
        KB.append(Rule([("f2", 1)], ("acidic", 0), 1))
        # ground randomly changes from acid to base or reversed
        KB.append(Rule([("acidic", 0)], ("acidic", 1), 0.025))
        KB.append(Rule([("acidic", 1)], ("acidic", 0), 0.025))
        KB.append(Rule([("acidic", 1), ("f1", 1)], ("acidic", 1), 1))
        KB.append(Rule([("acidic", 0), ("f2", 0)], ("acidic", 0), 1))

    elif model == "M3":
        KB.append(Rule([("", "")], ("acidic", 1), 0.9))
        KB.append(Rule([("", "")], ("f1", 1), 0.5))
        KB.append(Rule([("f1", 1)], ("acidic", 0), 0.4))
        KB.append(Rule([("acidic", 0)], ("f2", 1), 0.5))

    elif model == "M4":
        KB.append(Rule([("", "")], ("f1", 1), 1))
        KB.append(Rule([("", "")], ("acidic", 0), 1))
        KB.append(Rule([("f1", 1)], ("acidic", 1), 0.99))
        KB.append(Rule([("f1", 1)], ("f2", 1), 0.6))
        KB.append(Rule([("f1", 1)], ("f1", 0), 0.2))



    else:
        pass
    return KB

if __name__ == "__main__":
    for model in ["M1", "M2", "M3", "M4"]:
        ks = Knowledge_Structure(model)
        bn.generate_ground_BN(ks)