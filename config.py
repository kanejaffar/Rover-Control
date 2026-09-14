# Controller settings
DEADZONE = 0.10
SCALING = 0 # 0 = linear, greater number = more exponential

# Scheme settings
SCHEME = "ACKERMANN"

# Motor settings
MAX_STEER = 90
MAX_SPEED = 1.0

# Rover geometry
WIDTH = 78
LENGTH = 101

# Steering servos
STEER_PINS = {
    "FLA": 8,
    "FRA": 9,
    "RLA": 10,
    "RRA": 11
}

# Drive motor pins
MOTOR_PINS = {
    "FLS": (18, 19, 4),
    "FRS": (20, 21, 5),
    "RLS": (22, 23, 6),
    "RRS": (24, 25, 7)
}