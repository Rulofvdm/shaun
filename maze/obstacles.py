import random

obstacle_list = []

def create_random_obstacles():
    global obstacle_list
    obstacle_list = []

    for i in range(random.randint(0, 9)):
        x_cor = random.randint(-100, 100)
        y_cor = random.randint(-200, 200)

        new_obstacle = (x_cor, y_cor)

        obstacle_list.append(new_obstacle)
    return obstacle_list


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