import numpy as np 
from matplotlib import pyplot as plt


class Car:
    def __init__(self, lane, loc, nav, road, next, prev, leftProb=0, rightProb=0, historyLen=50):
        if leftProb + rightProb > 1: raise Exception('Invalid probabilities!')
        self.lane = lane
        self.loc = loc 
        self.nav = nav 
        self.road = road
        self.next = next 
        self.prev = prev
        self.speed = 0
        self.history = [self.speed]
        self.historyLen = historyLen
        self.speedLim = 3
        self.stoppingDist = {3:6, 2:4, 1:1}
        self.isIntersection = False
        self.turning = False
        self.leftTurnLanes = {0:2, 1:3, 2:1, 3:0}
        self.rightTurnLanes = {0:3, 1:2, 2:0, 3:1}
        self.leftProb = leftProb
        self.rightProb = rightProb
        if self.nav is None:
            self.randomizeNav()

    def randomizeNav(self):
        draw = np.random.uniform(0, 1)
        if draw < self.leftProb: self.nav = 'left'
        elif draw < self.leftProb + self.rightProb: self.nav = 'right'
        else: self.nav = 'straight'
        self.turning = False

    def continueStraight(self):
        if self.lane == 0 or self.lane == 2:
            self.loc = (self.loc + self.speed)%self.road.roadLen
        elif self.lane == 1 or self.lane == 3:
            self.loc = (self.loc - self.speed)%self.road.roadLen
    
    def executeTurn(self):
        if self.nav == 'right':
            if self.loc == self.road.laneLocs[self.rightTurnLanes[self.lane]]:
                self.speed += 1
                self.next.prev = self.road.stops[self.lane]
                self.road.stops[self.lane].next = self.next 
                self.loc = self.road.laneLocs[self.lane]
                self.lane = self.rightTurnLanes[self.lane] 
                self.next = self.road.stops[self.lane].next 
                self.next.prev = self 
                self.road.stops[self.lane].next = self 
                self.prev = self.road.stops[self.lane]
                self.turning = False
        elif self.nav == 'left':
            if self.loc == self.road.laneLocs[self.leftTurnLanes[self.lane]]:
                self.speed += 1
                self.next.prev = self.road.stops[self.lane]
                self.road.stops[self.lane].next = self.next 
                self.loc = self.road.laneLocs[self.lane]
                self.lane = self.leftTurnLanes[self.lane] 
                self.next = self.road.stops[self.lane].next 
                self.next.prev = self 
                self.road.stops[self.lane].next = self 
                self.prev = self.road.stops[self.lane]
                self.turning = False
        else: raise Exception('Turning error!')
        self.continueStraight()

    def update(self):
        # randomize nav upon entering from edge of screen
        if self.lane == 0 or self.lane == 2: 
            if self.loc >= self.road.roadLen - 3: self.randomizeNav()
        elif self.lane == 1 or self.lane == 2:
            if self.loc <= 3: self.randomizeNav()

        # update position
        if self.speed > 0:
            if self.turning:
                self.executeTurn() 
            else:
                self.continueStraight()
        self.history.append(self.speed)
        if len(self.history) > self.historyLen: self.history.pop(0)

        # find distance to next obstacle
        if self.lane == 0 or self.lane == 2:
            spaceAhead = (self.next.loc - self.loc)%self.road.roadLen
        elif self.lane == 1 or self.lane == 3:
            spaceAhead = (self.loc - self.next.loc)%self.road.roadLen

        # accelerate from stop
        if self.speed == 0:
            if spaceAhead > 1: 
                self.speed += 1
            elif spaceAhead == 1 and self.next.isIntersection:
                if self.nav != 'straight': self.turning = True
                if self.lane not in self.road.stopStack:
                    self.road.stopStack.append(self.lane)
                # if (np.all(np.array(self.history[-3:]) == 0)  
                if (self.road.stopStack[0] == self.lane 
                    and self.road.stopStackUpdated == 0
                    and self.road.intersectionClear()):
                    self.speed += 1
                    self.road.stopStack.pop(0)
                    if self.nav == 'straight': self.road.stopStackUpdated = 3
                    if self.nav == 'left': self.road.stopStackUpdated = 6
                    if self.nav == 'right': self.road.stopStackUpdated = 3
                    self.next = self.road.stops[self.lane].next
                    self.next.prev = self
                    self.road.stops[self.lane].next = self 
                    self.road.stops[self.lane].prev = self.prev 
                    self.prev.next = self.road.stops[self.lane]
                    self.prev = self.road.stops[self.lane]

        # accelerate if there is enough empty space ahead
        elif not self.turning and spaceAhead > (self.stoppingDist[self.speed] 
                + self.stoppingDist[min(self.speedLim, self.speed + 1)]):
            self.speed = min(self.speedLim, self.speed + 1)

        # decelerate if an obstacle is ahead
        elif not self.turning and spaceAhead <= self.stoppingDist[self.speed]:
            self.speed = max(0, self.speed - 1)

    def observe(self):
        if self.nav == 'straight': color = 'white'
        elif self.nav == 'left': color = 'steelblue'
        elif self.nav == 'right': color = 'sandybrown'
        # color = 'w'
        if self.lane == 0 or self.lane == 1:
            plt.scatter(self.road.laneLocs[self.lane] + .5, self.road.roadLen - self.loc - .5, marker='D', color=color)
        elif self.lane == 2 or self.lane == 3:
            plt.scatter(self.loc + .5, self.road.roadLen - self.road.laneLocs[self.lane] - .5, marker='D', color=color)

