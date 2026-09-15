from gpiozero import Motor, AngularServo
import config

try:
    steer_servos = {
        'FLA': AngularServo(8, min_angle=-90, max_angle=90, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
        'FRA': AngularServo(9, min_angle=-90, max_angle=90, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
        'RLA': AngularServo(10, min_angle=-90, max_angle=90, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
        'RRA': AngularServo(11, min_angle=-90, max_angle=90, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    }

    drive_motors = {
        'FLS': Motor(forward=18, backward=19, enable=4), #IN1 -> forward, IN2 -> backward
        'FRS': Motor(forward=20, backward=21, enable=5),
        'RLS': Motor(forward=22, backward=23, enable=6),
        'RRS': Motor(forward=24, backward=25, enable=7)
    }
except:
    print("GPIOZero not available. Running in simulation mode.")
    steer_servos = {
        'FLA': None,
        'FRA': None,
        'RLA': None,
        'RRA': None
    }

    drive_motors = {
        'FLS': None,
        'FRS': None,
        'RLS': None,
        'RRS': None
    }

def set_steer_angle(name, angle_deg):
    angle_deg = max(-config.MAX_STEER, min(config.MAX_STEER, angle_deg))
    steer_servos[name].angle = angle_deg

def set_motor_speed(name, speed):
    speed = max(-config.MAX_SPEED, min(config.MAX_SPEED, speed))
    drive_motors[name].value = speed


def update(commands):
    set_steer_angle('FLA', commands['FLA'])
    set_steer_angle('FRA', commands['FRA'])
    set_steer_angle('RLA', commands['RLA'])
    set_steer_angle('RRA', commands['RRA'])
    set_motor_speed('FLS', commands['FLS'])
    set_motor_speed('FRS', commands['FRS'])
    set_motor_speed('RLS', commands['RLS'])
    set_motor_speed('RRS', commands['RRS'])

def display(commands):
    print()
    for motor in commands:
        print(f"{motor}: {commands[motor]:.2f}")