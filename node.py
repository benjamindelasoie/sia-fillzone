class Node:

    def __init__(self, state, visited, cost, parent, color, value):
        self.visited = visited
        self.state = state
        self.color = color
        self.parent = parent
        self.cost = cost
        self.value = value

    def set_cost(self, cost):
        self.cost = cost

    def set_value(self, value):
        self.value = value
