import mesa
from model import SimpleEnv
from agents import WalkAgent, Patch, Flower1, Flower2


def agent_portrayal(agent):

    if type(agent) == Patch:
        if agent.value == 1:
            portrayal = {
                "Shape": "rect",
                "Filled": "#b2de27",
                "Layer": 1,
                "Color": "#b2de27",
                "w":1,
                "h":1
            }
        else:
            portrayal = {
                "Shape": "rect",
                "Filled": "#6ed747",
                "Layer": 1,
                "Color": "#6ed747",
                "w": 1,
                "h": 1
            }

    elif type(agent) == Flower2:
        portrayal = {
            "Shape": "circle",
            "Filled": "#FFC300",
            "Layer": 3,
            "Color": "#FFC300",
            "r": 0.5,
        }
    elif type(agent) == Flower1:
        portrayal = {
            "Shape": "circle",
            "Filled": "#FF5733",
            "Layer": 2,
            "Color": "#FF5733",
            "r": 0.5,
        }

    return portrayal



    if type(agent) == WalkAgent:


        portrayal = {
            "Shape": "circle",
            "Filled": agent.color,
            "Layer": 1,
            "Color": agent.color,
            "r": 0.5,
        }

        if agent.state == "dead":
            portrayal = {
                "Shape": "img/skull.png",
                "Filled": agent.color,
                "Layer": 1,
                "Color": agent.color,
                "r": 0.5,
            }

    else:
        portrayal = {
            "Shape": "rect",
            "Filled": "orange",
            "Layer": 0,
            "Color": "orange",
            "h": 3,
            "w":3
        }

    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 50, 50, 500, 500)


server = mesa.visualization.ModularServer(
    SimpleEnv, [grid], "Simple Env Model", {"N": 0, "width": 50, "height": 50}
)
server.port = 8521  # The default
server.launch()