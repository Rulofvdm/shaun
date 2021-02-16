import re
import sys

if len(sys.argv) > 1 and sys.argv[1] == "turtle":
    from world.turtle import world
else:
    from world.text import world


# list of valid command names
valid_commands = ['off', 'help', 'forward', 'back', 'right', 'left', 'sprint', 'replay']
recorded_commands = ['forward', 'back', 'right', 'left', 'sprint']
commands_with_numbers_paramaters = ['forward', 'back', 'sprint']

#variable tracking command history
command_history = []

#TODO: WE NEED TO DECIDE IF WE WANT TO PRE_POPULATE A SOLUTION HERE, OR GET STUDENT TO BUILD ON THEIR PREVIOUS SOLUTION.

def get_robot_name():
    """
    Gets none robot name

    Returns:
        string: unfiltered none empty string
    """
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


def split_command_input(command):
    """
    Splits the string at the first space character,
    to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """

    (command_name, arg1) = split_command_input(command)
    if command_name.lower() in commands_with_numbers_paramaters:
        return arg1.isdigit()
    elif command_name.lower() == "replay":
        return correct_replay_flags(arg1.lower())
    elif command_name.lower() == "mazerun":
        return arg1.lower() in ["top", "bottom", "left", "right", ""]
    return command_name.lower() in valid_commands and not arg1


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)

    return command.lower()


