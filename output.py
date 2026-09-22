from gpiozero import AngularServo, Motor
import config

steering = {
    "FLA": AngularServo(
        config.STEER_PINS["FLA"],
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    ),

    "FRA": AngularServo(
        config.STEER_PINS["FRA"],
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    ),

    "RLA": AngularServo(
        config.STEER_PINS["RLA"],
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    ),

    "RRA": AngularServo(
        config.STEER_PINS["RRA"],
        min_angle=-90,
        max_angle=90,
        min_pulse_width=0.0005,
        max_pulse_width=0.0025,
        frame_width=0.02
    )
}

motors = {
    "FLS": Motor(
        forward=config.MOTOR_PINS["FLS"][0],
        backward=config.MOTOR_PINS["FLS"][1],
        enable=config.MOTOR_PINS["FLS"][2],
        pwm=True
    ),

    "FRS": Motor(
        forward=config.MOTOR_PINS["FRS"][0],
        backward=config.MOTOR_PINS["FRS"][1],
        enable=config.MOTOR_PINS["FRS"][2],
        pwm=True
    ),

    "RLS": Motor(
        forward=config.MOTOR_PINS["RLS"][0],
        backward=config.MOTOR_PINS["RLS"][1],
        enable=config.MOTOR_PINS["RLS"][2],
        pwm=True
    ),

    "RRS": Motor(
        forward=config.MOTOR_PINS["RRS"][0],
        backward=config.MOTOR_PINS["RRS"][1],
        enable=config.MOTOR_PINS["RRS"][2],
        pwm=True
    )
}

def initialise():

    for servo in steering.values():
        servo.angle = 0

    for motor in motors.values():
        motor.stop()

def set_steer_angle(name, angle):

    angle = max(
        -config.MAX_STEER,
        min(config.MAX_STEER, angle)
    )

    steering[name].angle = angle

def set_motor_speed(name, speed):

    speed = max(
        -config.MAX_SPEED,
        min(config.MAX_SPEED, speed)
    )

    speed = speed / config.MAX_SPEED

    motors[name].value = speed

def update(commands):

    set_steer_angle("FLA", commands["FLA"])
    set_steer_angle("FRA", commands["FRA"])
    set_steer_angle("RLA", commands["RLA"])
    set_steer_angle("RRA", commands["RRA"])

    set_motor_speed("FLS", commands["FLS"])
    set_motor_speed("FRS", commands["FRS"])
    set_motor_speed("RLS", commands["RLS"])
    set_motor_speed("RRS", commands["RRS"])

def shutdown():

    for motor in motors.values():
        motor.stop()

    for servo in steering.values():
        servo.detach()