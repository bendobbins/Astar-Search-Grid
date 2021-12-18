class Node:
    """
    Class keeps track of each space that can be explored as well as the heuristic distance
    from that space to the end, and the path from the start to that space (cost is length of the path).
    """

    def __init__(self, state, heuristic, path):
        self.state = state
        self.heuristic = heuristic
        self.path = path
        self.cost = len(self.path)


class AstarFrontier():
    """
    Defines a list as the frontier and provides functions that do tasks useful for A* search.
    """

    def __init__(self):
        self.frontier = []

    def add(self, node):
        """
        Adds a node to the end of the frontier.
        """
        self.frontier.append(node)

    def empty(self):
        """
        Returns if the frontier is empty.
        """
        return len(self.frontier) == 0

    def purge(self, nodes):
        """
        Removes every node in a list of nodes from the frontier.
        """
        for node in nodes:
            self.frontier.remove(node)

    def bestCost(self, newNode):
        """
        Makes a list of nodes from the frontier with the same state as the newNode parameter, then returns that list
        as well as the node in the list with the shortest path length.
        """
        nodes = [newNode]
        for node in self.frontier:
            if node.state == newNode.state:
                nodes.append(node)

        bestPath = 1000
        for node in nodes:
            if len(node.path) < bestPath:
                bestPath = len(node.path)
                bestNode = node

        return nodes, bestNode

    def retrieve(self):
        """
        Finds the node in the frontier with the smallest f(n), removes it from the frontier and returns it.
        f(n) = h(n) + g(n)
        h(n) -- Node heuristic
        g(n) -- Node cost
        """
        bestPath = 1000
        for node in self.frontier:
            if (node.heuristic + node.cost) < bestPath:
                bestPath = node.heuristic + node.cost
                bestNode = node

        self.frontier.remove(bestNode)
        return bestNode