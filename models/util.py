import random
import numpy as np
from gym.spaces import Discrete, Box, Tuple
from models.station import Station

'''
## To-DO

**Visualizer to be made - vizualization

**sampler to be fixed 

**paths - parsing

SAMPLER:
sampling as a function of time,station which returns mu, sigma

'''

def path(stationID, trainID):
    # return next_stationID, distance
    # del STATIONS[stationID].trains_approaching[trainID]
    isLast = 0
    if stationID == len(PATHS[trainID])-1:
        isLast = 1
    return PATHS[trainID][stationID] , isLast

# paths of each train (next_station,distance tuples)
# initialized by the topology of the railway network
PATHS = [[(1,20),(2,20),(3,40), (4,10), (0,10)] for i in range(10)] # paths[i] -> path_of_train[i]
# paths[i][j=current station] = next station, distance

STATIONS = [Station(i) for i in range(5)]

## Outgoing from train to be modelled
def sampler(stationID, trainID, max_people, occupancy, train_capacity=100):
    MAX_PEOPLE = 500
    normv = lambda mu,sigma: int(abs(random.normalvariate(mu,sigma)))
    while True:
        outgoing = normv(train_capacity*occupancy/2, train_capacity*occupancy/2)
        if train_capacity*occupancy >= outgoing:
            occupancy -= outgoing/train_capacity
            break

    while True:
        incoming = normv((MAX_PEOPLE-max_people)/2,(MAX_PEOPLE-max_people)/2)
        transfer = normv(max_people/2,max_people/2)
        if transfer < max_people and transfer < 100*(1-occupancy) and max_people -transfer+incoming < MAX_PEOPLE:
            break
    STATIONS[stationID].max_people = max_people - transfer + incoming
    return occupancy+transfer/100, max_people - transfer + incoming
    # return updated_occupancy, max_people

def calcTime(own_speed, own_dist):
    MAX_VAL = 10**6
    if own_speed == 0:
        own_time = 0 if own_dist==0 else MAX_VAL
    else:
        own_time = own_dist/own_speed
    return own_time

def calcReward(stationID, trainID, occupancy, speed,dist):
    # later calculated and generated using the automata
    # f(speed,dist, num_trains_approaching, occupancy
    MAX_VAL = 10**6
    status = STATIONS[stationID].get_distance(trainID,dist,speed)
    own_dist, own_speed = status[trainID]
    own_time = calcTime(own_speed, own_dist)

    reward = 0
    for ID in status.keys():
        dist, speed = status[ID]
        time = calcTime(speed, dist)
        if time > own_time:
            reward += 1

    return reward