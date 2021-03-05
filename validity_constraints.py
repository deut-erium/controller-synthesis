## minimum waiting time at each station
## distance between the trains at a given time
## train1 and train2 have time difference atleast delta
## should not be more than n trains waiting at a given time on a station
## maximum waiting time on a station limited
## less acceleration/less speed closer to the station

## log_format
# train_id
# reward
## [next station, number of people on upcoming station, occupancy of train, distance from the station ]
from z3 import *
import re
NUM_TRAINS = 5
np_array_replace = re.compile('array\(\[(.*)\].*\)')
make_ar = lambda x:re.sub(np_array_replace,r'\1',x)

f = open('log_1.txt','r')
raw_data = [f.readline() for _ in range(NUM_TRAINS*3)]
data = []
while raw_data[0]:
    raw_data = [eval(i) for i in raw_data]
    data.append(raw_data)
    raw_data = [make_ar(f.readline().strip()) for _ in range(NUM_TRAINS*3)]

time_data = []
for t in range(len(data)):
    filtered_data = []
    for i in range(NUM_TRAINS):
        train_data = data[t][3*i:3*i+3]
        filtered_data.append( 
            [train_data[0],train_data[2][0],train_data[2][-1]] 
        )
        # train_id, next_station, distance from station
    time_data.append(filtered_data)
    


PATHS = [[(1,20),(2,20),(3,40), (4,10), (0,10)] for i in range(5)] # paths[i] -> path_of_train[i]

MIN_WAIT = 20
MIN_TRAIN_DIFF = 60

class Train:
    def __init__(self, train_id):
        self.id = train_id
        self.enters = {
            station: Int(f'train{self.id}_station_{station}_enter') 
            for station,dist in PATHS[self.id]
        }
        self.exits = {
            station: Int(f'train{self.id}_station_{station}_exit') 
            for station,dist in PATHS[self.id]
        }

trains = [Train(i) for i in range(len(PATHS))]
stations = list(range(5))

constraints = []
for train in trains:
    for station in stations:
        constraints.append(
            train.exits[station]-train.enters[station]>=MIN_WAIT
        )

for station in stations:
    for t1,t2 in zip(trains,trains[1:]):
        constraints.append(
            t1.enters[station]-t2.exits[station]>=MIN_TRAIN_DIFF
        )


