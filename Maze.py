from MazeUI import *
from queue import PriorityQueue
import random
import functools

# Cell class representing one cell of a maze
@functools.total_ordering
class Cell():
    def __init__(self, location):
        self.location = location
        self.walls = []
        self.visited = False
        self.weight = 1

    def __lt__(self, other):
        return self.weight < getattr(other, 'weight', other)

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False

        return ((other.location == self.location) and
                (other.visited == self.visited) and
                (other.walls == self.walls))

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return str(self.location)

# Wall class representing a wall between two cells
@functools.total_ordering
class Wall():
    def __init__(self, parent_one, parent_two):
        self.parent_one = parent_one
        self.parent_two = parent_two
        self.open = False
        self.weight = 1

    def __lt__(self, other):
        return self.weight < getattr(other, 'weight', other)

    def __eq__(self, other):
        if not isinstance(other, Wall):
            return False

        return ((other.parent_one != other.parent_two) and
                (other.parent_one == self.parent_one or
                 other.parent_one == self.parent_two) and
                (other.parent_two == self.parent_one or
                 other.parent_two == self.parent_two))

    def __hash__(self):
        return hash(self.parent_one, self.parent_two)

    def __repr__(self):
        if self.open:
            return str(self.parent_one) + " <---> " + str(self.parent_two)
        else:
            return str(self.parent_one) + " <-/-> " + str(self.parent_two)

# Initialize cells/walls in maze
def init_maze(height, width):
    cellList = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(Cell((i, j)))
        cellList.append(row)

    # Corners
    cellList[0][0].walls.append(Wall(cellList[0][0], cellList[0][1]))
    cellList[0][0].walls.append(Wall(cellList[0][0], cellList[1][0]))
    cellList[height - 1][0].walls.append(Wall(cellList[height - 1][0], cellList[height - 1][1]))
    cellList[height - 1][0].walls.append(Wall(cellList[height - 1][0], cellList[height - 2][0]))
    cellList[0][width - 1].walls.append(Wall(cellList[0][width - 1], cellList[0][width - 2]))
    cellList[0][width - 1].walls.append(Wall(cellList[0][width - 1], cellList[1][width - 1]))
    cellList[height - 1][width - 1].walls.append(Wall(cellList[height - 1][width - 1], cellList[height - 1][width - 2]))
    cellList[height - 1][width - 1].walls.append(Wall(cellList[height - 1][width - 1], cellList[height - 2][width - 1]))

    # Edges
    for i in range(1, height - 1):
        cellList[i][0].walls.append(Wall(cellList[i][0], cellList[i - 1][0]))
        cellList[i][0].walls.append(Wall(cellList[i][0], cellList[i][1]))
        cellList[i][0].walls.append(Wall(cellList[i][0], cellList[i + 1][0]))

        cellList[i][width - 1].walls.append(Wall(cellList[i][width - 1], cellList[i - 1][width - 1]))
        cellList[i][width - 1].walls.append(Wall(cellList[i][width - 1], cellList[i][width - 2]))
        cellList[i][width - 1].walls.append(Wall(cellList[i][width - 1], cellList[i + 1][width - 1]))
    for i in range(1, width - 1):
        cellList[0][i].walls.append(Wall(cellList[0][i], cellList[0][i - 1]))
        cellList[0][i].walls.append(Wall(cellList[0][i], cellList[1][i]))
        cellList[0][i].walls.append(Wall(cellList[0][i], cellList[0][i + 1]))

        cellList[height - 1][i].walls.append(Wall(cellList[height - 1][i], cellList[height - 1][i - 1]))
        cellList[height - 1][i].walls.append(Wall(cellList[height - 1][i], cellList[height - 2][i]))
        cellList[height - 1][i].walls.append(Wall(cellList[height - 1][i], cellList[height - 1][i + 1]))

    # Inside
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            cellList[i][j].walls.append(Wall(cellList[i][j], cellList[i - 1][j]))
            cellList[i][j].walls.append(Wall(cellList[i][j], cellList[i + 1][j]))
            cellList[i][j].walls.append(Wall(cellList[i][j], cellList[i][j - 1]))
            cellList[i][j].walls.append(Wall(cellList[i][j], cellList[i][j + 1]))
    return cellList

# Generates randomized walls of maze (Prim's Algorithm)
def generate_maze(cellList):
    height, width = len(cellList), len(cellList[0])

    startCell = cellList[height - 1][width - 1]
    startCell.visited = True

    wallList = PriorityQueue()
    for wall in startCell.walls:
        wall.weight = random.randint(1, 10)
        wallList.put(wall)

    while not wallList.empty():
        randomWall = wallList.get()

        if not randomWall.parent_two.visited:
            neighborCell = randomWall.parent_two
            randomWall.open = True
            neighborCell.walls[neighborCell.walls.index(randomWall)].open = True
            neighborCell.visited = True

            for wall in neighborCell.walls:
                wall.weight = random.randint(1, 10)
                wallList.put(wall)
    return cellList

# Sovles maze using BFS
def solve_maze(maze):
    visited = set()
    queue = PriorityQueue()

    start = maze[0][0]
    goal = maze[len(maze) - 1][len(maze[0]) - 1]

    visited.add(start)
    for wall in start.walls:
        if wall.open:
            queue.put([start, wall.parent_two])

    while not queue.empty():
        currPath = queue.get()
        currCell = currPath[len(currPath) - 1]

        for wall in currCell.walls:
            if wall.parent_two == goal and wall.open:
                return currPath + [goal]
            elif not wall.parent_two in visited and wall.open:
                queue.put(currPath + [wall.parent_two])
                visited.add(wall.parent_two)

def main():
    height, width = 0, 0

    # Get user input for height and width
    user_input = input("Enter the maze height and maze width: ").split()
    while(True):
        if len(user_input) != 2:
            user_input = input("Please enter two arguments in format: " +
                               "<maze height> <maze width>: ").split()
        else:
            try:
                height, width = int(user_input[0]), int(user_input[1])

                if height < 2 or width < 2:
                    user_input = input("Please enter maze size greater than 1 x 1 in format: " +
                                       "<maze height> <maze width>: ").split()
                else:
                    break
            except ValueError:
                user_input = input("Please enter an integer in format: " +
                                   "<maze height> <maze width>: ").split()

    # Initialize maze
    cellList = init_maze(height, width)
    maze = generate_maze(cellList)
    solution = solve_maze(maze)

    # Draw maze
    draw(maze, "maze", solution)

main()
