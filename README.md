# NFA to DFA Converter

This project implements the **Subset Construction Algorithm** to convert a Nondeterministic Finite Automaton (NFA) with $\epsilon$-transitions (epsilon transitions) into a Deterministic Finite Automaton (DFA).

## 🗂️ Project Structure
* `main.py`: The main entry point of the script.
* `classes.py`: Contains the `State` data structure used to build the graph.
* `utils.py`: Contains all the functional logic (closures, moving, parsing, conversion, printing).
* `nfa.json` / `nfa_complex.json`: The NFA definitions using JSON format.

---

## 🏗️ Data Structures

### The `State` Class (`classes.py`)
Because an NFA is essentially a directed graph, we represent each state as a node (an object).
* **`name`**: The string identifier (e.g., `"q0"`).
* **`is_accepting`**: A boolean marking if the machine accepts a string when stopping on this state.
* **`transitions`**: A dictionary mapping an alphabet character to a list of target `State` objects. (NFA allows multiple targets for one character).
* **`epsilon_transitions`**: A list of `State` objects that can be reached without consuming any input.

---

## ⚙️ Core Functions (`utils.py`)

### 1. `read_nfa_from_json(filename)`
* **What it does:** Reads the NFA structure from the specified JSON file and constructs the Python objects.
* **Why we need it:** We need to convert plain text JSON files into an actual connected graph of `State` objects in memory.
* **How it works:** It does this in two passes:
  1. *First Pass:* Creates an isolated `State` object for every state in the JSON and flags if it's an accepting state.
  2. *Second Pass:* Iterates through the states again, replacing the string target names in `transitions` and `epsilon_transitions` with actual memory references to the `State` objects created in step 1.

### 2. `epsilon_closure(state)`
* **What it does:** Finds all NFA states that can be reached from a given state *without consuming any input characters* (using $\epsilon$-transitions).
* **Why we need it:** In an $\epsilon$-NFA, being in state `q0` means you are potentially also natively in any state connected to `q0` via an epsilon transition. We must group these together to evaluate the "true" current state.
* **How it works:** It uses a Depth First Search (DFS) algorithm with a `stack`. It pops a state, adds its epsilon targets to the stack, and marks them as visited (in a `set`) to prevent infinite looping. It returns a combined group (`set`) of all reachable states.

### 3. `move(states, symbol)`
* **What it does:** Given a *set* of current NFA states and an input symbol (e.g., `'a'`), it finds all possible next states.
* **Why we need it:** To figure out where our DFA goes when it reads a character.
* **How it works:** 
  1. It iterates through all current NFA tracking states.
  2. If the state has a transition for the `symbol`, it gathers the target states.
  3. After finding all direct target states, it computes the **`epsilon_closure`** for each of them to find any "free rides" the machine takes after making the standard transition.

### 4. `nfa_to_dfa(start_node, alphabet, nfa_accepting_states)`
* **What it does:** The main conversion engine (Subset Construction Algorithm). It converts the NFA into a DFA format.
* **Why we need it:** NFAs are great for theoretical design but hard for computers to strictly evaluate efficiently. DFAs are strictly deterministic (one state goes to exactly one other state per character).
* **How it works:**
  1. Calculate the `epsilon_closure` of the starting NFA state. This set of NFA states becomes the **first single DFA state** (named `A`).
  2. Put this new DFA state into an `unprocessed_states` queue.
  3. Loop while there are unprocessed DFA states:
     - Pop a DFA state. Determine if it is "accepting" (if it contains *any* NFA state that was accepting).
     - For every symbol in the alphabet, use `move()` to see what group of NFA states results.
     - Group these result states into a new DFA state (e.g., `B`). If `B` has never been seen before, add it to `unprocessed_states`.
     - Record the valid transition mapping.
  4. Yields a dictionary mapping `(DFA_State, Symbol) -> Next_DFA_State`.

### 5. `get_dfa_state_name(state_set, names_dict)`
* **What it does:** Simple helper to give clean string names to Sets of NFA states.
* **Why we need it:** Printing `Transitions for {q0, q1, q2}` is ugly. We want to convert `{q0, q1, q2}` to simply `"A"`, `{q2, q3}` to `"B"`, etc.
* **How it works:** It keeps a dictionary `names_dict` mapping the `frozenset` of states to a letter. It generates letters dynamically using ASCII mapping (`ord('A') + length`).

### 6. `print_dfa(...)`
* **What it does:** Neatly dynamically formats the output transition dictionary to the terminal.
* **Why we need it:** It highlights the starting state with `->` and accepting states with `*` providing a professional mathematical transition table.

---

## 🚀 How to Run
Ensure you have Python installed, then run the primary entry point from your terminal:
```bash
python3 main.py
```
This will parse `nfa.json`, compute the $\epsilon$-closures, calculate the subsets, and output the exact DFA transition table to the terminal.
 
