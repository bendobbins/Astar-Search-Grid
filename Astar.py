import copy

from util import Node, AstarFrontier

def handle_input(endpoints):
    """
    Makes sure user input for start and end is properly formatted, then converts each string into a tuple of 2 ints, returning a list of the tuples.

    endpoints -- A tuple of 2 strings where the first is the start spot and the second is the end
    """
    points = []
    for endpoint in endpoints:
        if len(endpoint) >= 5:      # Smallest valid input will have length of 5, Ex: (1,1)

            if endpoint[0] == "(" and endpoint[-1] == ")":      # No input not in ()
                numbers = endpoint.split(",")

                if len(numbers) == 2:       # Make sure there is an x and y coord
                    counter = 0
                    for number in numbers:
                        # Clean up numbers before attempting int conversion
                        number = number.replace("(", "")
                        number = number.replace(")", "")
                        number = number.strip()

                        try:
                            number = int(number) - 1        # -1 because user inputs 1-50 and computer handles 0-49
                            if number < 0 or number > 49:
                                return points
                        except ValueError:      # Return incomplete points list if input is invalid
                            return points

                        numbers[counter] = number
                        counter += 1
                    points.append((numbers[0], numbers[1]))
    return points
    

def build_grid(walls, endpoints):
    """
    Builds grid for computer to use based on values from GUI user input.
    """
    grid = []
    for i in range(50):
        grid.append([])
        for j in range(50):
            if (i, j) in endpoints:
                grid[i].append(2)
            elif (i, j) in walls:
                grid[i].append(1)
            else:
                grid[i].append(0)
    return grid


def manhattan_distance(start, end):
    """
    Finds manhattan distance from any given point to end.
    """
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def chebyshev_distance(start, end):
    """
    Finds chebyshev distance from any given point to end.
    """
    return max(abs(start[0] - end[0]), abs(start[1] - end[1]))


def get_options(state, grid, explored):
    """
    Returns a list of coordinate tuples where each one represents a possible space that can continue a path.

    state -- Current space in path
    grid -- Grid of open spaces, walls and endpoints
    explored -- List of spaces already explored
    """
    # Spaces north, south, east, west, northeast, southeast, southwest and northwest of state
    adjacents = [
        (state[0], state[1] + 1),
        (state[0], state[1] - 1),
        (state[0] + 1, state[1]),
        (state[0] - 1, state[1]),
        (state[0] + 1, state[1] + 1),       # Comment the last four out if using Manhattan distance, only go NSEW
        (state[0] + 1, state[1] - 1),
        (state[0] - 1, state[1] - 1),
        (state[0] - 1, state[1] + 1)
        ]

    options = []
    for box in adjacents:
        if box[0] >= 0 and box[1] >= 0:     # Handle corner cases
            try:
                if grid[box[0]][box[1]] != 1:       # Check if space is wall
                    if box not in explored:
                        options.append(box)
            except IndexError:      # Handle corner cases
                pass
    return options


def shortest_path(walls, start, end):
    """
    Finds the shortest path around any walls between two points moving vertically and horizontally. Returns the path taken, or an empty path if none exists.

    walls -- set of coordinates where there are walls in the grid
    start -- startpoint
    end -- endpoint
    """
    # Initializing steps: build grid, start frontier and explored, add starting node
    grid = build_grid(walls, (start, end))
    explored = set()
    frontier = AstarFrontier()
    startNode = Node(state=start, heuristic=manhattan_distance(start, end), path=[])
    frontier.add(startNode)

    while True:
        # If there are no possible paths left
        if frontier.empty():
            return []

        # Pull the node with smallest f(n) out of frontier, add to explored and find possible adjacent spaces
        node = frontier.retrieve()
        explored.add(node.state)
        options = get_options(node.state, grid, explored)
        node.path.append(node.state)        # Add node state to path so that path can be passed to children

        for option in options:
            # Check if space is goal state
            if grid[option[0]][option[1]] == 2 and option != start:
                node.path.remove(start)
                return node.path

#            child = Node(state=option, heuristic=manhattan_distance(option, end), path=copy.deepcopy(node.path))       Manhattan version
            child = Node(state=option, heuristic=chebyshev_distance(option, end), path=copy.deepcopy(node.path))

            nodeList, bestNode = frontier.bestCost(child)       # List of nodes with same state as child and node in list with shortest path
            nodeList.remove(child)      # Child not in frontier yet, don't want it to be in list when purge happens

            if bestNode == child:
                frontier.add(child)     # If child has shortest path of all nodes with same state, add it to frontier
            else:
                nodeList.remove(bestNode)       # If node with shortest path is not child, remove it from list so it stays in frontier
            frontier.purge(nodeList)        # Remove all nodes with same state as child that don't have shortest path from frontier