import asyncio
import curses
import itertools
import random
import time

from curses_tools import draw_frame, read_controls, get_frame_size

TIC_TIMEOUT = 0.1

async def blink(canvas, row, column, symbol='*'):

    random_delay = random.randint(0, 30)
    for _ in range(random_delay):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, row, column, frames, ship_speed=1):


    max_y, max_x = canvas.getmaxyx()

    dubleframes = [frame for frame in frames for _ in range(2)]

    frames_cycle = itertools.cycle(dubleframes)

    for current_frame in frames_cycle:

        # управление
        rows_direction, columns_direction, space_pressed = read_controls(canvas)


        row += rows_direction * ship_speed
        column += columns_direction * ship_speed

        # получили размер рамки
        frame_rows, frame_cols = get_frame_size(current_frame)


        # зажимаем в рамку
        row = max(1, min(row, max_y - frame_rows - 1))
        column = max(1, min(column, max_x - frame_cols - 1))

        # рисуем кадр
        draw_frame(canvas, row, column, current_frame)

        # ожидаем 1 такт чтобы читать управление максимально часто
        await asyncio.sleep(0)

        # стираем
        draw_frame(canvas, row, column, current_frame, negative=True)


def draw(canvas):

    curses.curs_set(0)


    canvas.nodelay(True)

    max_y, max_x = canvas.getmaxyx()
        

    coroutines = list()
    occupied = set()

    with open('rocket_frame_1.txt', 'r') as f:
        frame_1 = f.read()
    with open('rocket_frame_2.txt', 'r') as f:
        frame_2 = f.read()

    frames = [frame_1, frame_2]

    # корабль
    ship_row = max_y // 2
    ship_col = max_x // 2 - 2 # сдвинули чтобы корабль смотрелся по центру

    # очистим зону от звезд, чтобы не налезали на корабль
    clean_y_range = range(ship_row - 2, ship_row + 10)
    clean_x_range = range(ship_col - 5, ship_col + 10)

    for _ in range(200):
        while True:
            rand_y = random.randint(1, max_y - 2)
            rand_x = random.randint(1, max_x - 2)

            # если уже занято другой звездой
            if (rand_y, rand_x) not in occupied:
                break

        occupied.add((rand_y, rand_x))

        rand_symbol = random.choice(['+', '*', '.', ':'])

        star = blink(canvas, rand_y, rand_x, symbol=rand_symbol)

        coroutines.append(star)

    # выстрел
    laser = fire(canvas, max_y // 2, max_x // 2)
    coroutines.append(laser)

    ship = animate_spaceship(canvas, ship_row, ship_col, frames)
    coroutines.append(ship)

    # игровой движок
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.border() # поставил в цикле иначе дырки в рамке
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':

    curses.update_lines_cols()
    curses.wrapper(draw)