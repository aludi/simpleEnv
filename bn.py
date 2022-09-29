import pyAgrum as gum
import pyAgrum.lib.image as gim
import random

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


def get_node_name_from_id(id):
    bn = gum.loadBN("input_bns/acidic.net")
    for name in bn.names():
        if bn.idFromName(name) == id:
            return name

##### generate BNs

def generate_BN(model_output):
    learner = gum.BNLearner(f"out/{model_output}.csv", False)
    print(learner)
    bn = learner.learnBN()
    output_file = f"output_bns/{model_output}.net"
    gum.saveBN(bn, output_file)
    ie = gum.LazyPropagation(bn)
    gim.exportInference(model=bn, filename=f"out/{model_output}_pic.pdf", engine=ie,
                        evs={})
    gim.exportInference(model=bn, filename=f"out/{model_output}_pic_a.pdf", engine=ie,
                        evs={'acidic':1})
