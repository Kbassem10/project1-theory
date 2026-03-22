def epsilon_closure(state):
    '''This function gets a state and returns the epsilon closure of that state.'''
    closure = set() #defining the set of closure to avoid duplicates
    stack = [state] #defining the stack to keep track of the states we need to explore

    while stack:
        current_state = stack.pop()
        closure.add(current_state)

        #Loop on all of the epsilon_transitions of the current state and add it to the stack
        #if not already in the closure (the set)
        for next_state in current_state.epsilon_transitions:
            if next_state not in closure:
                stack.append(next_state)
                closure.add(next_state)
    return closure

def move(states, symbol):
    '''
        This function gets a set of states and a symbol,
        and returns the set of states that can be reached
        from (including the epsilon transitions) 
        any of those states on that symbol.
    '''

    result = set() #defining the set of result to avoid duplicates

    '''
        loop over the states on the input set and check if there
        is a transition on the input symbol, if there is, add the
        next state to the result set
    '''
    for state in states:
        if symbol in state.transitions:
            for next_state in state.transitions[symbol]:
                result.add(next_state)
    
    #loop over the result set and add the epsilon closure of each state to the result set
    for item in list(result):
        result.update(epsilon_closure(item))

    return result