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
        self.ACTIONS = ["N", "E", "W"]
        self.STATES = ["HHH", "HHL", "HLH", "HLL", "LHH", "LHL", "LLH", "LLL"]
        # generate the states
        # STATES = []
        self.states_with_direction = {}
        # probabilities will be a matrix that stores all the probabilities
        self.probabilities = []
        self.prev_action = None
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
        pct = pandas.DataFrame(self.probabilities, index=states_and_dir, columns=self.STATES)
        return pct

    def cost(self, n_action):
        try:
            # print("l",line_num)
            # o_action = self.data_actions[line_num - 1]
            # n_action = self.data_actions[line_num]
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
        for next_state in self.STATES:
            state = init_state + "-" + action
            value += float(pct.loc[state, next_state] * old_values[next_state])
        if (action == 'W' or action == 'E') and init_state == 'HHH':
            print(old_values)
            print('uwu', action, value)

        return value

    def value_iteration(self):
        pct = self.calculate_probabilities()
        print(pct)
        values = {state: 0 for state in self.STATES}
        optimal_policy = {state: "" for state in self.STATES}
        old_values = {}
        while old_values != values:
            # print(old_values)
            # print(values)
            for i in values.keys():
                old_values[i] = values[i]
            for state in self.STATES:
                optimal_action = {}
                for action in self.ACTIONS:
                    optimal_action[action] = self.bellman_equation(state, action, old_values, pct)
                values[state] = float(min(list(optimal_action.values())))
                action_index = list(optimal_action.values()).index(values[state])
                action = list(optimal_action.keys())[action_index]
                if state == 'HHH':
                    print(values[state], action)
                self.prev_action = action
                optimal_policy[state] = self.prev_action
                #     optimal_policy[initial_state] = self.prev_action
                    # value = min(optimal_action.values())
                    # # print("value", value)
                    # action_index = list(optimal_action.values()).index(value)
                    # action = list(optimal_action.keys())[action_index]
                    # print(optimal_action)
                # print("old", old_values)
                # new_line = self.simplify_data(line)
                # print("6565", new_line)
                # example: if "HHH" in "HHH-E"
                # if s in new_line[0]:
                # the action is the last character of the first result obtained from simplify_data
                # result = line.split("-")
                # initial_state = result[0]
                # for s_idx, s in enumerate(self.STATES):
                # policy = {action: 0 for action in self.ACTIONS}

                #     print(old_values,values)
                #     # print("bellman", values[initial_state])
                #     self.prev_action = action
                #     optimal_policy[initial_state] = self.prev_action

                # for s in self.STATES:
                #     print("%s value: %f" % (s, values[s]))
                # if old_values == values:
                #     convergence = True
        return optimal_policy


mdp = MDP("Data.csv")
result = mdp.value_iteration()
# optimal_policy = pandas.DataFrame(result, index=mdp.STATES)
print("optimal policy", list(result.values()))
