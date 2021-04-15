class Clocks:
    def __init__(self, num_clocks):
        self.num_clocks = num_clocks
        self.clocks = {}
        for ind in range(num_clocks):
            self.clocks[ind] = 0
        return
    
    def increment(self, resets=[]):
        for ind in range(self.num_clocks):
            if ind in resets:
                self.clocks[ind] = 0
            else:
                self.clocks[ind] += 1
        return
    
    def gettime(self, index):
        return self.clocks[index]
