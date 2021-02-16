# Variables needed for coordinates
obstacle_list = []
min_x,max_x = -95,95 
min_y,max_y = -195,195 
def walls_x(x, x1, y):
    '''
    Makes a wall on the x-axis 
    :param x,x1,y:
    '''
    global obstacle_list
    while x <= x1:
        obstacle_list.append((x,y))
        x+=4
def door_for_walls_x(x, x1, y):
    global obstacle_list
    while x <= x1:
        obstacle_list.remove((x,y))
        x+=4
def walls_y(x, y1, y):
    global obstacle_list
    while y <= y1:
        obstacle_list.append((x,y))
        y+=4
def door_for_walls_y(x, y1, y):
    '''
    Makes a wall on the x-axis 
    :param x,y1,y:
    '''
    global obstacle_list
    while y <= y1:
        obstacle_list.remove((x,y))
        y+=4
def create_random_obstacles():
    '''
    Generates the random coordinates for the blocked path
    '''
    walls_x(-80,80,150)
    walls_x(-80,80,-150)
    walls_x(-50,50,100)
    walls_x(-50,50,-100)
    walls_x(-20,20,50)
    walls_x(-20,20,-50)
    walls_y(80,150,-150)
    walls_y(-80,150,-150)
    walls_y(-50,100,-100)
    walls_y(50,100,-100)
    walls_y(-20,50,-50)
    walls_y(20,50,-50)
    door_for_walls_x(0,12,150)
    door_for_walls_y(50,-32,-44)
    door_for_walls_y(-20,-2,-14)
    return obstacle_list
def is_position_blocked(x, y):
    '''
    Checks if robot is in a location where there is an obstical
    :param x,y:
    :return True if it is else False
    '''
    for obs in obstacle_list:
        if (obs[0] <= x <= obs[0] + 4 and
            obs[1] <= y <= obs[1] + 4):
            return True
    return False
def is_path_blocked(x1, y1, x2, y2):
    '''
    Checks if robot will walk into an obstical trying to get where it wants to go
    :param x1,x2,y1,y2:
    :return True if it is else False
    '''
    if x1 == x2:
        for y in range(min(y1,y2),max(y1,y2)):
            if is_position_blocked(x1,y):
                return True
    elif y1 == y2:
        for x in range(min(x1,x2),max(x1,x2)):
            if is_position_blocked(x,y1):
                return True
    return False
def get_obstacles():
    return create_random_obstacles()