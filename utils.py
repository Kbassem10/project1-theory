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