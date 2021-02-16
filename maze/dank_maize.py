import random

obstacle_list = []
visited_nodes = []
min_y, max_y = -40, 38
min_x, max_x = -20, 18


def valid_node(loc):
    """
    Used by my maze generation algorithm.
    Used to determain if this 5X5 cell is a valid place 
    to put a road.

    Args:
        loc (tuple): Position to be validated

    Returns:
        Boolean: True if it is valid else False
    """
    if (loc[0], loc[1]) in obstacle_list:
        return False
    if (loc[0], loc[1]) in visited_nodes:
        return False
    if (-105 <= loc[0] < 100 and
        -205 <= loc[1] < 200):
        return True


def make_loc(loc, direction):
    """
    Used by my maze generation algorithm.
    Used to determain the location of a new node
    in a certain direction.

    Args:
        loc (Tuple): Current location
        direction (Int): Current direction

    Returns:
        tuple : position of the next node in this direction, 
        tuple : position of the obstacle between the current
                and potential node (used to remove the obstacle, 
                if this is a valid node, to make the route between the 2)
    """
    if direction == 0:
        return (loc[0] + 10, loc[1]), (loc[0] + 5, loc[1])
    if direction == 1:
        return (loc[0], loc[1] + 10), (loc[0], loc[1] + 5)
    if direction == 2:
        return (loc[0] - 10, loc[1]), (loc[0] - 5, loc[1])
    if direction == 3:
        return (loc[0], loc[1] - 10), (loc[0], loc[1] - 5)


def make_maze(loc):
    """
    Main part of the maize making process.

     - Chooses a random order of directions to
       check for a possible paths
     - checks each path and follows it:
       - clearing obstacles in the way
       - adds the path to visited_nodes
       - recurses
    
    Args:
        loc (tuple): Starting point of the maze maker.
    """
    global obstacle_list, visited_nodes

    directions = [0,1,2,3]
    random.shuffle(directions)
    for i in directions:
        new_loc, wall = make_loc(loc, i)
        if valid_node(new_loc):
            obstacle_list.remove(wall)
            visited_nodes.append(new_loc)
            make_maze(new_loc)


def make_border_obstacles():
    """
    Generates obstacles all around the border 
    and randomly removes an accessable one on each side
    """
    global obstacle_list
    obstacle_list = []
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            if (x == min_x - 1 or x == max_x + 1 or 
                y == min_y - 1 or y == max_y + 1):
                obstacle_list.append((x * 5, y * 5))
    obstacle_list.remove(((min_x - 1) * 5,(random.randrange(min_y + 1, max_y - 1, 2)) * 5))
    obstacle_list.remove(((max_x + 1) * 5,(random.randrange(min_y + 1, max_y - 1, 2)) * 5))
    obstacle_list.remove(((random.randrange(min_x + 1, max_x - 1, 2)) * 5, (min_y - 1) * 5))
    obstacle_list.remove(((random.randrange(min_x + 1, max_x - 1, 2)) * 5, (max_y + 1) * 5))


def create_random_obstacles():
    """
    Driver funtion to creates all obstacles
    and add them to the obsticle_list list.
    
     - Starts by making the border
     - Followed by creating a grid/node system for the
       make_maze to work from
     - shifts all obstacles to fit better in a 200 X 400 area
    """
    global obstacle_list
    obstacle_list = []

    make_border_obstacles()

    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y + 1):
            if not(x % 2 == 1 and y % 2 == 1):
                obstacle_list.append((x * 5, y * 5))
    visited_nodes.append((-5,-5))
    make_maze((-5,-5))
    
    new_list = []
    for obs in obstacle_list:
        new_list.append((obs[0] + 2, obs[1] + 2))
    obstacle_list = new_list


def is_position_blocked(x, y):
    """Loops through object_list to see if the
       parameter coordinates is inside one of the objects

    Args:
        x_cor (int): x coordinate to be checked if in any object
        y_cor (int): y coordinate to be checked if in any object

    Returns:
        Boolean : True if coordinates is in an object else false
    """
    for obs in obstacle_list:
        if (obs[0] <= x <= obs[0] + 4 and
           obs[1] <= y <= obs[1] + 4):
           return True
    return False


def is_path_blocked(x1, y1, x2, y2):
    """loops through coordinates between x1, y1 and x2, y2
       and calls is_position_blocked to see if there is an object
       in the path

    Args:
        x1 (int): starting x
        y1 (int): starting y
        x2 (int): ending x
        y2 (int): ending y

    Returns:
        Boolean: True if there is an object on the path else false
    """
    direction_x = 1 if x2 >= x1 else -1
    direction_y = 1 if y2 >= y1 else -1
    for x in range(x1, x2 + direction_x, direction_x):
        for y in range(y1, y2 + direction_y, direction_y):
            if is_position_blocked(x, y):
                return True
    return False


def get_obstacles():
    """Returns global list of all tracked objects
       created by this module

    Returns:
        List: obstacle_list
    """
    create_random_obstacles()
    return obstacle_list