from msvcrt import getch
import os
import threading
import time
import random
from Point import Point
from colorama import Fore, Style, Back

clear = lambda: os.system('cls')

MAX_X = 20
MAX_Y = 20

# All set in main
direction = None
direction_list = None
# 0 = Clear
# 1 = Tail
# 2 = Head
# 3 = Coin
Matrix = None
length = None
body_positions = None
head_position = None


def keypress():
    global direction
    while True:
        key = ord(getch())
        if key == 224:
            key = ord(getch())
            if key == 80:
                # Down arrow
                if length > 0 and direction_list is not None and not len(direction_list) > 0:
                    next_position = head_position.copy()
                    next_position.y += 1
                    if next_position.x == body_positions[0].x and next_position.y == body_positions[0].y:
                        # Bad, this means we will run into ourself right away.
                        continue
                direction_list.append('down')
            elif key == 72:
                # Up arrow
                if length > 0 and direction_list is not None and not len(direction_list) > 0:
                    next_position = head_position.copy()
                    next_position.y -= 1
                    if next_position.x == body_positions[0].x and next_position.y == body_positions[0].y:
                        # Bad, this means we will run into ourself right away.
                        continue
                direction_list.append('up')
            elif key == 77:
                # Right arrow
                if length > 0 and direction_list is not None and not len(direction_list) > 0:
                    next_position = head_position.copy()
                    next_position.x += 1
                    if next_position.x == body_positions[0].x and next_position.y == body_positions[0].y:
                        # Bad, this means we will run into ourself right away.
                        continue
                direction_list.append('right')
            elif key == 75:
                # Lets Arrow
                if length > 0 and direction_list is not None and not len(direction_list) > 0:
                    next_position = head_position.copy()
                    next_position.x -= 1
                    if next_position.x == body_positions[0].x and next_position.y == body_positions[0].y:
                        # Bad, this means we will run into ourself right away.
                        continue
                direction_list.append('left')


def print_game():
    clear()
    game_str = ''
    #game_str += Fore.LIGHTGREEN_EX + '\t\tPySnake by @hunter_bdm\n'

    for y in range(0, len(Matrix)):
        for x in range(0, len(Matrix[y])):
            if Matrix[x][y] == 0:
                # Nothing here
                game_str += Back.RED + '  ' + Style.RESET_ALL
            elif Matrix[x][y] == 1:
                # Body here
                game_str += Back.GREEN + '  ' + Style.RESET_ALL
            elif Matrix[x][y] == 2:
                # Head here
                game_str += Back.LIGHTCYAN_EX + '  ' + Style.RESET_ALL
            elif Matrix[x][y] == 3:
                game_str += Back.CYAN + '  ' + Style.RESET_ALL
        game_str += '\n'

    print(game_str)


def main():
    global direction
    global direction_list
    global Matrix
    global length
    global body_positions
    global head_position

    # The keypress must be in a different thread
    t = threading.Thread(target=keypress)
    t.daemon = True
    t.start()
    while True:
        direction = None
        direction_list = []
        # 0 = Clear
        # 1 = Tail
        # 2 = Head
        # 3 = Coin
        Matrix = [[0 for x in range(MAX_X)] for y in range(MAX_Y)]
        length = 0
        body_positions = []
        head_position = Point(0, 0)
        print_game()
        main_loop()


def add_coin():
    global Matrix
    rand_x = random.randrange(0, MAX_X)
    rand_y = random.randrange(0, MAX_Y)
    while True:
        if not Matrix[rand_x][rand_y] == 0:
            rand_x = random.randrange(0, MAX_X)
            rand_y = random.randrange(0, MAX_Y)
        else:
            break
    Matrix[rand_x][rand_y] = 3


def main_loop():
    global direction
    global Matrix
    global length

    add_coin()
    while True:
        # Get direction
        if not len(direction_list) == 0:
            direction = direction_list[0]
            direction_list.remove(direction)

        prev = head_position.copy()
        if direction == 'down':
            head_position.y += 1
        elif direction == 'up':
            head_position.y -= 1
        elif direction == 'right':
            head_position.x += 1
        elif direction == 'left':
            head_position.x -= 1
        # Check if out of bounds or if hit body
        if head_position.x >= MAX_X or head_position.y >= MAX_Y or Matrix[head_position.x][head_position.y] == 1:
            a = input('GAME OVER\nPress enter to play again.')
            return

        # Check if head is on coin
        if Matrix[head_position.x][head_position.y] == 3:
            for i in range(0, 5):
                body_positions.append((body_positions[-1] if length > 0 else head_position))
            add_coin()
        # Move body
        added = False
        if len(body_positions) > length:
            added = True
            length += 1
        for i in range(0, length):
            hold = body_positions[i]
            body_positions[i] = prev
            prev = hold
        # If we did not add to the body we need to clear the last block
        if not added:
            Matrix[prev.x][prev.y] = 0
        # Draw Body
        for position in body_positions:
            Matrix[position.x][position.y] = 1

        Matrix[head_position.x][head_position.y] = 2

        if head_position.x > MAX_X or head_position.x < 0:
            input('GAME OVER\nPress enter to play again.')
            return
        if head_position.y > MAX_Y or head_position.y < 0:
            input('GAME OVER\nPress enter to play again.')
            return

        print_game()
        time.sleep(0.09)


if __name__ == '__main__':
    main()
