from classes import State
from utils import epsilon_closure, move, load_nfa, print_dfa

def main():
    # --- LOAD INPUT ---
    # Load the NFA configuration from your JSON file
    nfa_data = load_nfa("nfa.json , nfa_complex.json")  # Adjust the path as needed")
    if not nfa_data:
        return

    # Create State objects dynamically based on JSON 'states' and 'accepting_states'
    states = {name: State(name, name in nfa_data["accepting_states"]) 
              for name in nfa_data["states"]}
    
    # Map Alphabet Transitions from JSON
    for start_node, trans in nfa_data["transitions"].items():
        for char, targets in trans.items():
            states[start_node].transitions[char] = [states[t] for t in targets]
            
    # Map Epsilon Transitions from JSON
    for start_node, targets in nfa_data["epsilon_transitions"].items():
        states[start_node].epsilon_transitions = [states[t] for t in targets]

    # --- LOGIC TESTING (Optional) ---
    start_node = states[nfa_data["start_state"]]
    print(f"Testing Epsilon Closure of {start_node.name}:", epsilon_closure(start_node))

    # ---  FORMAT OUTPUT ---
    # Once  provides the final conversion result (dfa_dict), 
    # you display it using your professional table formatter.
    
    # Example placeholder of a converted DFA result:
    example_dfa_results = {("A", "a"): "B", ("A", "b"): "A", ("B", "a"): "B", ("B", "b"): "C"}
    
    # This fulfills the "Arrow/Asterisk" marking requirement
    print_dfa(example_dfa_results, nfa_data["alphabet"], "A", ["C"])

if __name__ == "__main__":
    main()