from ta import TA



if __name__ == "__main__":
    states = ["start", "loop", "end"]
    input_symbols = ["a"]
    num_clocks = 2
    transitions = {("start", "a"): 
                   [{1: lambda x: 1 if (x<=20 and x>=10) else 0}, [0,1], "loop"],
                   ("loop", "a"): 
                   [{1:lambda x: 1 if (x<=50 and x>=40) else 0}, [0,1], "end"],
                   ("end", "a"): 
                   [{1:lambda x: 1 if (x>=10) else 0}, [1], "start"]
                  }
    initial_state = ["start"]
    final_states = ["start"]

    ta = TA(states,input_symbols, num_clocks, transitions, initial_state, final_states)

    ta.accepts_inputs("aaa")
    ta.accepts_inputs("aa")
