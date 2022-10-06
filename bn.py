import pyAgrum as gum
import pyAgrum.lib.image as gim
import random
from ruleModel import Knowledge_Structure
### input BN

def make_input_bn():
    bn = gum.loadBN("input_bns/acidic.net")
    ie=gum.LazyPropagation(bn)
    gim.exportInference(model=bn, filename="input_bns/image.pdf", engine=ie, evs={})

def prior_prob(node_name, dict_):
    bn = gum.loadBN("input_bns/acidic.net")
    p = bn.cpt(bn.idFromName(node_name))
    for i in p.loopIn():
        d = i.todict(withLabels=True)
        if d[node_name] == 't':
            del d[node_name]
            if d == dict_:
                print(node_name, p.get(i))
                return p.get(i)


def find_outcome(node_name, dict_):
    print(node_name)
    p = prior_prob(node_name, dict_)
    r = random.random()
    print(p, r, r<=p)
    print()
    if r <= p:
        return "t"
    else:
        return "f"

def find_parents(node_name):
    bn = gum.loadBN("input_bns/acidic.net")
    p = bn.parents(bn.idFromName(node_name))
    list_parents = []
    if len(p) > 0:
        for x in p:
            list_parents.append(get_node_name_from_id(x))
    return list_parents


def get_node_name_from_id(id, network):
    bn = gum.loadBN("input_bns/acidic.net")
    for name in bn.names():
        if bn.idFromName(name) == id:
            return name

##### generate BNs

def generate_ground_BN(ks):
    bn = gum.BayesNet(ks.model_name)
    for node in ks.domain.keys():
        a = bn.add(gum.LabelizedVariable(node, node, 2))
    for (arc_p, arc_c) in ks.arcs:
        bn.addArc(arc_p, arc_c)

    learner = gum.BNLearner(f"out/data/{ks.model_name}.csv", False)
    bn_learned = learner.learnParameters(bn.dag())

    ie = gum.LazyPropagation(bn_learned)
    gim.exportInference(model=bn_learned, filename=f"out/grounded/ground_{ks.model_name}_pic.pdf", engine=ie,
                        evs={})
    gim.exportInference(model=bn, filename=f"out/inferenced/ground_{ks.model_name}_pic_a.pdf", engine=ie,
                        evs={'acidic': 1})

    output_file = f"output_bns/ground_{ks.model_name}.net"
    gum.saveBN(bn_learned, output_file)

def generate_agent_BN(model_output, agent_name):
    file = f"out/agent_data/{model_output}_{agent_name}.csv"

    learner = gum.BNLearner(f"out/agent_data/{model_output}_{agent_name}.csv", False)
    bn = learner.learnBN()
    output_file = f"out/agent_data/output_network/{model_output}_{agent_name}.net"
    gum.saveBN(bn, output_file)
    ie = gum.LazyPropagation(bn)
    gim.exportInference(model=bn, filename=f"out/agent_data/generated/{model_output}_{agent_name}_pic.png", engine=ie,
                        evs={})
    try:
        gim.exportInference(model=bn, filename=f"out/agent_data/inferenced/{model_output}_{agent_name}_pic_a.png", engine=ie,
                        evs={'acidic': 1})
        print(f"updated bayesian network of agent {agent_name}")

    except gum.pyAgrum.InvalidArgument:
        print("non-probabilistic environment")

    dict_representation_network = {}
    for node in bn.names():
        l = []
        for n in bn.parents(node):
            for name in bn.names():
                if bn.idFromName(name) == n:
                    l.append(name)
        dict_representation_network[node] = l
    return dict_representation_network

def predict_output(event_name, value_dict, bn_file):
    bn = gum.loadBN(bn_file)
    ie = gum.LazyPropagation(bn)
    try:
        ie.setEvidence(value_dict)
    except gum.pyAgrum.NotFound:
        print("agent doesn't know about this thing yet")

    try:
        x = ie.posterior(event_name)
    except gum.pyAgrum.NotFound:
        print("agent doesn't know about this thing yet")
        x = {}
        x[0] = 1
        x[1] = 0
    return x[0], x[1]


def generate_BN(model_output):
    learner = gum.BNLearner(f"out/data/{model_output}.csv", False)
    bn = learner.learnBN()
    output_file = f"output_bns/{model_output}.net"
    gum.saveBN(bn, output_file)
    ie = gum.LazyPropagation(bn)
    gim.exportInference(model=bn, filename=f"out/generated/{model_output}_pic.pdf", engine=ie,
                        evs={})
    gim.exportInference(model=bn, filename=f"out/inferenced/{model_output}_pic_a.pdf", engine=ie,
                        evs={'acidic':1})
