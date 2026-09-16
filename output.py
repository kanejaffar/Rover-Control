import pigpio
import config


# ---------------------------------------------------------
# GPIO setup
# ---------------------------------------------------------

pi = pigpio.pi()

if not pi.connected:
    print("pigpio not available. Running in simulation mode.")
    pi = None


# ---------------------------------------------------------
# GPIO pins
# ---------------------------------------------------------

STEER_PINS = {
    'FLA': 8, #PWM
    'FRA': 9,
    'RLA': 10,
    'RRA': 11
}

DRIVE_PINS = {
    'FLS': (18, 19, 4), #IN1, IN2, EN
    'FRS': (20, 21, 5),
    'RLS': (22, 23, 6),
    'RRS': (24, 25, 7)
}


# ---------------------------------------------------------
# Servo configuration
# ---------------------------------------------------------

MIN_PULSE_WIDTH = 500
MAX_PULSE_WIDTH = 2500

MIN_SERVO_ANGLE = -90
MAX_SERVO_ANGLE = 90


# ---------------------------------------------------------
# Servo state
# ---------------------------------------------------------

current_angles = {
    'FLA': None,
    'FRA': None,
    'RLA': None,
    'RRA': None
}


# ---------------------------------------------------------
# Convert angle to pulse width
# ---------------------------------------------------------

def angle_to_pulse(angle_deg):

    angle_deg = max(
        MIN_SERVO_ANGLE,
        min(MAX_SERVO_ANGLE, angle_deg)
    )

    pulse_range = MAX_PULSE_WIDTH - MIN_PULSE_WIDTH
    angle_range = MAX_SERVO_ANGLE - MIN_SERVO_ANGLE

    pulse = MIN_PULSE_WIDTH + (
        (angle_deg - MIN_SERVO_ANGLE)
        * pulse_range
        / angle_range
    )

    return int(pulse)


# ---------------------------------------------------------
# Set steering servo angle
# ---------------------------------------------------------

def set_steer_angle(name, angle_deg):

    angle_deg = max(
        -config.MAX_STEER,
        min(config.MAX_STEER, angle_deg)
    )

    # Don't send another command if the angle hasn't changed.
    if (
        current_angles[name] is not None
        and abs(angle_deg - current_angles[name]) < 0.5
    ):
        return

    current_angles[name] = angle_deg

    if pi is None:
        return

    pulse = angle_to_pulse(angle_deg)

    pi.set_servo_pulsewidth(
        STEER_PINS[name],
        pulse
    )


# ---------------------------------------------------------
# Set drive motor speed
# ---------------------------------------------------------

def set_motor_speed(name, speed):

    speed = max(
        -config.MAX_SPEED,
        min(config.MAX_SPEED, speed)
    )

    if pi is None:
        return

    forward_pin, backward_pin, enable_pin = DRIVE_PINS[name]

    # Convert speed to 0.0 - 1.0
    speed_normalised = abs(speed) / config.MAX_SPEED

    # Set direction
    if speed > 0:
        pi.write(forward_pin, 1)
        pi.write(backward_pin, 0)

    elif speed < 0:
        pi.write(forward_pin, 0)
        pi.write(backward_pin, 1)

    else:
        pi.write(forward_pin, 0)
        pi.write(backward_pin, 0)

    # Hardware PWM
    pi.hardware_PWM(
        enable_pin,
        1000,
        int(speed_normalised * 1_000_000)
    )


# ---------------------------------------------------------
# Update all outputs
# ---------------------------------------------------------

def update(commands):

    display(commands)

    try:

        set_steer_angle('FLA', commands['FLA'])
        set_steer_angle('FRA', commands['FRA'])
        set_steer_angle('RLA', commands['RLA'])
        set_steer_angle('RRA', commands['RRA'])

        set_motor_speed('FLS', commands['FLS'])
        set_motor_speed('FRS', commands['FRS'])
        set_motor_speed('RLS', commands['RLS'])
        set_motor_speed('RRS', commands['RRS'])

    except Exception as e:
        print(f'Output error: {e}')


# ---------------------------------------------------------
# Display commands
# ---------------------------------------------------------

def display(commands):

    print()

    for motor in commands:
        print(f"{motor}: {commands[motor]:.2f}")