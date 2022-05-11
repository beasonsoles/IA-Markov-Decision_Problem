"""Main module docstring"""
import pandas

# ------------- reset the size of the terminal -------------
pandas.options.display.max_columns = None

# ------------- variables -------------
df = pandas.read_csv("Data.csv", sep=";")
# these three constants can be changed by the user
NUMBER_OF_ROADS = 3
TRAFFIC_LEVELS = ["H", "L"]
ACTIONS = ["N", "E", "W"]
STATES = ["HHH", "HHL", "HLH", "HLL", "LHH", "LHL", "LLH", "LLL"]
# generate the states
# STATES = []
states_with_direction = {}
# probabilities will be a matrix that stores all the probabilities
probabilities = []

# ------------- functions -------------


def simplify_data(line):
    """Function that keeps the first letter of the characters in the entered row.
    Thus, we ease working with the data. It returns two strings: a string with the initial state
    and the action, and another string with the final state"""
    action_found = False
    initial_state_and_action = ""
    final_state = ""
    for column in line:
        # to make the program more general, we will use the boolean action_found to separate each line
        # in the two strings created above
        if not action_found:
            if column == "High":
                initial_state_and_action += "H"
            elif column == "Low":
                initial_state_and_action += "L"
            else:
                initial_state_and_action += "-" + column
                action_found = True
        else:
            if column == "High":
                final_state += "H"
            elif column == "Low":
                final_state += "L"
    return initial_state_and_action, final_state


def generate_states(l): # RECURSION FUNCTION FOR THE FOR LOOPS
    print("Finish this")
        # we fill the STATES list based on the constants NUMBER_OF_ROADS and TRAFFIC_LEVELS,
        # so that the program is more generic
        # for i in range(len(TRAFFIC_LEVELS) ^ NUMBER_OF_ROADS):
        #     # in this case, 2 traffic levels (H, L) to the power of 3 roads
        #     state = generate_states(STATES)
        #     for road in range(NUMBER_OF_ROADS):
        #         for level in TRAFFIC_LEVELS:
        #             state += level
        #     STATES.append(state)
        # print(STATES)


# loop to create the keys of the states_with_direction dictionary and assign it a counter of 0
# these keys will have the form: levellevellevel-action
for state in STATES:
    for action in ACTIONS:
        states_with_direction[state + "-" + action] = 0
# fill the probability matrix with 0
for row in range(len(states_with_direction)):
    probabilities.append([])
    for col in range(len(STATES)):
        probabilities[row].append(0)
# store the data and the states and direction in a list
data_list = df.to_numpy()
states_and_dir = list(states_with_direction.keys())
# calculate how many times each levellevellevel-action key appears in the data

for line in data_list:
    new_line = simplify_data(line)
    # the two following variables will store the initial state and action (e.g. HHL-E)
    # and the final state (e.g. HLH)
    i_state_and_action = new_line[0]
    f_state = new_line[1]
    for row in states_and_dir:
        if i_state_and_action == row:
            states_with_direction[row] += 1
        # calculate the frequency of each complete line
        for state in STATES:
            if i_state_and_action == row and f_state == state:
                probabilities[states_and_dir.index(row)][STATES.index(state)] += 1

# calculate the probabilities
for row in range(len(states_and_dir)):
    for column in range(len(STATES)):
        try:
            previous = probabilities[row][column]
            probability = previous / states_with_direction.get(states_and_dir[row])
            # probabilities[states_and_dir.index(row)][STATES.index(state)] = round(probability, 4)
            probabilities[row][column] = probability
        except ZeroDivisionError:
            probabilities[row][column] = 0
pct = pandas.DataFrame(probabilities, index=states_with_direction, columns=STATES)
print(pct)
