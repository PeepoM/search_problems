from SearchProblem import *


class EightPuzzle(SearchProblem):
    def __init__(self, init_state, goal_state):
        super().__init__(init_state, goal_state)

    def locate_empty(self, state):
        return state.index(0)

    def result(self, state, action):
        i_empty = self.locate_empty(state)
        new_state = list(state)

        actions = {"UP": -3, "DOWN": 3, "LEFT": -1, "RIGHT": 1}
        to_swap = i_empty + actions[action]

        new_state[i_empty], new_state[to_swap] = new_state[to_swap], new_state[i_empty]

        return tuple(new_state)

    def actions(self, state):
        possible_actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        i_empty = self.locate_empty(state)

        if i_empty % 3 == 0:
            possible_actions.remove("LEFT")
        if i_empty < 3:
            possible_actions.remove("UP")
        if i_empty % 3 == 2:
            possible_actions.remove("RIGHT")
        if i_empty > 5:
            possible_actions.remove("DOWN")

        return possible_actions

    def step_cost(self, state, action):
        return 1

    def h_misplaced(self, node):
        # number of misplaced tiles
        state = node.state

        misplaced = 0
        for i in range(len(state)):
            e = state[i]
            if e != i:
                misplaced += 1

        return misplaced

    def h_manhattan(self, node):
        state = node.state

        man_dist = 0
        for i in range(len(state)):
            e = state[i]
            if e == 0:
                continue

            # coordinate transform from 1D to 2D
            i_curr = i // 3
            j_curr = i % 3

            # i, j coordinates, where the number is supposed to be
            i_supp = e // 3
            j_supp = e % 3

            man_dist += abs(i_supp - i_curr) + abs(j_supp - j_curr)

        return man_dist

    def display_state(self, state):
        separator = "-------------"
        print(separator)
        for i in range(len(state)):
            if (i + 1) % 3 == 1:
                print(f"| {state[i]}", end=" | ")
            elif (i + 1) % 3 == 0:
                print(f"{state[i]} |")
                print(separator)
            else:
                print(state[i], end=" | ")
        print()


# Eight Puzzle
init_state = (7, 2, 4, 5, 0, 6, 8, 3, 1)
goal_state = tuple(range(9))
eight_puzzle = EightPuzzle(init_state, goal_state)

search_algos = [a_star_search, best_first_search]
heuristics = [eight_puzzle.h_manhattan, eight_puzzle.h_misplaced]

for algo in search_algos:
    for heuristic in heuristics:
        print(f"running {algo.__name__} with {heuristic.__name__} heuristic")
        goal_node = algo(eight_puzzle, heuristic)
        path_len = len(goal_node.reconstruct_path())
        print(f"path of length {path_len} was found\n")
