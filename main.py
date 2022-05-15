"""Main module docstring"""
import pandas

# ------------- reset the size of the terminal -------------
pandas.options.display.max_columns = None


class MDP:

    def __init__(self, input_file, levels_num):
        # ------------- variables -------------
        self.df = pandas.read_csv(input_file, sep=";")
        # convert the dataframe with our data to a list
        self.data_list = self.df.to_numpy()
        self.levels_num = levels_num
        # these three constants can be changed by the user
        # self.ACTIONS = ["E", "N", "W"]
        self.ACTIONS = []
        self.STATES = []
        # self.STATES = ["HHH", "HHL", "HLH", "HLL", "LHH", "LHL", "LLH", "LLL"]
        self.GOAL = ["LLL"]
        self.states_with_direction = {}
        # probabilities will be a matrix that stores all the probabilities
        self.probabilities = []
        self.prev_action = {}

    # ------------- methods -------------
    def simplify_data(self, line):
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

    def generate_states(self):
        df_unique = self.df.drop_duplicates()
        unique_lines = df_unique.to_numpy()
        for line in unique_lines:
            state_and_dir, final_state = self.simplify_data(line)
            result = state_and_dir.split("-")
            state = result[0]
            action = result[1]
            if final_state not in self.STATES:
                self.STATES.append(final_state)
            if state not in self.STATES:
                self.STATES.append(state)
            if action not in self.ACTIONS:
                self.ACTIONS.append(action)
        self.STATES.sort()
        self.ACTIONS.sort()

    # loop to create the keys of the states_with_direction dictionary and assign it a counter of 0
    # these keys will have the form: levellevellevel-action
    def create_states_with_direction(self):
        for state in self.STATES:
            for action in self.ACTIONS:
                self.states_with_direction[state + "-" + action] = 0
        # fill the probability matrix with 0
        for row in range(len(self.states_with_direction)):
            self.probabilities.append([])
            for col in range(len(self.STATES)):
                self.probabilities[row].append(0)
        # store the states and direction in a list
        states_and_dir = list(self.states_with_direction.keys())
        return states_and_dir

    def count_occurrences(self):
        # calculate how many times each levellevellevel-action key appears in the data
        states_and_dir = self.create_states_with_direction()
        for line in self.data_list:
            new_line = self.simplify_data(line)
            # the two following variables will store the initial state and action (e.g. HHL-E)
            # and the final state (e.g. HLH)
            i_state_and_action = new_line[0]
            f_state = new_line[1]
            for row in states_and_dir:
                if i_state_and_action == row:
                    self.states_with_direction[row] += 1
                # calculate the frequency of each complete line
                for state in self.STATES:
                    if i_state_and_action == row and f_state == state:
                        self.probabilities[states_and_dir.index(row)][self.STATES.index(state)] += 1
        return states_and_dir

    def calculate_probabilities(self):
        # calculate the probabilities
        states_and_dir = self.count_occurrences()
        for row in range(len(states_and_dir)):
            for column in range(len(self.STATES)):
                try:
                    previous = self.probabilities[row][column]
                    probability = previous / self.states_with_direction.get(states_and_dir[row])
                    self.probabilities[row][column] = probability
                except ZeroDivisionError:
                    self.probabilities[row][column] = 0
        pct = pandas.DataFrame(self.probabilities, index=states_and_dir, columns=self.STATES)
        return pct

    def cost(self, state, n_action):
        try:
            if n_action == self.prev_action[state]:
                return 1
            elif n_action != self.prev_action[state]:
                return 2
        except KeyError:
            return 1

    def bellman_equation(self, init_state, action, old_values, pct):
        if init_state in self.GOAL:
            return 0
        value = self.cost(init_state, action)
        for next_state in self.STATES:
            state = init_state + "-" + action
            value += pct.loc[state, next_state] * old_values[next_state]
        return value

    def value_iteration(self):
        self.generate_states()
        pct = self.calculate_probabilities()
        values = {state: 0 for state in self.STATES}
        old_values = {}
        while old_values != values:
            old_values = values.copy()
            for state in self.STATES:
                minimum = float('inf')
                for action in self.ACTIONS:
                    bellman_result = self.bellman_equation(state, action, old_values, pct)
                    if bellman_result < minimum:
                        minimum = bellman_result
                        self.prev_action[state] = action
                if state in self.GOAL:
                    self.prev_action[state] = "undefined"
                values[state] = minimum
        return self.prev_action


text = "Welcome to the traffic management program. " \
    "Please enter the number of levels that will represent the traffic flow."
print(text)
levels = int(input("Enter the number of streets: \n"))
mdp = MDP("Data.csv", levels)
# mdp.generate_states()
optimal_policy = mdp.value_iteration()
print("OPTIMAL POLICY:")
for key in optimal_policy.keys():
    print(key, "--->", optimal_policy[key])
