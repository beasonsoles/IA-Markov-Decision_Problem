"""Main module docstring"""
import pandas

# ------------- reset the size of the terminal -------------
pandas.options.display.max_columns = None


class MDP:

    def __init__(self, input_file):
        # ------------- variables -------------
        self.df = pandas.read_csv(input_file, sep=";")
        # convert the dataframe with our data to a list
        self.data_list = self.df.to_numpy()
        self.unique_lines = []
        # these three constants can be changed by the user
        self.NUMBER_OF_ROADS = 3
        self.TRAFFIC_LEVELS = ["H", "L"]
        self.ACTIONS = ["E", "N", "W"]
        self.STATES = ["HHH", "HHL", "HLH", "HLL", "LHH", "LHL", "LLH", "LLL"]
        # generate the states
        # STATES = []
        self.states_with_direction = {}
        # probabilities will be a matrix that stores all the probabilities
        self.probabilities = []
        # self.prev_action = {}
        # self.data_actions = []

    # ------------- functions -------------
    def get_unique_lines(self):
        df_unique = self.df.drop_duplicates()
        self.unique_lines = df_unique.to_numpy()

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
                    # self.data_actions.append(column)
                    initial_state_and_action += "-" + column
                    action_found = True
            else:
                if column == "High":
                    final_state += "H"
                elif column == "Low":
                    final_state += "L"
        return initial_state_and_action, final_state

    def generate_states(self, l):  # RECURSION FUNCTION FOR THE FOR LOOPS
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
    # def count_occurrences(self):
    #     extract first part of calculate_probabilities

    def calculate_probabilities(self):
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
        # calculate the probabilities
        for row in range(len(states_and_dir)):
            for column in range(len(self.STATES)):
                try:
                    previous = self.probabilities[row][column]
                    probability = previous / self.states_with_direction.get(states_and_dir[row])
                    self.probabilities[row][column] = probability
                except ZeroDivisionError:
                    self.probabilities[row][column] = 0
            # print("ihs", sum(self.probabilities[row]) == 1)
        pct = pandas.DataFrame(self.probabilities, index=states_and_dir, columns=self.STATES)
        # print(pct)
        return pct

    def cost(self, n_action):
        try:
            if n_action == self.prev_action or self.prev_action is None:
                return 1
            elif n_action != self.prev_action:
                return 2
        except IndexError:
            return 0

    def bellman_equation(self, init_state, action, old_values, pct):
        # print("old value", old_values.get(self.STATES["HHH"]))
        # optimal_action = {action: 0 for action in self.ACTIONS}
        # optimal_action[action] = self.cost(action)
        value = self.cost(action)
        count = 0
        for next_state in self.STATES:
            state = init_state + "-" + action
            count += pct.loc[state, next_state]
            value += pct.loc[state, next_state] * old_values[next_state]
        if init_state == 'HHH':
            print("value", value)
        # if (action == 'W' or action == 'E') and init_state == 'HHH':
            # print(old_values)
            # print('uwu', action, value)
        # print(init_state, action, "OK", count == 1)
        return value

    def value_iteration(self):
        pct = self.calculate_probabilities()
        action = ""
        values = {state: 0 for state in self.STATES}
        optimal_policy = {state: "" for state in self.STATES}
        old_values = {}
        while old_values != values:
            for i in values.keys():
                old_values[i] = values[i]
            for state in self.STATES:
                self.prev_action = None
                optimal_action = {}
                minimum = float('inf')
                for action in self.ACTIONS:
                    bellman = self.bellman_equation(state, action, old_values, pct)
                    if bellman < minimum:
                        minimum = bellman
                        optimal_action[action] = minimum
                        self.prev_action = action
                values[state] = minimum
                action_index = list(optimal_action.values()).index(values[state])
                action = list(optimal_action.keys())[action_index]
                optimal_policy[state] = self.prev_action
        return optimal_policy


mdp = MDP("Data.csv")
result = mdp.value_iteration()
# optimal_policy = pandas.DataFrame(result, index=mdp.STATES)
print("optimal policy", list(result.values()))