def output(name, message):
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
MAZERUN - solves the maze for you, you lazy schmuck
"""


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    update_status = world.update_position(steps)
    if update_status == "safe":
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    elif update_status == "unsafe":
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'
    elif update_status == "obstacle":
        return True, ''+robot_name+': Sorry, there is an obstacle in the way.'


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    update_status = world.update_position(-steps)
    if update_status == "safe":
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    elif update_status == "unsafe":
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'
    elif update_status == "obstacle":
        return True, ''+robot_name+': Sorry, there is an obstacle in the way.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    world.do_right()
    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    world.do_left()

    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)


def get_replay_range(flags):
    """Gets the range of commands to be replayed

    Args:
        flags (string): all flags in a string format


    Returns:
        list: the range of the commands to be played ex. [2, 3]
    """
    flags = flags.split()
    command_range = list(filter(lambda x: re.match("^(\d+|\d+-\d+)$", x), flags))
    hist_len = len(filter_command_history())

    if not command_range:
        return [0, hist_len]
    if "-" in command_range[0]:
        command_range = command_range[0].split("-")
        return [hist_len - int(command_range[0]), hist_len - int(command_range[1])]
    elif command_range[0]:
        return [hist_len - int(command_range[0]), hist_len]


def filter_command_history():
    """
    Returns a filtered version of the command history tracked 
    in the global variable command_history.
    It is filtered by the global variable recorded_commands which contains 
    all commands that is supposed to be played in the reversed command.
    """
    return list(filter(lambda x: x.split()[0] in recorded_commands, command_history))


def do_replay(robot_name, flags):
    """
    replays a filtered version of commands stored in the command_history variable
    """
    silent = "silent" in flags.split()
    reverse = "reversed" in flags.split()
    replay_range = get_replay_range(flags)  #always a list with 2 elements, used in line 272
    new_history = filter_command_history()
    
    replay_range[0] = 0 if replay_range[0] < 0 else replay_range[0]     #checks if the replay_range is
    replay_range[1] = 0 if replay_range[1] < 0 else replay_range[1]     #in range of the actual command_history list

    if reverse:
        new_history.reverse()

    for i in range(replay_range[0], replay_range[1]):
        handle_command(robot_name, new_history[i], silent)
    
    silent_text = (" silently" if silent else "")
    reversed_text = (" in reverse" if reverse else "")
    return True, " > " + robot_name + " replayed " + str(replay_range[1] - replay_range[0]) + " commands" + reversed_text + silent_text + "."


def correct_replay_flags(flags):
    """checks if all flags in "flags" are valid flags for the replay command

    Args:
        flags string: string of args seperated by spaces

    Returns:
        boolean: True if it is a valid argument for the replay command else False
    """
    range_count = 0
    for flag in flags.split():
        if not re.match("^(silent|reversed|\d+|\d+-\d+)$", flag):
            return False
        if re.match("^(\d+|\d+-\d+)$", flag):
            range_count += 1
        if re.match("^(\d+-\d+)$", flag):
            if int(flag.split("-")[0]) < int(flag.split("-")[1]):
                return False
    if range_count > 1:
        return False
    if len(flags.split()) != len(set(flags.split())):
        return False
    return True


def get_valid_positions(pos, maze):
    """
    Used to the maze
    Makes a list of all valid directions to move in
    or returns true and the endpoint if the endpoint is found

    Args:
        pos (Tuple): Current position of mazerunner
        maze (List): Two dimentional array representing the maze
                    See get_maze in the world files

    Returns:
        Boolean: True if the endpoint was found else False
        List: List of all valid positions to move towards/end point
    """
    valid_positions = []
    if maze[pos[0]][pos[1] + 1] == 2:
        return True, (pos[0], pos[1] + 1)
    if maze[pos[0] + 1][pos[1]] == 2:
        return True, (pos[0] + 1, pos[1])
    if maze[pos[0]][pos[1] - 1] == 2:
        return True, (pos[0] - 1, pos[1])
    if maze[pos[0] - 1][pos[1]] == 2:
        return True, (pos[0], pos[1] - 1)

    if maze[pos[0]][pos[1] + 1] == 0:
        valid_positions.append((pos[0], pos[1] + 1))
    if maze[pos[0] + 1][pos[1]] == 0:
        valid_positions.append((pos[0] + 1, pos[1]))
    if maze[pos[0]][pos[1] - 1] == 0:
        valid_positions.append((pos[0], pos[1] - 1))
    if maze[pos[0] - 1][pos[1]] == 0:
        valid_positions.append((pos[0] - 1, pos[1]))

    return False, valid_positions


def find_end(pos, maze):
    """
    Function that drives most of the maze solving

    This function uses the idea of Breadth First Search(BFS)
    to search for the end point and track the steps getting there.
    It tracks the steps by storing the position of the 
    node it came from in each node which can be used
    to step back from the last node to the first.

    Args:
        pos (Tuple): Position it should start solving the mazr
        maze (List): Two dimentional array representing the maze
                     See get_maze in the world files

    Returns:
        Tuple: The end point used to track nodes all 
        the way back to the start
        List: Solved version of the maze
    """
    current_positions = []
    current_positions.append(pos)
    end = False

    while True:
        end, valid_positions = get_valid_positions(current_positions[0], maze)
        if end == True:
            maze[valid_positions[0]][valid_positions[1]] = current_positions[0]
            return current_positions[0], maze
        for valid_position in valid_positions:    
            maze[valid_position[0]][valid_position[1]] = current_positions[0]
            current_positions.append((valid_position[0], valid_position[1]))
        current_positions.pop(0)


def next_node_direction(maze, pos):
    """
    Used to step through the maze
    Gets the direction in which the 
    next cell in the path lays

    Args:
        maze (List): See get maze in the worlds modules
        pos (Tuple): Position to check from

    Returns:
        Integer: The direction the next cell lays in
    """
    if maze[pos[0]][pos[1] + 1] == 4:
        return 0
    if maze[pos[0] + 1][pos[1]] == 4:
        return 1
    if maze[pos[0]][pos[1] - 1] == 4:
        return 2
    if maze[pos[0] - 1][pos[1]] == 4:
        return 3


def next_node_in_direction(pos):
    """Used to make the commands used to solve the maze

    Args:
        pos (Tuple): (x, y, direction) Position to work from

    Returns:
        Tuple: Position in the direction that pos is facing
    """
    if pos[2] == 0:
        return (pos[0], pos[1] + 1)
    if pos[2] == 1:
        return (pos[0] + 1, pos[1])
    if pos[2] == 2:
        return (pos[0], pos[1] - 1)
    if pos[2] == 3:
        return (pos[0] - 1, pos[1])


def get_turn_commands(maze, pos):
    """
    Used to generate commands to solve the maze
    Determines the direction to turn to next
    and returns the appropriate command/s that will do so

    Args:
        maze (List): See get_maze in world modules
        pos (Tuple): Position to look from

    Returns:
        List: List of command/s to achieve 
              the next desired direction
        Integer: Direction the runner will face
    """
    next_direction = next_node_direction(maze, pos)
    if pos[2] == next_direction:
        return [], pos[2]
    elif (pos[2] + 1) % 4 == next_direction:
        return ["right"], (pos[2] + 1) % 4
    elif (pos[2] - 1) % 4 == next_direction:
        return ["left"], (pos[2] - 1) % 4
    else:
        return ["right", "right"], (pos[2] + 2) % 4


def get_forward_commands(maze, pos):
    """
    Determines the range to move next
    and returns the appropriate command/s that will do so

    Args:
        maze (List): See get_maze in word modules
        pos (Tuple): Position to check from

    Returns:
        List[string]: Command/s used to move the 
                      runner a certain distance
        Tuple: Position after the runner moved a 
               certain distance
    """
    count = 0
    next_node = next_node_in_direction(pos)
    while maze[next_node[0]][next_node[1]] == 4:
        pos[0] = next_node[0]
        pos[1] = next_node[1]
        count += 1
        maze[next_node[0]][next_node[ 1]] = 0
        next_node = next_node_in_direction(pos)
    return [f"forward " + str(count)], pos


def generate_commands(maze, pos, end):
    """
    Compile a list of commands that can be used
    by the robot to run through the maze

    Args:
        maze (List): See get_maze in world modules
        pos (Tuple): Position to start generating from
        end (Tuple): Position to end walking

    Returns:
        List: The list of commands the should be run to finish the maze
    """
    commands = []
    while(pos[0] != end[0] or pos[1] != end[1]):
        turn_commands, pos[2] = get_turn_commands(maze, pos)
        commands += turn_commands
        forward_commands, pos = get_forward_commands(maze, pos)
        commands += forward_commands
    commands += ["forward 1"]
    return commands


def do_mazerun(robot_name, goal):
    """
    Function to start and manage the mazerun process

    - Solves the maze
    - Cleans it up for really fun testing purposes
    - plots "4"'s representing the path
    - Ships the plotted maze of to be turned into 
    upstanding commands that will actually benefit this program
    - Handle said commands
    - Drops mic because this function knows that it is cool

    Args:
        robot_name (String): The name of your robot
        goal (String): The side that is wished to be reached

    Returns:
        String: The output of the function
    """
    pos = world.get_pos()
    goal = "top" if goal == "" else goal
    maze = world.get_maze(goal)
    print(f"> {robot_name} starting maze run..")

    end, pathed_maze = find_end((pos[0] + 101, pos[1] + 201), maze)

    maze = world.get_maze(goal)
    pathed_maze[pos[0] + 101][pos[1] + 201] = 3
    current = end
    pointer = pathed_maze[end[0]][end[1]]
    while True:
        if pointer == 3:
            break
        maze[current[0]][current[1]] = 4
        current = pointer
        pointer = pathed_maze[pointer[0]][pointer[1]]

    maze[pos[0] + 101][pos[1] + 201] = 5

    solving_commands = generate_commands(maze, [current[0], current[1], pos[2]], end)
    for command in solving_commands:
        handle_command(robot_name, command)
    return True, f"{robot_name}: I am at the {goal} edge."


def handle_command(robot_name, command, silent = False):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """

    (command_name, arg) = split_command_input(command)

    if command_name == 'off':
        return False
    elif command_name == 'help':
        (do_next, command_output) = do_help()
    elif command_name == 'forward':
        (do_next, command_output) = do_forward(robot_name, int(arg))
    elif command_name == 'back':
        (do_next, command_output) = do_back(robot_name, int(arg))
    elif command_name == 'right':
        (do_next, command_output) = do_right_turn(robot_name)
    elif command_name == 'left':
        (do_next, command_output) = do_left_turn(robot_name)
    elif command_name == 'sprint':
        (do_next, command_output) = do_sprint(robot_name, int(arg))
    elif command_name == 'replay':
        (do_next, command_output) = do_replay(robot_name, arg)
    elif command_name == 'mazerun':
        (do_next, command_output) = do_mazerun(robot_name, arg)

    if not silent:
        print(command_output)
        world.show_position(robot_name)
    return do_next


def robot_start():
    """This is the entry point for starting my robot"""

    global command_history

    command_history = []

    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")

    world.setup_world(robot_name)

    command = get_command(robot_name)
    command_history.append(command)
    while handle_command(robot_name, command):
        command = get_command(robot_name)
        command_history.append(command)

    output(robot_name, "Shutting down..")


if __name__ == "__main__":
    robot_start()

