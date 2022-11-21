import mesa
import random
import math

class MinionAgent(mesa.Agent):     
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 2
        self.width = 1
        self.prevCells = []
        self.stepsToDestination = 0
        self.destination = None
        self.randomSteps = 0
        self.destinationSteps = 0

    def mantainPrevCells(self):
        while len(self.prevCells) >= 25:
            self.prevCells.pop()

    def randomMove(self):
        neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        while not self.model.grid.is_cell_empty(neighborCell) and (not neighborCell in self.prevCells):
            neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        self.prevCells.append(neighborCell)
        self.model.grid.move_agent(self, neighborCell)
        self.mantainPrevCells()
        self.randomSteps += 1
    
    def distanceBetweenPoints(self, point1, point2):
        return math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))

    def getToDestination(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, False)
        if self.destination in neighbors: return
        bestPoint = None
        bestDistance = -1
        for neighbor in neighbors:
            if self.model.grid.is_cell_empty(neighbor) and (not neighbor in self.prevCells):
                distance = self.distanceBetweenPoints(self.destination, neighbor)
                if distance < bestDistance or bestDistance < 0:
                    bestDistance = distance
                    bestPoint = neighbor
        if (bestDistance < 0): 
            self.prevCells = [self.prevCells[-1]]
        else:
            self.destinationSteps += 1
            self.prevCells.append(bestPoint)
            self.stepsToDestination += 1
            self.model.grid.move_agent(self, bestPoint)

    def setDestination(self, destination):
        self.destination = destination

    def step(self):
        if not self.destination: 
            self.stepsToDestination = 0
            self.randomMove()
        else:
            if self.stepsToDestination == 0: self.prevCells = []
            self.getToDestination()
        return