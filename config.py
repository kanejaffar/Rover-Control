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
    "FLA": 4,
    "FRA": 3,
    "RLA": 2,
    "RRA": 14
}

# Drive motor pins
MOTOR_PINS = {
    "FLS": (26, 19, 13), #IN1, IN2, EN/PWM
    "FRS": (6, 5, 0),
    "RLS": (11, 9, 10),
    "RRS": (22, 27, 17)
}