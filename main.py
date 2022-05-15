"""Main module docstring"""
import pandas

# ------------- reset the size of the terminal -------------
pandas.options.display.max_columns = None


class MDP:

    def __init__(self, input_file, levels_num):
        self.df = pandas.read_csv(input_file, sep=";")
        # convert the dataframe with our data to a list
        self.data_list = self.df.to_numpy()
        self.levels_num = levels_num
        self.actions = []
        self.states = []
        self.goal = ["L"*self.levels_num]
        self.states_with_direction = {}
        # probabilities will be a matrix that stores all the probabilities
        self.probabilities = []
        self.pct = None
        self.optimal_policy = {}

    @staticmethod
    def simplify_data(line):
        """Method that keeps the first letter of the characters in the entered row
        to ease working with the data. It returns two strings:
        a string with the initial state and the action,
        and another string with the final state"""
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

    def generate_states_and_actions(self):
        """Method that generates the lists self.states and self.actions and sorts them"""
        df_unique = self.df.drop_duplicates()
        unique_lines = df_unique.to_numpy()
        for line in unique_lines:
            state_and_dir, final_state = self.simplify_data(line)
            result = state_and_dir.split("-")
            state = result[0]
            action = result[1]
            if final_state not in self.states:
                self.states.append(final_state)
            if state not in self.states:
                self.states.append(state)
            if action not in self.actions:
                self.actions.append(action)
        self.states.sort()
        self.actions.sort()

    def fill_probability_matrix(self):
        """Method that fills the probability matrix with 0s"""
        probabilities = []
        for row in range(len(self.states_with_direction)):
            probabilities.append([])
            for col in range(len(self.states)):
                probabilities[row].append(0)
        self.probabilities = probabilities

    def create_states_with_direction(self):
        """This method creates the keys of the states_with_direction dictionary and assigns it a counter of 0.
        These keys will have the form: levellevellevel-action"""
        self.generate_states_and_actions()
        for state in self.states:
            for action in self.actions:
                self.states_with_direction[state + "-" + action] = 0
        # store the states and direction in a list
        states_and_dir = list(self.states_with_direction.keys())
        return states_and_dir

    def count_occurrences(self):
        """This method calculates how many times each levellevellevel-action key appears in the data"""
        states_and_dir = self.create_states_with_direction()
        self.fill_probability_matrix()
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
                for state in self.states:
                    if i_state_and_action == row and f_state == state:
                        self.probabilities[states_and_dir.index(row)][self.states.index(state)] += 1
        return states_and_dir

    def calculate_probabilities(self):
        """This method calculates the probabilities"""
        states_and_dir = self.count_occurrences()
        for idx_row, row in enumerate(states_and_dir):
            for idx_col in range(len(self.states)):
                try:
                    previous = self.probabilities[idx_row][idx_col]
                    probability = previous / self.states_with_direction[row]
                    self.probabilities[idx_row][idx_col] = probability
                except ZeroDivisionError:
                    self.probabilities[idx_row][idx_col] = 0
        self.pct = pandas.DataFrame(self.probabilities, index=states_and_dir, columns=self.states)

    def cost(self, state, n_action):
        """This method returns the cost of performing an action depending on the action taken before"""
        try:
            if n_action == self.optimal_policy[state]:
                return 1
            if n_action != self.optimal_policy[state]:
                return 2
        except KeyError:
            return 1

    def bellman_equation(self, init_state, action, old_values):
        """This method returns the value obtained by using the Bellman Equation"""
        if init_state in self.goal:
            return 0
        value = self.cost(init_state, action)
        for next_state in self.states:
            state = init_state + "-" + action
            value += self.pct.loc[state, next_state] * old_values[next_state]
        return value

    def value_iteration(self):
        """This method performs iterations of the values of the states until two of them converge"""
        self.calculate_probabilities()
        values = {state: 0 for state in self.states}
        old_values = {}
        while old_values != values:
            old_values = values.copy()
            for state in self.states:
                minimum = float('inf')
                for action in self.actions:
                    bellman_result = self.bellman_equation(state, action, old_values)
                    # we save the minimum value
                    if bellman_result < minimum:
                        minimum = bellman_result
                        self.optimal_policy[state] = action
                if state in self.goal:
                    self.optimal_policy[state] = "undefined"
                values[state] = minimum
        return self.optimal_policy


if __name__ == '__main__':
    print("Welcome to the traffic management program. "
          "Please enter the number of levels that will represent the traffic flow.")
    levels = int(input("Enter the number of streets: \n"))
    mdp = MDP("Data.csv", levels)
    optimal_policy = mdp.value_iteration()
    print("OPTIMAL POLICY:")
    for key in optimal_policy.keys():
        print(key, "--->", optimal_policy[key])
