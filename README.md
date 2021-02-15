# controller-synthesis

## Ideas
  - Constraint as classifier - I
  - Metric(decided by us) for reward shaping based on deviation from constraint to train RL Agent - I
  
  - Later stage
    - Build an automaton for constraints and use this for deriving metrics - II
    - 

## Models

- Model 1

  Cases:
  1. Train is in radius of station
  2. Train is at station
  3. Train is inbetween stations

  ### Train
  - Case 2 per time delta produce actions, num people in station, train capacity(intrinsic) - Reward function
  - Case 1 speed, and information from station (num people in station) - Reward function
  - Case 3 speed, distance from the upcoming station

  - Action space -> speed, information from station(num_people, num_trains arriving to the station),

  - Observation space -> num people in the train, train capacity, information of the station it is going towards

  - Transition Function -> path that should be followed by the trains + change in speed

  - Input: 
  - Output: Speed

## To-Do
  - Modelling (By Sunday Evening)
    - Train Identifier
    - Station Identifier (Track + people)
    - Action (time)
    - Transition function (fixed)
    - Reward function (Just occupancy at the start and shape it on the fly)
    - gamma factor (1 for now)
  
  - Metric 
    - distance metric (for now, and check rest, what works)
  
  - RL model (By Saturday evening)
    - RLlib basic framework
  
  - Constraints (By Saturday evening)
    - Representation
    - Metrics



