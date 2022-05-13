from collections import deque
import heapq


class SearchProblem:
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state

    def result(self, state, action):
        raise NotImplementedError

    def step_cost(self, state, action):
        return 1

    def goal_test(self, state):
        return state == self.goal_state

    def actions(self, state):
        raise NotImplementedError

    def display_state(self, state):
        print(state)


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return isinstance(other, Node) and self.state < other.state

    def child_node(self, problem, action):
        state = problem.result(self.state, action)
        path_cost = self.path_cost + \
            problem.step_cost(self.state, action)
        child_node = Node(state, self, action, path_cost)

        return child_node

    def reconstruct_path(self):
        path = []
        current = self

        while current:
            path.append(current)
            current = current.parent

        return list(reversed(path))


def breadth_first_search(problem):
    node = Node(problem.init_state)
    if problem.goal_test(node.state):
        return node.state

    queue = deque([node])
    visited = set()  # set of visited states to avoid repetition

    while queue:
        node = queue.popleft()

        if problem.goal_test(node.state):
            return node.state

        for action in problem.actions(node.state):
            child_node = node.child_node(problem, action)
            if child_node.state not in visited:
                visited.add(child_node.state)
                queue.append(child_node)

    return None


def depth_first_search(problem):
    node = Node(problem.init_state)
    if problem.goal_test(node.state):
        return node.state

    stack = deque([node])
    visited = set()  # set of visited states to avoid repetition

    while stack:
        node = stack.pop()

        if problem.goal_test(node.state):
            return node.state

        if node.state not in visited:
            visited.add(node.state)
            for action in problem.actions(node.state):
                child_node = node.child_node(problem, action)
                stack.append(child_node)

    return None


def a_star_search(problem, h):
    return best_first_search(problem, lambda n: n.path_cost + h(n))


def best_first_search(problem, f):
    node = Node(problem.init_state)
    if problem.goal_test(node.state):
        return node.state

    queue = []
    heapq.heappush(queue, (f(node), node))

    visited = set()

    while queue:
        _, node = heapq.heappop(queue)

        if problem.goal_test(node.state):
            print(f"{len(visited)} nodes were explored")
            return node

        visited.add(node.state)

        for action in problem.actions(node.state):
            child_node = node.child_node(problem, action)
            if child_node.state not in visited:
                heapq.heappush(queue, (f(child_node), child_node))

    return None
