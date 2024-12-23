from collections import deque
from pathlib import Path
from typing import Any

example = '''029A
    980A
    179A
    456A
    379A'''
example = example.split()

def find_button(button: Any, keypad: list[list[Any]]) -> tuple[int, int]:
    print('finding', button)
    for y, row in enumerate(keypad):
        for x, location in enumerate(row):
            if str(location) == button:
                return (x,y)

def move_to_button(actuator_pos: tuple[int, int],
                   button_loc: tuple[int, int],
                   keypad: list[list[Any]]
                   ) -> list[str]:
    x, y = actuator_pos

    movements = []
    while True:
        delta_x = button_loc[0] - x
        delta_y = button_loc[1] - y
        print('actuator', keypad[y][x])
        if delta_x > 0: # No empty gaps on the right
            movements.append('>')
            x += 1
            delta_x -= 1
        elif delta_x < 0 and keypad[y][x-1] is not None:
            movements.append('<')
            x -= 1
            delta_x += 1
        elif delta_y > 0 and keypad[y+1][x] is not None:
            movements.append('v')
            y += 1
            delta_y -= 1
        elif delta_y < 0 and keypad[y-1][x] is not None:
            movements.append('^')
            y -= 1
            delta_y += 1
        else: # Arrived at the button
            movements.append('A')
            break
    
    return movements

def press_button(button, keypad, actuator_pos):
    button_loc = find_button(button, keypad)
    print('move', actuator_pos, button_loc, keypad)
    movements = move_to_button(actuator_pos, button_loc, keypad)

    return movements, button_loc

def process_sequence(code, keypads, actuators):
    current_buttons = list(code)

    for i, keypad in enumerate(keypads):
        actuator_pos = actuators[i]
        next_buttons = []
        for button in current_buttons:
            movements, button_loc = press_button(button, keypad, actuator_pos)
            # Update actuator location
            actuator_pos = button_loc
            next_buttons += movements
        print('current', current_buttons, next_buttons)
        current_buttons = next_buttons[:]
        # Update final actuator location in dictionary
        actuators[i] = button_loc

    return current_buttons, actuators

def calculate_complexity(code: str, sequence: list[str]):
    numeric_code = ('').join([char for char in code if char.isdigit()])

    print('complexity', len(sequence), int(numeric_code))

    return len(sequence) * int(numeric_code)

def run(data, keypads, actuators):
    complexity = 0
    for code in data:
        results, actuators = process_sequence(code, keypads, actuators)
        complexity += calculate_complexity(code, results)

    return complexity

keypad_0 = [[7, 8, 9], [4, 5, 6], [1, 2, 3], [None, 0, 'A']] # Door
keypad_1 = [[None, '^', 'A'], ['<', 'v', '>']] # 3 directional keypads
keypads = [keypad_0] + ([keypad_1] * 2) # Directional keypads have same format

# Position the actuators over the A buttons to start
directional_a = find_button('A', keypad_1)
actuators = {0: find_button('A', keypad_0),
             1: directional_a,
             2: directional_a,
             3: directional_a
             }
print('\n')

# This doesn't give the shortest final sequence but a possible sequence
run(example[:1], keypads, actuators)