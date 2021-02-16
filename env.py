import gym
import ray
from ray.rllib.agents import ppo
import random
from gym.spaces import Discrete, Box, Tuple

class Station:
    def __init__(self, id,max_people):
        self.id = id
        self.max_people = max_people



# paths of each train (next_station,distance tuples)
# initialized by the topology of the railway network
PATHS = [[(0,10),(1,20),(2,20),(3,40)],[(0,10),(1,20),(2,20),(3,40)]] 

STATIONS = [Station(i) for i in range(4)]

def path(stationID, trainID):
    # return next_stationID, distance
    return PATHS[trainID][stationID+1] 

def sampler(stationID, trainID, max_people, occupancy):
    while True:
        transfer = int(abs(random.normalvariate(max_people/2,max_people/2)))
        if transer < max_people:
            break
    STATIONS[stationID].max_people = max_people - transfer
    return occupancy+transfer, max_people-transfer
    # return updated_occupancy, max_people
    raise NotImplementedError


def calcReward(stationID, trainID, occupancy, speed):
    # return reward
    raise NotImplementedError

class Controller(gym.Env):
    """
    Action space -> variables that can be controlled and here it is only speed
    Observation space -> (station_to, train_id, num_people_at station, occupancy, distance)
    
    """

    def __init__(self, path, train_id, num_stations=4, max_speed=100, max_people=500, max_distance=100):
        self.MAX_SPEED = max_speed
        self.MAX_PEOPLE = max_people
        self.MAX_DISTANCE = max_distance
        self.MAX_OCCUPANCY = 1
        self.TRAIN_ID = train_id
        self.DELTA_TIME = 10 #10ms
        self.action_space = Box(0,self.MAX_SPEED) 
        self.observation_space = Tuple(Discrete(num_stations),
                                       Discrete(self.MAX_PEOPLE), 
                                       Box(0,self.MAX_OCCUPANCY), 
                                       Box(0, self.MAX_DISTANCE))
        
        self.curr_state = (0,50,0,0)
        self.curr_station = 0

    def reset(self):
        self.curr_station = 0
        self.curr_state = (0,50,0,0) #stationid, num_people_at_station,train_occupancy,distance_from_next_station
        return self.curr_state

    def step(self, action):
        state = list(self.curr_state)
        if action == 0:
            if state[-1] == 0:
                # currently at a station
                next_station, distance = path(state[0], self.TRAIN_ID)
                occupancy, next_max_people = sampler(state[0], self.TRAIN_ID, state[1], state[2])
                next_state = [next_station, next_max_people, occupancy, distance]
            else:
                # Between two stations but no movement
                next_state = state
        else:
            if state[-1] == 0:
                #currently leaving the station
                next_state = state
            else:
                #Between two stations and moving
                next_state = [state[0], state[1], state[2], state[3]- self.DELTA_TIME*action]

        done = 0

        reward = calcReward(next_state[0], self.TRAIN_ID, next_state[2], action)

        return tuple(next_state), reward, done, {}