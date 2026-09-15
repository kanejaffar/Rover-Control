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
keyboard_window = None


keyboard_axis_map = {
    "LX": ((pygame.K_d,), (pygame.K_a,)),
    "LY": ((pygame.K_w,), (pygame.K_s,)),
    "RX": ((pygame.K_RIGHT,), (pygame.K_LEFT,)),
    "RY": ((pygame.K_UP,), (pygame.K_DOWN,)),
    "RT": ((pygame.K_e, pygame.K_l), ()),
    "LT": ((pygame.K_q, pygame.K_j), ())
}


keyboard_button_map = {
    "A": (pygame.K_g, pygame.K_z),
    "B": (pygame.K_h, pygame.K_c),
    "X": (pygame.K_t, pygame.K_x),
    "Y": (pygame.K_y, pygame.K_v),
    "LB": (pygame.K_1, pygame.K_8),
    "RB": (pygame.K_3, pygame.K_0)
}

def deadzone(value, in_min=config.DEADZONE, in_max=1.0, out_min=0.0, out_max=1.0):
    magnitude = abs(value)

    if magnitude <= in_min:
        return 0.0

    magnitude = (magnitude - in_min) / (in_max - in_min)
    magnitude = max(0.0, min(1.0, magnitude))
    magnitude = magnitude * (out_max - out_min) + out_min

    return sign(value) * magnitude

def sign(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0

def exp(value):
    return 2.718281828459045 ** value

def scale(value):
    if config.SCALING > 0:
        value = sign(value) * ((exp(config.SCALING*abs(value)) - 1) / (exp(config.SCALING) - 1))
    return value


def _show_keyboard_window():
    global keyboard_window

    if keyboard_window is None:
        pygame.display.set_caption("Rover Control - Keyboard")
        keyboard_window = pygame.display.set_mode((320, 100))


def _hide_keyboard_window():
    global keyboard_window

    if keyboard_window is not None:
        pygame.display.quit()
        keyboard_window = None


def initialise():
    global joystick

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        _hide_keyboard_window()
        print("Joystick connected.")
    else:
        _show_keyboard_window()
        print("No joystick connected. Using keyboard.")


def _update_joystick_connection():
    global joystick

    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0 and joystick is not None:
        joystick.quit()
        joystick = None
        _show_keyboard_window()
        print("Joystick disconnected. Using keyboard.")
    elif joystick_count > 0 and joystick is None:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        _hide_keyboard_window()
        print("Joystick connected. Using controller.")


def _keyboard_inputs():
    keys = pygame.key.get_pressed()

    for name, (positive_keys, negative_keys) in keyboard_axis_map.items():
        positive = any(keys[key] for key in positive_keys)
        negative = any(keys[key] for key in negative_keys)
        inputs[name] = float(positive) - float(negative)

    for name, keys_for_button in keyboard_button_map.items():
        inputs[name] = any(keys[key] for key in keys_for_button)

    for name in hat_map.values():
        inputs[name] = False

    return inputs


def update():
    if pygame.display.get_init():
        pygame.event.pump()

    _update_joystick_connection()

    if joystick is None:
        return _keyboard_inputs()

    # Axes
    for axis in axis_map:
        if axis in [0, 2]:
            inputs[axis_map[axis]] = scale(deadzone(joystick.get_axis(axis)))
        elif axis in [1, 3]:
            inputs[axis_map[axis]] = -scale(deadzone(joystick.get_axis(axis))) # Undo inverted y-axis
        elif axis in [4, 5]:
            inputs[axis_map[axis]] = scale(deadzone((joystick.get_axis(axis) + 1) / 2))

        print(f'{inputs[axis_map[axis]]=}')

    # Buttons
    for button in button_map:
        inputs[button_map[button]] = joystick.get_button(button)

    # D-pad
    hat = joystick.get_hat(0)

    for hat_direction, button in hat_map.items():
        inputs[button] = hat == hat_direction

    return inputs