import json
from classes import State

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

def read_nfa_from_json(filename):
    '''
        This function reads the NFA definition from a JSON file
        and constructs the corresponding State objects.
    '''

    with open(filename, 'r') as f:
        nfa_data = json.load(f)

    states = {}
    
    # Extract the necessary dictionary components from JSON once
    transitions_data = nfa_data.get("transitions", {})
    epsilon_data = nfa_data.get("epsilon_transitions", {})
    accepting_states = set(nfa_data.get("accepting_states", []))
    
    # Single loop over all states
    for name in nfa_data.get("states", []):
        is_accepting = name in accepting_states
        state_obj = State(name, is_accepting)
        
        # We need to map string targets to string names temporarily
        # until all State objects are created. Setting simple dicts/lists for now:
        state_obj.transitions = transitions_data.get(name, {})
        state_obj.epsilon_transitions = epsilon_data.get(name, [])
        
        states[name] = state_obj

    # Second quick pass to resolve all strings into object
    #  references to avoid issues with forward references
    for state in states.values():
        
        # Resolve normal alphabet transitions
        new_transitions = {}
        for char, target_names in state.transitions.items():
            new_transitions[char] = [states[t] for t in target_names]
        state.transitions = new_transitions
        
        # Resolve epsilon transitions
        state.epsilon_transitions = [states[t] for t in state.epsilon_transitions]

    start_node = states[nfa_data["start_state"]]
    return start_node, nfa_data["alphabet"], list(accepting_states)

def get_dfa_state_name(state_set, names_dict):
    """
    Helper function to assign a unique letter (A, B, C...) 
    to each new set of NFA states we discover.
    """
    if state_set not in names_dict:
        # 'A' is 65 in ascii. The size of the dictionary tells us how many letters we've used.
        next_letter = chr(ord('A') + len(names_dict))
        names_dict[state_set] = next_letter
        
    return names_dict[state_set]

def nfa_to_dfa(start_node, alphabet, nfa_accepting_states):
    
    #The starting DFA state is the epsilon closure of the starting NFA state.
    start_closure = frozenset(epsilon_closure(start_node))

    # Keep track of mappings between sets of NFA states and their single letter name (A, B, C...)
    dfa_state_names = {}
    
    # Define our first DFA state
    start_dfa_name = get_dfa_state_name(start_closure, dfa_state_names)

    #Lists/Sets used to process DFA states algorithmically
    unprocessed_states = [start_closure]
    seen_dfa_states = {start_closure}

    # Tracking final results
    dfa_transitions = {}
    dfa_accepting_states = set()

    # 3. Main Loop
    while unprocessed_states:
        # Take the next DFA state to process
        current_dfa_state_set = unprocessed_states.pop(0)
        current_name = get_dfa_state_name(current_dfa_state_set, dfa_state_names)
        
        #Check if this DFA state is an accepting state
        #A DFA state is accepting if ANY of its interior NFA states were accepting
        for state in current_dfa_state_set:
            if state.name in nfa_accepting_states:
                dfa_accepting_states.add(current_name)
                break

        #Evaluate NFA transitions for each symbol in our alphabet ('a', 'b')
        for symbol in alphabet:
            
            # Find out where this whole block of states travels to next using the 'move' function
            next_state_set = frozenset(move(current_dfa_state_set, symbol))
            
            # If the transition leads nowhere, skip mapping it.
            if not next_state_set:
                continue

            # If we discovered a new group of states we haven't seen before, add it to our lists
            if next_state_set not in seen_dfa_states:
                seen_dfa_states.add(next_state_set)
                unprocessed_states.append(next_state_set)
                
            # Finally, record this valid transition into our dictionary map
            next_name = get_dfa_state_name(next_state_set, dfa_state_names)
            dfa_transitions[(current_name, symbol)] = next_name

    return dfa_transitions, start_dfa_name, list(dfa_accepting_states)

def print_dfa(dfa_dict, alphabet, start_state, accepting_states):
    print("--- DFA TRANSTIONS TABLE ---")
    print(f"{'State':<10} | " + " | ".join(f"{sym:<5}" for sym in alphabet))
    print("-" * (15 + 8 * len(alphabet)))

    states = set(state for (state, _) in dfa_dict.keys())
    states.update(dfa_dict.values())
    states.add(start_state)
    for state in sorted(states):
        prefix = ""
        if state == start_state:
            prefix += "->"
        if state in accepting_states:
            prefix += "*"
            
        state_display = f"{prefix}{state}"

        row = [f"{state_display:<10}"]
        for sym in alphabet:
            target = dfa_dict.get((state, sym), "-")
            row.append(f"{target:<5}")
        print(" | ".join(row))
    print("-" * (15 + 8 * len(alphabet)))