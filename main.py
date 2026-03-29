from classes import State
from utils import print_dfa, read_nfa_from_json, nfa_to_dfa

def main():
    start_node, alphabet, nfa_accepting_states = read_nfa_from_json("nfa_complex.json")
    if not start_node:
        return

    dfa_transitions, start_dfa_name, dfa_accepting_states = nfa_to_dfa(
        start_node, alphabet, nfa_accepting_states
    )

    print_dfa(dfa_transitions, alphabet, start_dfa_name, dfa_accepting_states)

if __name__ == "__main__":
    main()