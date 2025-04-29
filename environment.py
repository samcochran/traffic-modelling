import numpy as np 
from matplotlib import pyplot as plt
plt.style.use('dark_background')


class StopSign:
    def __init__(self, lane, road):
        self.lane = lane 
        self.road = road
        if self.lane == 0 or self.lane == 2: self.loc = road.roadLen//2 - 2
        elif self.lane == 1 or self.lane == 3: self.loc = road.roadLen//2 + 2
        self.next = None
        self.prev = None
        self.isIntersection = True
        self.isObstacle = True

class Road:
    def __init__(self, roadLen):
        self.roadLen = roadLen
        self.occMap = np.zeros((roadLen, roadLen))
        self.stops = dict()
        for lane in range(4):
            self.stops[lane] = StopSign(lane, self)
        self.stopStack = []
        self.stopStackUpdated = 0
        self.laneLocs = {0:self.roadLen//2 - 1, 1:self.roadLen//2 + 1,
                         2:self.roadLen//2 + 1, 3:self.roadLen//2 - 1}

    def placeCar(self, lane, loc):
        if lane == 3:
            if self.occMap[self.laneLocs[3], loc] == 1: raise Exception(f'Collision in lane {lane} loc {loc}!')
            self.occMap[self.laneLocs[3], loc] = 1
        elif lane == 2:
            if self.occMap[self.laneLocs[2], loc] == 1: raise Exception(f'Collision in lane {lane} loc {loc}!')
            self.occMap[self.laneLocs[2], loc] = 1
        elif lane == 1:
            if self.occMap[loc, self.laneLocs[1]] == 1: raise Exception(f'Collision in lane {lane} loc {loc}!')
            self.occMap[loc, self.laneLocs[1]] = 1 
        elif lane == 0:
            if self.occMap[loc, self.laneLocs[0]] == 1: raise Exception(f'Collision in lane {lane} loc {loc}!')
            self.occMap[loc, self.laneLocs[0]] = 1

    def removeCar(self, lane, loc):
        if lane == 3:
            if self.occMap[self.laneLocs[3], loc] == 0: raise Exception('No car to remove!')
            self.occMap[self.laneLocs[3], loc] = 0
        elif lane == 2:
            if self.occMap[self.laneLocs[2], loc] == 0: raise Exception('No car to remove!')
            self.occMap[self.laneLocs[2], loc] = 0
        elif lane == 1:
            if self.occMap[loc, self.laneLocs[1]] == 0: raise Exception('No car to remove!')
            self.occMap[loc, self.laneLocs[1]] = 0 
        elif lane == 0:
            if self.occMap[loc, self.laneLocs[0]] == 0: raise Exception('No car to remove!')
            self.occMap[loc, self.laneLocs[0]] = 0

    def intersectionClear(self):
        centerClear = np.all(self.occMap[self.laneLocs[0]:self.laneLocs[1] + 1,
                             self.laneLocs[3]:self.laneLocs[2] + 1] == 0)
        clear0 = self.occMap[self.laneLocs[0], self.laneLocs[3] - 1] == 0 
        clear1 = self.occMap[self.laneLocs[1], self.laneLocs[2] + 1] == 0 
        clear2 = self.occMap[self.laneLocs[2], self.laneLocs[0] - 1] == 0 
        clear3 = self.occMap[self.laneLocs[3], self.laneLocs[1] + 1] == 0
        if centerClear and clear0 and clear1 and clear2 and clear3:
            return True
        return False
      
    def plotRoad(self):
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.plot([0, self.roadLen//2 - 1.5], [self.roadLen//2 - 1.5, self.roadLen//2 - 1.5], color='white')
        plt.plot([self.roadLen//2 + 2.5, self.roadLen], [self.roadLen//2 - 1.5, self.roadLen//2 - 1.5], color='white')
        plt.plot([0, self.roadLen//2 - 1.5], [self.roadLen//2 + 2.5, self.roadLen//2 + 2.5], color='white')
        plt.plot([self.roadLen//2 + 2.5, self.roadLen], [self.roadLen//2 + 2.5, self.roadLen//2 + 2.5], color='white')
        plt.plot([0, self.roadLen//2 - 1.5], [self.roadLen//2 + .5, self.roadLen//2 + .5], color='white', linestyle='--')
        plt.plot([self.roadLen//2 + 2.5, self.roadLen], [self.roadLen//2 + .5, self.roadLen//2 + .5], color='white', linestyle='--')
        plt.plot([self.roadLen//2 - 1.5, self.roadLen//2 - 1.5], [0, self.roadLen//2 - 1.5], color='white')
        plt.plot([self.roadLen//2 - 1.5, self.roadLen//2 - 1.5], [self.roadLen//2 + 2.5, self.roadLen], color='white')
        plt.plot([self.roadLen//2 + 2.5, self.roadLen//2 + 2.5], [0, self.roadLen//2 - 1.5], color='white')
        plt.plot([self.roadLen//2 + 2.5, self.roadLen//2 + 2.5], [self.roadLen//2 + 2.5, self.roadLen], color='white')
        plt.plot([self.roadLen//2 + .5, self.roadLen//2 + .5], [0, self.roadLen//2 - 1.5], color='white', linestyle='--')
        plt.plot([self.roadLen//2 + .5, self.roadLen//2 + .5], [self.roadLen//2 + 2.5, self.roadLen], color='white', linestyle='--')
        plt.xlim(0, self.roadLen)
        plt.ylim(0, self.roadLen)
        plt.gca().set_aspect('equal')
        


