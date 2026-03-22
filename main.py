from classes import State
from utils import epsilon_closure

def main():
    #Create the States
    q0 = State("q0")
    q1 = State("q1")
    q2 = State("q2")
    q3 = State("q3")
    q4 = State("q4")
    q5 = State("q5")
    q6 = State("q6")
    q7 = State("q7")
    q8 = State("q8")
    q9 = State("q9", is_accepting=True) # The double circle in the diagram


    #Draw the Arrows (Transitions)

    #Standard Alphabet Transitions
    q0.transitions['a'] = [q1]   # q0 goes to q1 on 'a'
    q4.transitions['b'] = [q5]   # q4 goes to q5 on 'b'
    q6.transitions['c'] = [q7]   # q6 goes to q7 on 'c'

    #Epsilon Transitions 
    q1.epsilon_transitions.append(q2)

    q2.epsilon_transitions.append(q3)
    q2.epsilon_transitions.append(q9)

    q3.epsilon_transitions.append(q4)
    q3.epsilon_transitions.append(q6)

    q5.epsilon_transitions.append(q8)
    q7.epsilon_transitions.append(q8)

    q8.epsilon_transitions.append(q3)
    q8.epsilon_transitions.append(q9)

    #Test the Epsilon Closure Function
    print("Epsilon closure of q0:", epsilon_closure(q0))
    print("Epsilon closure of q2:", epsilon_closure(q2))
    print("Epsilon closure of q3:", epsilon_closure(q3))
    print("Epsilon closure of q5:", epsilon_closure(q5))
    print("Epsilon closure of q8:", epsilon_closure(q8))

if __name__ == "__main__":
    main()