import os
import random
import time
import msvcrt
import threading
from colorama import init, Fore, Back, Style
colors = {'snake': Fore.YELLOW, 'snake_head': Fore.BLUE, 'food': Fore.GREEN, 'field': '', 'bounds': Back.WHITE}
QUIT = False
NEWGAME = False
PAUSE = False
LOST = False
FIELD_SIZE = 19
SCORE = 0
move_maps = {'w': 0, 'd': 1, 's': 2, 'a': 3}
input_maps = {'q': 5, # Quit program
              'p': 6, # Pause
              'n': 7} # New game
field = [['x' for j in range(0, FIELD_SIZE)] for i in range(0, FIELD_SIZE)]
snake = {'dir': 0, 'body': [], 'old_dir': 0}
food = ()


def show_field(snake_body):
    l_field = [[colors['field']+' ' for j in range(0, FIELD_SIZE)] for i in range(0, FIELD_SIZE)]

    # print snake head
    l_field[snake['body'][0][0]][snake['body'][0][1]] = colors['snake_head']+'o'+colors['field']
    # print snake body
    for part in snake_body[1:]:
        l_field[part[0]][part[1]] = colors['snake']+'o'+colors['field']
    output = colors['field']+Style.BRIGHT
    l_field[food[0]][food[1]] = colors['food']+'F'+colors['field']

    # generating output matrix
    output += '\nSCORE: %s' % SCORE+"\n\n'n' - New Game, 'p' - Pause, 'q' - Quit\n"
    output += '-'*(FIELD_SIZE*2)+'\n'  # too blinky
    for i in range(0, FIELD_SIZE):
        # output += Fore.RESET+Back.RESET + '|' #too blinky
        for j in range(0, FIELD_SIZE):
            output += (l_field[i][j]+' ')
        output += Fore.RESET+Back.RESET + '\n'
        # output += Fore.RESET+Back.RESET + '|\n'   #too blinky
    output += '-'*(FIELD_SIZE*2+1)
    print output


def initialize_snake(l_snake):
    l_snake['body'] = [[FIELD_SIZE/2-2, FIELD_SIZE/2], [FIELD_SIZE/2-1, FIELD_SIZE/2], [FIELD_SIZE/2-2, FIELD_SIZE/2]]
    l_snake['dir'] = 0


def make_move(l_snake):
    global SCORE
    global LOST
    new_element = l_snake['body'][0][:]

    # check if snake is trying to turn 180 degrees
    if abs(l_snake['dir'] - l_snake['old_dir']) == 2:
        snake['dir'] = snake['old_dir']

    # create next place for head
    if l_snake['dir'] == 0:
        new_element[0] -= 1
    elif l_snake['dir'] == 1:
        new_element[1] += 1
    elif l_snake['dir'] == 2:
        new_element[0] += 1
    elif l_snake['dir'] == 3:
        new_element[1] -= 1

    # teleport if bounds of field are reached
    if new_element[0] < 0:
        new_element[0] = FIELD_SIZE-1
    elif new_element[0] > FIELD_SIZE-1:
        new_element[0] = 0
    elif new_element[1] < 0:
        new_element[1] = FIELD_SIZE-1
    elif new_element[1] > FIELD_SIZE-1:
        new_element[1] = 0

    # add new head and possibly remove tail
    l_snake['body'].insert(0, new_element)
    if new_element[0] == food[0] and new_element[1] == food[1]:
        SCORE += 10
        generate_food(l_snake['body'])
    else:
        del l_snake['body'][-1]

    # check for snake collision
    if check_collision(l_snake):
        LOST = True
    snake['old_dir'] = snake['dir']


def check_input(l_snake):
    global QUIT
    global PAUSE
    global NEWGAME
    global LOST
    inp = ''
    while True:
        while msvcrt.kbhit():
            inp = msvcrt.getch()
        if inp in move_maps:
            l_snake['dir'] = move_maps[inp]
        elif inp in input_maps:
            if input_maps[inp] == 5:
                QUIT = True
            elif input_maps[inp] == 6:
                PAUSE = not PAUSE
            elif input_maps[inp] == 7:
                NEWGAME = True
                LOST = False
                PAUSE = False
                print 'New game pressed'
        inp = ''


def initialize_keyboard():
    t = threading.Thread(target=check_input, args=(snake,))
    t.daemon = True
    t.start()


def check_collision(l_snake):
    head = l_snake['body'][0]
    # print 'snake: ' + str(snake['body'])
    for element in l_snake['body'][1:]:
        if element[0] == head[0] and element[1] == head[1]:
            return True
    return False


def generate_food(snake):
    global food
    flag = True
    collision = False

    while flag:
        el = [random.randrange(0, FIELD_SIZE), random.randrange(0, FIELD_SIZE)]
        for element in snake:
            if element[0] == el[0] and element[0] == el[1]:
                collision = True
        if not collision:
            flag = False
    food = el


initialize_keyboard()

while not QUIT:
    NEWGAME = False
    initialize_snake(snake)
    generate_food(snake['body'])
    init()
    while not NEWGAME:
        os.system('cls')
        make_move(snake)
        show_field(snake['body'])

        if LOST:
            print 'YOU LOST! Press n to start new Game'
            while LOST:
                1
        if QUIT:
            break

        if PAUSE:
            print 'PAUSE PRESSED'
            while PAUSE and not QUIT:
                1
        time.sleep(0.3)





