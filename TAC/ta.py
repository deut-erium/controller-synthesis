from clock import Clocks

class TA:
    def __init__(self, states, input_symbols, num_clocks, transitions, initial_state, final_states) :
        self.states = states
        self.num_clocks = num_clocks
        self.input_symbols = input_symbols
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.clocks = Clocks(num_clocks)

    def get_next_state(self, state, symbol):
        [clock_constraints, resets, next_state] = self.transitions[(state, symbol)]
        while True:
            check = []
            for clock, constraint in clock_constraints.items():
                # print(f"{self.clocks.gettime(clock)=}")
                check.append(constraint(self.clocks.gettime(clock)))
                # print(check)

            if all(check):
                for ind in range(self.num_clocks):
                    print(f"clock = {ind} : time ={self.clocks.gettime(ind)} state= {next_state}")
                self.clocks.increment(resets)
                return next_state
            
            else:
                self.clocks.increment()
                    # for ind in range(self.num_clocks):
                    #     print(f"clock = {ind} : time ={self.clocks.gettime(ind)} state= {next_state}")
        
    def accepts_inputs(self, timed_word):
        curr_state = self.initial_state[0]
        for letter in timed_word:
            next_state = self.get_next_state(curr_state, letter)
            curr_state = next_state
        
        if curr_state in self.final_states:
            print("accepted")
        else:
            print("rejected")        



