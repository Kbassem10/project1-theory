class State:
    def __init__(self, name, is_accepting=False):
        self.name = name
        self.is_accepting = is_accepting
        
        #A dictionary for standard alphabet transitions (e.g., 'a', 'b')
        #Format: {'a': [State2, State3], 'b': [State1]}
        self.transitions = {} 
        
        #A specific list just for epsilon transitions
        #Format: [State4, State5]
        self.epsilon_transitions = [] 
        
    def __repr__(self):
        #this just makes it look nice if you print a State object to the terminal
        #Not necessary
        return f"State({self.name})"