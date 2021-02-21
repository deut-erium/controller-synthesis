class Station:
    def __init__(self, id,max_people=100,comm_radius=100):
        self.id = id
        self.max_people = max_people
        self.trains_approaching = {0:(10,100), 1:(50,50), 2:(70,70)} #train_id:distance,speed
        self.comm_radius = comm_radius

    def get_distance(self,train_id,dist,speed):
        if dist<self.comm_radius:
            self.trains_approaching[train_id]=(dist,speed)
        return self.trains_approaching