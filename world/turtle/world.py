import turtle
import sys
import import_helper

try:
    obstacles = import_helper.dynamic_import('maze.' + sys.argv[2])
    obs_module = sys.argv[2]
except:
    from maze import obstacles
    obs_module = "obstacles"

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100

#turtle variables
robo_turtle = None

# global obstacle_list to only make obtacles once
obstacle_list = []

def setup_world(robot_name):
    """
    initialising the module
    """
    global robo_turtle, obstacle_list
    print(f"{robot_name}: Loaded {obs_module}.")
    obstacle_list = obstacles.get_obstacles()
    robo_turtle = turtle.Turtle()
    screen = turtle.Screen()
    screen.tracer(False)
    screen.setup((max_x - min_x) * 4, (max_y - min_y) * 4)
    screen.setworldcoordinates(min_x, min_y, max_x, max_y)
    robo_turtle.color("red")
    make_obstacles()
    make_border()
    screen.tracer(True)


def show_position(robot_name):
    """
    pass cause contingency
    """
    pass


def make_border():
    """
    draws border from area limit global variables
    """
    global robo_turtle
    robo_turtle.penup()
    robo_turtle.setpos(min_x, min_y)
    robo_turtle.pendown()
    robo_turtle.setpos(max_x, min_y)
    robo_turtle.setpos(max_x, max_y)
    robo_turtle.setpos(min_x, max_y)
    robo_turtle.setpos(min_x, min_y)
    robo_turtle.penup()
    robo_turtle.goto(0, 0)
    robo_turtle.setheading(90)
    robo_turtle.color("black")
    robo_turtle.pendown()


def make_obstacles():
    """
    gets objects from obstacles and draws them
    """
    
    for obs in obstacle_list:
        robo_turtle.penup()
        robo_turtle.goto(obs[0], obs[1])
        robo_turtle.pendown()
        robo_turtle.begin_fill()
        robo_turtle.goto(obs[0], obs[1] + 4)
        robo_turtle.goto(obs[0] + 4, obs[1] + 4)
        robo_turtle.goto(obs[0] + 4, obs[1])
        robo_turtle.goto(obs[0], obs[1])
        robo_turtle.end_fill()
    robo_turtle.penup()


def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global robo_turtle
    robo_turtle._tracer(False)
    new_x = robo_turtle.xcor()
    new_y = robo_turtle.ycor()
    if robo_turtle.heading() == 90:
        new_y = new_y + steps
    elif robo_turtle.heading() == 0:
        new_x = new_x + steps
    elif robo_turtle.heading() == 270:
        new_y = new_y - steps
    elif robo_turtle.heading() == 180:
        new_x = new_x - steps

    if not is_position_allowed(new_x, new_y):
        return "unsafe"
    elif obstacles.is_path_blocked(robo_turtle.xcor(), robo_turtle.ycor(), new_x, new_y):
        return "obstacle"
    else:
        robo_turtle.setpos(new_x, new_y)
        robo_turtle._tracer(True)
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
    robo_turtle._tracer(False)
    robo_turtle.left(90)
    robo_turtle._tracer(True)


def do_right():
    robo_turtle._tracer(False)
    robo_turtle.right(90)
    robo_turtle._tracer(True)


def get_pos():
    """Returns current vectors

    Returns:
        Tuple: Current position of robot
    """
    if robo_turtle.heading() == 90:
        return ((robo_turtle.xcor(), robo_turtle.ycor(), 0))
    elif robo_turtle.heading() == 0:
        return ((robo_turtle.xcor(), robo_turtle.ycor(), 1))
    elif robo_turtle.heading() == 270:
        return ((robo_turtle.xcor(), robo_turtle.ycor(), 2))
    elif robo_turtle.heading() == 180:
        return ((robo_turtle.xcor(), robo_turtle.ycor(), 3))


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