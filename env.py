import gym
import ray
from ray.rllib.agents import ppo

from gym.spaces import Discrete, Box, Tuple

def path(stationID, trainID):
    # return next_stationID, distance
    raise NotImplementedError

def sampler(stationID, trainID, max_people, occupancy):
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
        self.curr_state = (0,50,0,0)
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