"""We will check if any state (randomly chosen) can reach the goal state LLL"""
from main import MDP
import random

mdp = MDP("Data.csv", 3)
mdp.value_iteration()
# we create a random initial state
initial_state = mdp.states[random.randint(0, len(mdp.states)-1)]
# we will try to reach the final state
final_state = "LLL"
curr_state = initial_state
random_index = 0
while curr_state != final_state:
    action = mdp.optimal_policy[curr_state]
    # we obtain a random state that can be reached from the initial state
    curr_state_probability = 0
    while curr_state_probability == 0:
        random_index = random.randint(0, len(mdp.states)-1)
        curr_state_probability = mdp.pct.loc[curr_state+"-"+action, mdp.states[random_index]]
    next_state = mdp.states[random_index]
    print("%s goes to %s with action %s" % (curr_state, next_state, action))
    curr_state = next_state
print("Test OK")
