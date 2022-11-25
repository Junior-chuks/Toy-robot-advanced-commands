"""
TODO: You can either work from this skeleton, or you can build on your solution for Toy Robot 2 exercise.
"""


# list of valid command names
valid_commands = ['off', 'help', 'forward', 'back', 'right', 'left', 'sprint', "replay", "silent", "reversed"]

# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100

# list of historical commands
hist_lis = []



def get_robot_name():
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


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


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """
    com = command.split()
    (command_name, arg1) = split_command_input(command)
    new = arg1.split()
    special_char = arg1.split("-")
    reverse_with_num = arg1.split()

    return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1) or (is_int(special_char[0]) and is_int(special_char[1]))  or arg1.lower() in valid_commands or (len(new)==2 and new[0].lower()== "reversed" or (is_int(reverse_with_num[0]) and str(reverse_with_num[1]))))


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
"""


def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


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

    if is_position_allowed(new_x, new_y):
        position_x = new_x
        position_y = new_y
        return True
    return False


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    if update_position(steps):
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """

    if update_position(-steps):
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global current_direction_index

    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0

    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global current_direction_index

    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3

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

    
def replay_command(name,com):
    """
    Runs all types of replay function\commands
    """

    number = number_locator(com)
    lis =command_history(com,number) 
    lis_len = len(lis)
    
    if "replay" == com:
        n = [handle_command(name,i,"") for i in lis]
        print(f" > {name} replayed {lis_len} commands.")
        show_position(name)
        return n

    elif f"replay {number[0]}" == com :
        leng_0 =len(lis)
        m = lis[leng_0-int(number[0]):]
        leng_1 =len(m)
        b = [handle_command(name,i,"") for i in m][0]
        print(f" > {name} replayed {leng_1} commands.")
        show_position(name)
        return b
    
    elif f"replay {number[0]}-{number[1]}" == com :
        leng_0 =len(lis)
        k = lis[leng_0-int(number[0]):leng_0-1]
        leng_2 =len(k)
        c = [handle_command(name,i,"") for i in k][0]
        print(f" > {name} replayed {leng_2} commands.")
        show_position(name)
        return c
            
    elif "replay silent" == com or f"replay {number[0]} silent" == com:
        return replay_silent(name,com,number)
    
    elif "replay reversed" == com or f"replay {number[0]} reversed" == com:
        return replay_reversed(name,com,number)

    elif "replay reversed silent" == com:
        return replay_reversed_silent(name,com,number)


def replay_reversed_silent(name,com,num):
    """
    Replays reversed commands without displaying information about its movement
    but displays its final position.
    """
    
    lis =command_history(com,num) 
    lis_len = len(lis)
    lis.reverse()
    n_2 = [handle_command(name,i,"silent") for i in lis]
    print(f" > {name} replayed {lis_len} commands in reverse silently.")
    show_position(name)
    return n_2

    
def replay_silent(name,com,num):
    """Replays commands and displays only the final destination."""

    lis =command_history(com,num) 
    lis_len = len(lis)

    if "replay silent" == com:
        n_1 = [handle_command(name,i,"silent") for i in lis]
        print(f" > {name} replayed {lis_len} commands silently.")
        show_position(name)
        return n_1
    
    else:
        leng_0 =len(lis)
        j = lis[leng_0-int(num[0]):]
        leng_1 =len(j)
        lis =command_history(com,num) 
        lis_len = len(lis)
        n_1 = [handle_command(name,i,"silent") for i in j]
        print(f" > {name} replayed {leng_1} commands silently.")
        show_position(name)
        return n_1


def replay_reversed(name,com,num):
    """
    Replays commands in reverse.
    """

    if "replay reversed" == com:
        lis =command_history(com,num) 
        lis_len = len(lis)
        lis.reverse()
        n = [handle_command(name,i,"") for i in lis]
        print(f" > {name} replayed {lis_len} commands in reverse.")
        show_position(name)
        return n
    
    else:
        lis =command_history(com,num) 
        leng_0 =len(lis)
        lis.reverse()
        m = lis[leng_0-int(num[0]):]
        leng_1 =len(m)
        n = [handle_command(name,i,"") for i in m]
        print(f" > {name} replayed {leng_1} commands in reverse.")
        show_position(name)
        return n


def handle_command(robot_name, command,default):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """
    global command_output
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
    elif command_name == "replay":
        return  replay_command(robot_name,command)
    
        
    if len(default) == 0 :
        print(command_output)
        show_position(robot_name)
    return do_next


def command_history(commands,number):
    """
    Stores commands in a list.
    """

    x =[True if i in commands else False for i in valid_commands]
    word =["replay","replay silent","replay reversed","replay reversed silent",f"replay {number[0]}", f"replay {number[0]}-{number[1]}",f"replay {number[0]} reversed",f"replay {number[0]} silent"]
    if commands not in word and x :
        hist_lis.append(commands)
        return hist_lis
    
    else:
        return hist_lis


def number_locator(command):
    """
    Retrieves number from commands and returns them.
    """
    number =''
    if "-" in command:
        for i in command:
            if i.isdigit() == True or i == "-":
                number+=i
        n = number.split("-")
        return n
    else:
        for i in command:
            if i.isdigit() == True:
                number+=i
        return [number,""]
   

def robot_start():
    """This is the entry point for starting my robot"""

    global position_x, position_y, current_direction_index, hist_lis

    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")

    position_x = 0
    position_y = 0
    current_direction_index = 0
    

    command = get_command(robot_name)
    num_1 = number_locator(command)
    command_history(command,num_1)
    while handle_command(robot_name, command,""):
        command = get_command(robot_name)
        num = number_locator(command)
        hist_lis=command_history(command,num)
        
    hist_lis.clear()
    output(robot_name, "Shutting down..")


if __name__ == "__main__":
    robot_start()
    
