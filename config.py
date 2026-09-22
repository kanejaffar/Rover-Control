# Controller settings
DEADZONE = 0.10
SCALING = 2 # 0 = linear, greater number = more exponential

# Scheme settings
SCHEME = 'ACK'

# Motor settings
MAX_STEER = 90
MAX_SPEED = 1.0

# Rover geometry
WIDTH = 78
LENGTH = 101

# Steering servos
STEER_PINS = {
    "FLA": 7,
    "FRA": 5,
    "RLA": 3,
    "RRA": 8
}

# Drive motor pins
MOTOR_PINS = {
    "FLS": (37, 35, 33), #IN1, IN2, EN/PWM
    "FRS": (31, 29, 27),
    "RLS": (23, 21, 19),
    "RRS": (15, 13, 11)
}