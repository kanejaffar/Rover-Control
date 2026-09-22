from gpiozero import AngularServo, Motor
import config


# ============================================================
# Steering motors
# ============================================================

steering = {
    "FLA": AngularServo(
        8,
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    ),

    "FRA": AngularServo(
        9,
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    ),

    "RLA": AngularServo(
        10,
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    ),

    "RRA": AngularServo(
        11,
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    )
}


# ============================================================
# Drive motors
# ============================================================

motors = {
    "FLS": Motor(
        forward=18,
        backward=19,
        enable=4,
        pwm=True
    ),

    "FRS": Motor(
        forward=20,
        backward=21,
        enable=5,
        pwm=True
    ),

    "RLS": Motor(
        forward=22,
        backward=23,
        enable=6,
        pwm=True
    ),

    "RRS": Motor(
        forward=24,
        backward=25,
        enable=7,
        pwm=True
    )
}


# ============================================================
# Initialise
# ============================================================

def initialise():

    for servo in steering.values():
        servo.angle = 0

    for motor in motors.values():
        motor.stop()


# ============================================================
# Set steering angle
# ============================================================

def set_steer_angle(name, angle):

    angle = max(
        -config.MAX_STEER,
        min(config.MAX_STEER, angle)
    )

    steering[name].angle = angle


# ============================================================
# Set motor speed
# ============================================================

def set_motor_speed(name, speed):

    speed = max(
        -config.MAX_SPEED,
        min(config.MAX_SPEED, speed)
    )

    # Convert to GPIO Zero's -1 to +1 range
    speed = speed / config.MAX_SPEED

    motors[name].value = speed


# ============================================================
# Update all outputs
# ============================================================

def update(commands):

    set_steer_angle("FLA", commands["FLA"])
    set_steer_angle("FRA", commands["FRA"])
    set_steer_angle("RLA", commands["RLA"])
    set_steer_angle("RRA", commands["RRA"])

    set_motor_speed("FLS", commands["FLS"])
    set_motor_speed("FRS", commands["FRS"])
    set_motor_speed("RLS", commands["RLS"])
    set_motor_speed("RRS", commands["RRS"])


# ============================================================
# Shutdown
# ============================================================

def shutdown():

    for motor in motors.values():
        motor.stop()

    for servo in steering.values():
        servo.detach()