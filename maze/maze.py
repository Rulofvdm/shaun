import sys, os, random
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)

# creating the obstacles lists
obstacle_list = []

def create_obstacles(min_x, min_y, max_x, max_y):
    """
    """
    draw_lines(20, -10, 20, 50)
    draw_lines(20, 50, -20, 50)
    draw_lines(-20, 50, -20, -10)

    draw_lines(40, -10, 20, -10)
    draw_lines(40, -10, 40, -50)
    draw_lines(40 , -50,  -40, -50)
    draw_lines(-40, 100, -40, -50)
    
    draw_lines(60, 80, 0, 80)

    draw_lines(60, 100, -60, 100)
    draw_lines(60, -100, -60, -100)
    draw_lines(60, 100, 60, -100)
    draw_lines(-60, 100, -60, -60)

    draw_lines(-80, 150, -80, -150)
    draw_lines(-80, -150, 92, -150)
    draw_lines(80, 150, -80, 150)

    draw_lines(80, 146, 80, -134)
    draw_lines(96, 192, 96, -150)
    draw_lines(92, 196, -20, 196)
    draw_lines(-50, 196, -100, 196)

    draw_lines(-100, -200, -100, -50)
    draw_lines(-100, 192, -100, 30)
    draw_lines(-100, -200, -30, -200)
    draw_lines(10, -200, 92, -200)
    draw_lines(10, -184, 92, -184)
    draw_lines(96, -188, 96, -196)
    return obstacle_list


def is_position_blocked(x,y):
    """
    foreach set of tuples inside of the obstacles lists, it checks if the position of either x or y (which is the robot passed position) is in the range of the obstacle, 
    :returns True if the position is blocked:
    :returns False if the position is not blocked:
    """
    for tups in obstacle_list:
        tup_x = tups[0]
        tup_y = tups[1]
        if (tup_x <= x <= (tup_x + 4)) and (tup_y <= y <= (tup_y + 4)):
            return True
    return False


def is_path_blocked(x1, y1, x2, y2):
    """
    takes the min and max values passed through with x1 and y1 being the co-ords
    that you are at and x2 and y2 the co-ords that you are moving to. and checks
    that if the position you are moving towards has an obstacle in the way
    :returns True if the path is blocked:
    :returns False if the path is not blocked:
    """

    a1 = min(x1, x2)
    a2 = max(x1, x2)
    b1 = min(y1, y2)
    b2 = max(y1, y2)

    if x1 == x2:
        for i in range(b1, b2 + 1):
            if is_position_blocked(x1, i) :
                # print(x1, i)
                return True
    elif y1 == y2:
        for i in range(a1, a2 + 1):
            if is_position_blocked(i, y1):
                return True
    return False


def draw_lines(old_x, old_y, new_x, new_y):
    global obstacle_list

    sm_x = min(old_x, new_x)
    mx_x = max(old_x, new_x)
    sm_y = min(old_y, new_y)
    mx_y = max(old_y, new_y)

    if old_y == new_y:
        for i in range(sm_x, mx_x + 5, 5):
            obstacle_list.append((i, old_y))
    elif old_x == new_x:
        for i in range(sm_y, mx_y + 5, 5):
            obstacle_list.append((old_x, i))
    return obstacle_list


def get_obstacles():
    create_obstacles(-100, -200, 100, 200)
    return obstacle_list