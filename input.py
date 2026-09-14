import pygame
import config


inputs = {
    "LX": 0.0,
    "LY": 0.0,
    "RX": 0.0,
    "RY": 0.0,
    "LT": 0.0,
    "RT": 0.0,

    "A": False,
    "B": False,
    "X": False,
    "Y": False,
    "LB": False,
    "RB": False,

    "DU": False,
    "DD": False,
    "DL": False,
    "DR": False
}


axis_map = {
    0: "LX",
    1: "LY",
    2: "RX",
    3: "RY",
    4: "LT",
    5: "RT"
}


button_map = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "LB",
    5: "RB"
}


hat_map = {
    (0, 1): "DU",
    (0, -1): "DD",
    (-1, 0): "DL",
    (1, 0): "DR"
}


joystick = None

def remap(value, in_min=config.DEADZONE, in_max=1.0, out_min=0.0, out_max=1.0):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def sign(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0

def exp(value):
    return 2.718281828459045 ** value

def scale(value, deadzone=config.DEADZONE, scaling=config.SCALING):
    if abs(value) < deadzone:
        return 0.0
    else:
        value = remap(value)
        if scaling > 0:
            value = sign(value) * ((exp(scaling*abs(value)) - 1) / (exp(scaling) - 1))
    return value


def initialise():
    global joystick

    pygame.init()
    pygame.joystick.init()

    while pygame.joystick.get_count() == 0:
        pygame.event.pump()
        print("Waiting for joystick...")
        pygame.time.delay(100)

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick connected.")


def update():
    pygame.event.pump()

    # Axes
    for axis in axis_map:
        if axis in [0, 2]:
            inputs[axis_map[axis]] = scale(joystick.get_axis(axis))
        elif axis in [1, 3]:
            inputs[axis_map[axis]] = -scale(joystick.get_axis(axis)) # Undo inverted y-axis
        elif axis in [4, 5]:
            trigger = (joystick.get_axis(axis) + 1) / 2
            trigger = max(0.0, min(1.0, trigger))

            inputs[axis_map[axis]] = scale(
                trigger,
                deadzone=0.0
            )

    # Buttons
    for button in button_map:
        inputs[button_map[button]] = joystick.get_button(button)

    # D-pad
    hat = joystick.get_hat(0)

    for hat_direction, button in hat_map.items():
        inputs[button] = hat == hat_direction

    return inputs