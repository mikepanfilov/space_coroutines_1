# Spaceship Game

An interactive terminal-based space shooter game with smooth animations, keyboard controls. The game 
Spaceship can move freely across the screen fullfiled with beautiful stars.

## How to install

Python 3.6+ should already be installed.

No additional requirements needed at this time.

### Project structure

- `main.py` — main game script with game loop and all coroutines
- `curses_tools.py` — helper functions
- `rocket_frame_1.txt` and `rocket_frame_2.txt` — spaceship animation frames

## How to run

To start the game, execute the following command:

```
python3 main.py
```

## Game controls

- **Arrow Up** — move spaceship up
- **Arrow Down** — move spaceship down
- **Arrow Left** — move spaceship left
- **Arrow Right** — move spaceship right

## How it works

The game is built using Python's `asyncio` library and `curses` for terminal rendering. Stars blink with various brightness levels. Cycles through animation frames while responding to keyboard input.

## Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/)
