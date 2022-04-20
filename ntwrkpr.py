###### Equality model, neighbors give to poorer neighbors, histogram should be a box.
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
#import networkx as nx #to use network grid instead of multigrid


class MoneyAgent(Agent):
    """Find closest neighbors that are poorer and give them money."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            if other_agent.wealth < self.wealth: # Only give money to poorer neighbors
                other_agent.wealth += 1
                self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()



class GivingModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True) # This allows agents to share a grid
        # think of it as some kind of homophily in the network.
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
                
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

