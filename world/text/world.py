import sys
import import_helper

try:
    obstacles = import_helper.dynamic_import('maze.' + sys.argv[2])
    obs_module = sys.argv[2]
except:
    from maze import obstacles
    obs_module = "obstacles"

# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100

# global obstacle_list to only make obtacles once
obstacle_list = []
def setup_world(robot_name):
    """
    initialise global variables
    """
    global position_x, position_y, current_direction_index, obstacle_list
    print(f"{robot_name}: Loaded {obs_module}.")
    obstacle_list = obstacles.get_obstacles()
    position_x = 0
    position_y = 0
    current_direction_index = 0

    make_obstacles()


def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')


def make_obstacles():
    """
    initiates the obstacles module and prints out
    each object created by the module
    """
    if obstacle_list :
        print("There are some obstacles:")
        for obst in obstacle_list :
            print(f"- At position {obst[0]},{obst[1]} (to {obst[0] + 4},{obst[1] + 4})")


def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    if not is_position_allowed(new_x, new_y):
        return "unsafe"
    elif obstacles.is_path_blocked(position_x, position_y, new_x, new_y):
        return "obstacle"
    else:
        position_x = new_x
        position_y = new_y
        return "safe"


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def do_left():
    global current_direction_index

    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3


def do_right():
    global current_direction_index

    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0


def get_pos():
    """Returns current vectors

    Returns:
        Tuple: Current position of robot
    """
    return ((position_x, position_y, current_direction_index))


def at_right_edge(goal, pos, width, height):
    """
    Used by get_maize to determain if "pos" is on the
    "goal" edge

    Args:
        goal (String): "top", "bottom" ,"left", "right"
                       The side to be reached by the mazerun command
        pos (Tuple): Position to be checked
        width (Integer): Width of area
        height (Integer): Height of area

    Returns:
        Boolean: True if the location is on the edge else False
    """ 
    if goal == "top" and pos[1] == height - 1:
        return True
    if goal == "bottom" and pos[1] == 0:
        return True
    if goal == "left" and pos[0] == 0:
        return True
    if goal == "right" and pos[0] == width - 1:
        return True
    return False


def get_maze(goal):
    """
    Used to aid solving the maze
    
    Creates a two dimentional array 
    representing each pixel where:
    0 = Open path
    1 = An opstacle
    2 = A "goal" cell

    The fist set of for loops sets each "object" cell
    to 1

    The second set of for loops sets the border to either
    2 or 1 depending on whether or not it is the goal side or not

    There is try blocks in case there are obstacles 
    outside the relevant map area

    Args:
        goal (String): The side to be reached by the mazerunner

    Returns:
        list[list[Integer]]: The two dimentional array 
                             used to solve the maze.
    """
    width = max_x - min_x + 3
    height = max_y - min_y + 3
    maze = [[ 0 for x in range(height)] for y in range(width)]

    for obstacle in obstacle_list:
        for x in range(obstacle[0] + 101, obstacle[0] + 106):
            for y in range(obstacle[1] + 201, obstacle[1] + 206):
                try:
                    maze[abs(x)][abs(y)] = 1
                except IndexError:
                    pass
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            try:
                if at_right_edge(goal, (x, y), width, height):
                    maze[x][y] = 2
                elif (x == 0 or x == width - 1 or
                    y == 0 or y == height - 1):
                    maze[x][y] = 1
            except IndexError:
                pass
    return maze