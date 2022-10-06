import mesa
from model import SimpleEnv
from agents import Walker, Patch, Flower1, Flower2
import os, sys, subprocess
from viz import AttributeElement, AgentProbabilities


def agent_portrayal(agent):
    if type(agent) == Patch:
        if agent.value == 1:
            portrayal = {
                "Shape": "rect",
                "Filled": "#b2de27",    # dark green, base
                "Layer": 1,
                "Color": "#b2de27",
                "w":1,
                "h":1
            }
        else:
            portrayal = {
                "Shape": "rect",
                "Filled": "#6ed747",    # light green, acidic
                "Layer": 1,
                "Color": "#6ed747",
                "w": 1,
                "h": 1
            }

    elif type(agent) == Flower2:
        portrayal = {
            "Shape": "circle",
            "Filled": "#FFC300",    # yellow = flower 2 = likes base
            "Layer": 3,
            "Color": "#FFC300",
            "r": 0.5,
        }
    elif type(agent) == Flower1:
        portrayal = {
            "Shape": "circle",
            "Filled": "#FF5733",    # red = flower1 = likes acid
            "Layer": 2,
            "Color": "#FF5733",
            "r": 0.5,
        }

    elif type(agent) == Walker:
        portrayal = {
            "Shape": "circle",
            "Filled": "black",  # walker
            "Layer": 5,
            "Color": "black",
            "r": 0.25

        }

    return portrayal

def p_a(agent):
    if type(agent) == Walker:
        if agent.agent_name == "alice":
            portrayal = {
                "Shape": f"out/agent_data/generated/{agent.model.model}_{agent.agent_name}_pic.png",
                "Filled": "black",  # walker
                "Layer": 5,
                "Color": "black",
                "scale":20
            }
        else:
            portrayal = {
                "Shape": "circle",
                "Filled": "white",  # walker
                "Layer": 1,
                "Color": "white",
                "r": 1
            }
    else:
        portrayal = {
            "Shape": "circle",
            "Filled": "white",  # walker
            "Layer": 1,
            "Color": "white",
            "r": 1
        }
    return portrayal

def p_b(agent):
    if type(agent) == Walker:
        if agent.agent_name == "bob":
            portrayal = {
                "Shape": f"out/agent_data/generated/{agent.model.model}_{agent.agent_name}_pic.png",
                "Filled": "black",  # walker
                "Layer": 5,
                "Color": "black",
                "scale":20
            }
        else:
            portrayal = {
                "Shape": "circle",
                "Filled": "white",  # walker
                "Layer": 1,
                "Color": "white",
                "r": 1
            }
    else:
        portrayal = {
            "Shape": "circle",
            "Filled": "white",  # walker
            "Layer": 1,
            "Color": "white",
            "r": 1
        }
    return portrayal



def server_main_call(model):
    w = 25
    h = 25
    grid = mesa.visualization.CanvasGrid(agent_portrayal, w, h, 500, 500)
    p1 = AgentProbabilities("alice")
    p2 = AgentProbabilities("bob")


    m = AttributeElement("model")
    d = AttributeElement("domain")
    r = AttributeElement("rules")
    a = AttributeElement("causes")


    server = mesa.visualization.ModularServer(
        SimpleEnv, [m, grid, d, a, p1, p2], "Simple Env Model", {"N": 2, "width": w, "height": h, "model": model}
    )
    server.port = 8521  # The default
    server.launch()

if __name__ == "__main__":
    server_main_call("M1")
