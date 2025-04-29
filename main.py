import numpy as np 
from matplotlib import pyplot as plt
from vehicle import Car
from environment import Road
from animate import animate
from copy import deepcopy


global cars 
global road
def initialize(nCars, roadLen, leftProb, rightProb):
    global cars
    global road
    road = Road(roadLen)
    cars = dict()
    for lane in nCars.keys(): cars[lane] = []
    for lane in nCars.keys():
        for i in range(nCars[lane]):
            if lane == 1 or lane == 3: loc = road.roadLen - 1 - i#//4
            elif lane == 0 or lane == 2: loc = i#//4
            newCar = Car(lane=lane, loc=loc, nav=None, road=road, next=None, prev=None, leftProb=leftProb, rightProb=rightProb)
            cars[lane].append(newCar)
            road.placeCar(lane, loc)
            
    for lane in nCars.keys():
        for i in range(nCars[lane]):
            cars[lane][i].next = cars[lane][(i + 1)%nCars[lane]]
            cars[lane][i].prev = cars[lane][i - 1]
        if nCars[lane] > 0 and lane in road.stops.keys():
            cars[lane][0].prev = road.stops[lane]
            cars[lane][-1].next = road.stops[lane]
            road.stops[lane].next = cars[lane][0]
            road.stops[lane].prev = cars[lane][-1]

    cars = np.concatenate([cars[lane] for lane in nCars.keys()])

def update():
    global cars
    global road
    for car in cars:
        road.removeCar(car.lane, car.loc)
        car.update()
        road.placeCar(car.lane, car.loc)
    if road.stopStackUpdated > 0: road.stopStackUpdated -= 1 

def observe():
    global cars
    global road
    road.plotRoad()
    for car in cars:
        car.observe()

def runModel(leftProb, rightProb, burnIn=0, t=50):
    roadLen = 51
    nCars = {0:10, 1:10, 2:10, 3:10} #don't go over 20 cars per lane, I haven't added error handling for starting in the intersection
    # burnIn = 100
    # t = 150
    delay = .25
    drawFrames = True
    # fileName = 'directional_density_test_uneven'
    initialize(nCars, roadLen, leftProb, rightProb)
    snapshots = []
    if drawFrames: 
        plt.ion()
        fig = plt.figure(facecolor='k', figsize=(12, 12))
        observe()
    for i in range(t):
        if i >= burnIn:
            snapshots.append(deepcopy(cars))
            if drawFrames:
                observe()
                plt.draw()
                plt.pause(delay)
                plt.cla()
        update()
    if drawFrames:
        plt.ioff()
    snapshots.append(deepcopy(cars))

    meanSpeeds = []
    for car in cars:
        meanSpeeds.append(np.mean(car.history))
    return np.mean(meanSpeeds)

runModel(.2, .2)

# print('Making mp4')
# animate(road, snapshots, fileName, 'mp4', nSeconds=(t - burnIn)*delay, endPause=0)
# print('Making gif')
# animate(road, snapshots, fileName, 'gif', nSeconds=(t - burnIn)*delay)
# print('Done!')

# meanMeans = []
# labels = []
# for leftProb in [0, .1, .5, 1]:
#     for rightProb in [0, .1, .5, 1]:
#         if leftProb + rightProb > 1: continue
#         meanMean = runModel(leftProb, rightProb)
#         meanMeans.append(meanMean)
#         # print('leftProb:', leftProb, 'rightProb:', rightProb, 'meanMean:', meanMean)
#         label = f'Left Prob {leftProb}, Right Prob {rightProb}'
#         labels.append(label)
#
# print(meanMeans)
# plt.clf()
# plt.rcParams['font.size'] = 16
# plt.figure(figsize=(20, 12))
# plt.barh(list(range(len(meanMeans))), meanMeans, tick_label=labels)
# plt.show()
