import gym
import ray
from ray.rllib.agents import ppo
import random
import numpy as np
from gym.spaces import Discrete, Box, Tuple
from models.station import Station
from models.util import path, sampler, calcReward

'''
## To-DO

**Visualizer to be made - vizualization

**RL env to parallelize

##acceleration is has limits not speed... change the model accordingly
action should be acceleration and speed should be kept track off

'''
class Controller(gym.Env):
    """
    Action space -> variables that can be controlled and here it is only speed
    Observation space -> (station_to, train_id, num_people_at station, occupancy, distance)    
    """

    def __init__(self, train_id=0, num_stations=4, 
                    max_acceleration=100, max_speed=100, 
                    max_people=500, max_distance=100, initial_state= [1,50,0,0]):
        self.MAX_SPEED = max_speed
        self.MAX_ACC = max_acceleration
        self.MAX_PEOPLE = max_people
        self.MAX_DISTANCE = max_distance
        self.MAX_OCCUPANCY = 1
        self.TRAIN_ID = train_id
        self.DELTA_TIME = 0.1 #10ms
        self.INITIAL_STATE = initial_state
        self.action_space = Box(0,self.MAX_SPEED, shape=(1,)) 
        self.observation_space = Box(low=np.array([0, 0, 0, 0]), 
                                    high=np.array([5, self.MAX_PEOPLE, self.MAX_OCCUPANCY, self.MAX_DISTANCE]), 
                                    dtype=np.float64)
        
        self.curr_state = np.array(self.INITIAL_STATE, dtype=np.float64)
        self.curr_station = 1
        self.prev_action = 0

    def reset(self):
        self.curr_station = 1
        self.curr_state = np.array(self.INITIAL_STATE, dtype=np.float64) #stationid, num_people_at_station,train_occupancy,distance_from_next_station
        return self.curr_state

    def step(self, action):
        if abs(action - self.prev_action) > self.MAX_ACC * self.DELTA_TIME:
            if self.prev_action > action:
                action = self.prev_action - self.MAX_ACC * self.DELTA_TIME
            else:
                action = self.prev_action + self.MAX_ACC * self.DELTA_TIME

        self.prev_action = action
        state = list(self.curr_state)
        #print(f"{action=}")
        done = 0
        # action is current speed
        if action == 0:
            # distance from current station = state[-1]
            if state[-1] == 0:
                # currently at a station
                (next_station, distance), done = path(int(state[0]), self.TRAIN_ID)
                occupancy, next_max_people = sampler(int(state[0]), self.TRAIN_ID, state[1], state[2])
                next_state = [next_station, next_max_people, occupancy, distance]
            else:
                # Between two stations but no movement
                next_state = state
        else:
            if state[-1] == 0:
                #currently leaving the station
                (next_station, distance), done = path(int(state[0]), self.TRAIN_ID)
                occupancy, next_max_people = sampler(int(state[0]), self.TRAIN_ID, state[1], state[2])
                next_state = [next_station, next_max_people, occupancy, distance]
            else:
                #Between two stations and moving
                updated_distance = state[3]- self.DELTA_TIME*action[0]

                if updated_distance > 0:
                    next_state = [state[0], state[1], state[2], updated_distance]
                else:
                    next_state = [state[0], state[1], state[2], 0]

        trains_approaching = STATIONS[next_state[0]].get_distance(self.TRAIN_ID, action, next_state[3])
        
        rew = calcReward(int(next_state[0]), self.TRAIN_ID, next_state[2], action,next_state[1])
        self.curr_state = tuple(next_state)
        #print(f"{rew=},{next_state=}")
        return np.array(self.curr_state, dtype=np.float64), rew, done, {}

if __name__ == "__main__":
    env = [Controller(train_id=i) for i in range(10)]

    for i in range(100):
        for j in range(10):
            # print(f"----------------- train ID={j}")
            env[j].reset()
            env[j].step(env[j].action_space.sample()) # take a random action
            env[j].close()