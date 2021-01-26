from z3 import *
import random
#  A   ->   B 
#  |^  <-   |^ 
#  ||       ||
#  v|  ->   v|
#  D   <-   C
#data = {'Andheri East': [{'Goregaon': ['8.5 km', '18 mins']}, {'Powai': ['6.1 km', '15 mins']}, {'Bandra': ['12.4 km', '25 mins']}], 'Goregaon': [{'Andheri East': ['7.0 km', '16 mins']}, {'Powai': ['10.3 km', '25 mins']}, {'Bandra': ['17.7 km', '30 mins']}], 'Powai': [{'Andheri East': ['6.1 km', '14 mins']}, {'Goregaon': ['11.6 km', '28 mins']}, {'Bandra': ['18.4 km', '39 mins']}], 'Bandra': [{'Andheri East': ['11.5 km', '24 mins']}, {'Goregaon': ['17.9 km', '31 mins']}, {'Powai': ['20.0 km', '39 mins']}]}

graph = {
    'a':{'b':12400,'d':6100},
    'b':{'c':17900,'a':11500},
    'c':{'d':10300,'b':17700},
    'd':{'a':6100,'c':11600}
}
# distances in meters

STATIONS = ['a','b','c','d']
TRACKS = [['a','b','c','d'],['d','c','b','a']]
TRAIN_CAP = 100
MU,SIG = 20,5
NUM_TRAINS = 2
MIN_WAIT = 200 #seconds
DEBOARDING_WAIT = 100 #seconds
MAX_SPEED = 8 #m/s
INTER_TRAIN_TIME = 30 #seconds

class Train:
    def __init__(self,train_id,track_no,capacity,graph=None):
        self.stations = TRACKS[track_no]
        self.track_no = track_no
        self.id = train_id
        self.starts = {
            track:Int(f'train{self.id}_track{track_no}_start_{track}')
                        for track in self.stations}
        self.ends = {
            track:Int(f'train{self.id}_track{track_no}_end_{track}')
                      for track in self.stations}
        #self.occupied = Int(f'{self.id}_{track_no}_occ')
        self.occupied = Function(
            f'train{self.id}_track{track_no}_occ',IntSort(),IntSort())
        self.pass_dest = {
            station: Function(
                f'train{self.id}_track{track_no}_dest_{station}',
                IntSort(),IntSort()) for station in self.stations
        }
    def __repr__(self):
        return f"Train: {self.id}; Track: {self.track_no}"

class Track:
    def __init__(self, track_no, num_trains):
        self.stations = TRACKS[track_no]
        self.num_trains = num_trains
        self.id = track_no
        self.trains = {
            (track_no,i):Train(i,track_no,TRAIN_CAP) 
            for i in range(num_trains)
        }
    def __repr__(self):
        return f"Track: {self.id}\nStations: {self.stations}\nTrains:\n{list(self.trains.values())}"

class Station:
    def __init__(self,station_id):
        self.stations_to = [i for i in STATIONS if i!=station_id ]
        self.id = station_id
        self.going_to = {
            station:lambda : int(abs(random.normalvariate(MU,SIG)))
            for station in self.stations_to
        }
        self.exiting = lambda : int(abs(random.normalvariate(NUM_TRAINS*MU,SIG)))
        self.num_people = {
            station:Function(
                f'station_{station_id}_to_{station}',IntSort(),IntSort()) 
            for station in self.stations_to
        }
        self.track_nos = [i for i,v in enumerate(TRACKS) if self.id in self.id ]
    def __repr__(self):
        return f"Station: {self.id}\nTracks:\n{self.track_nos}"

#t = Int('t')
stations = [Station(i) for i in STATIONS]
tracks = [Track(i,NUM_TRAINS) for i in range(len(TRACKS))]
constraints = []
for track in tracks:
    for (track_no,train_no),train in track.trains.items():
        for station in track.stations: #minimum wait time
            constraints.append(
                train.ends[station]-train.starts[station]>=MIN_WAIT
            )
        # it should begin positive
        constraints.append(train.starts[track.stations[0]]>=0)
        for s1,s2 in zip(track.stations,track.stations[1:]):
            # train leaving a station in track 
            # arrives later at the oter station on the track
            # by atleast max speed * distance
            constraints.append(
                train.starts[s2]-train.ends[s1]>=(graph[s1][s2])//MAX_SPEED
            )
        # train occupancy should be non-neg and should not exceed capacity
        # temporal property
        #constraints.append(train.occupied<=TRAIN_CAP)
        #constraints.append(train.occupied>=0)
    # next train starts atleast after first train leaves the station
    for train_no in range(track.num_trains-1):
        for station in track.stations:
            track_no = track.id
            constraints.append(
                track.trains[(track_no,train_no+1)].starts[station] > 
                track.trains[(track_no,train_no)].ends[station] + 
                INTER_TRAIN_TIME
            )
    for (track_no,train_no),train in track.trains.items():
        for station in track.stations:
            constraints.append(
                train.pass_dest[station](0)==0
            )

for station in stations:
    for dest in station.stations_to:
        constraints.append(
            station.num_people[dest](0)>=0
        )


for i in range(5,1000,5):
    for station in stations:
        for dest in station.stations_to:
            # people willing to go at each station as a function of
            # number of people entering and as a last time
            constraints.append(
                station.num_people[dest](i) == 
                station.num_people[dest](i-5) + station.going_to[dest]()
            )
        for track_no in station.track_nos:
            for (_,train_no),train in tracks[track_no].trains.items():
                constraints.append(
                    train.pass_dest[station.id](i) == If(And(
                        i>=train.starts[station.id],
                        i<train.starts[station.id]+DEBOARDING_WAIT),
                    0,
                    train.pass_dest[station.id](i-5)
                    )
                )

    for track in tracks:
        for (track_no,train_no),train in track.trains.items():
            for station in track.stations: #minimum wait time
                constraints.append(
                    train.ends[station]-train.starts[station]>=MIN_WAIT
                )

