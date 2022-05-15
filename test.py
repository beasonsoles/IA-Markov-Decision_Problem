"""We will check if any state (randomly chosen) can reach the goal state LLL"""
from main import MDP
import random

mdp = MDP("Data.csv", 3)
mdp.value_iteration()
initial_state = mdp.states[random.randint(0, len(mdp.states))]
final_state = "LLL"
state = initial_state
while state != final_state:
    probabilities = mdp.calculate_probabilities()
    curr_state_probabilities = probabilities.loc[state, :]
    next_state = curr_state_probabilities[random.randint(0, len(curr_state_probabilities))]
    print("")
