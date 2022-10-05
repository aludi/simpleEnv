import mesa
from model import SimpleEnv
from agents import Walker, Patch, Flower1, Flower2


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
            "r": 0.25,
        }

    return portrayal


def server_main_call(model):
    w = 25
    h = 25
    grid = mesa.visualization.CanvasGrid(agent_portrayal, w, h, 500, 500)

    server = mesa.visualization.ModularServer(
        SimpleEnv, [grid], "Simple Env Model", {"N": 10, "width": w, "height": h, "model":model}
    )
    server.port = 8521  # The default
    server.launch()

if __name__ == "__main__":
    server_main_call("M4")