# controller-synthesis

## Ideas
  - Constraint as classifier - I
  - Metric(decided by us) for reward shaping based on deviation from constraint to train RL Agent - I
  
  - Later stage
    - Build an automaton for constraints and use this for deriving metrics - II
    - 

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
