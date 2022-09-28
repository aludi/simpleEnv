import pyAgrum as gum
import pyAgrum.lib.image as gim
import random


bn = gum.loadBN("bns/acidic.net")
ie=gum.LazyPropagation(bn)
gim.exportInference(model=bn, filename="bns/image.pdf", engine=ie, evs={})

def prior_prob(node_name, dict_):
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
    p = bn.parents(bn.idFromName(node_name))
    list_parents = []
    if len(p) > 0:
        for x in p:
            list_parents.append(get_node_name_from_id(x))
    return list_parents


def get_node_name_from_id(id):
    for name in bn.names():
        if bn.idFromName(name) == id:
            return name
