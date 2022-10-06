from mesa.visualization.modules.TextVisualization import TextElement
from mesa.visualization.ModularVisualization import VisualizationElement
from collections import defaultdict

class AttributeElement(TextElement):
    def __init__(self, attr_name):
        '''
        Create a new text attribute element.

        Args:
            attr_name: The name of the attribute to extract from the model.

        Example return: "happy: 10"
        '''
        self.attr_name = attr_name

    def render(self, model):
        val = getattr(model, self.attr_name)
        return self.attr_name + ": " + str(val)

class AgentProbabilities(TextElement):
    def __init__(self, ag_name):
        '''
        Create a new text attribute element.

        Args:
            attr_name: The name of the attribute to extract from the model.

        Example return: "happy: 10"
        '''
        self.agent_name = ag_name

    def render(self, model):
        m = model.model
        z = ""
        for agents in model.walkerAgents:
            if agents.agent_name == self.agent_name:
                x = agents.agent_name
                y = agents.bn_struct
                z += f"{x}: {y}"
        return z





class Image(VisualizationElement):
    local_includes = ["ImageModule.js"]
    js_code = "elements.push(new ImageModule());"