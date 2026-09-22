import gpiod
import config
import threading
import time


# ============================================================
# GPIO configuration
# ============================================================




# ============================================================
# PWM configuration
# ============================================================

SERVO_FREQUENCY = 50
SERVO_PERIOD = 1 / SERVO_FREQUENCY

SERVO_MIN_US = 500
SERVO_MAX_US = 2500


MOTOR_FREQUENCY = 500
MOTOR_PERIOD = 1 / MOTOR_FREQUENCY


# ============================================================
# State
# ============================================================

angles = {
    "FLA": 0,
    "FRA": 0,
    "RLA": 0,
    "RRA": 0,
}

speeds = {
    "FLS": 0,
    "FRS": 0,
    "RLS": 0,
    "RRS": 0,
}


# ============================================================
# Find GPIO chip
# ============================================================

def find_gpio_chip():

    for i in range(10):

        try:
            chip = gpiod.Chip(f"/dev/gpiochip{i}")
            info = chip.get_info()

            if "bcm2835" in info.name.lower() or "rp1" in info.name.lower():
                return chip

            chip.close()

        except OSError:
            pass

    raise RuntimeError("Could not find Raspberry Pi GPIO chip")


GPIO_CHIP = find_gpio_chip()


# ============================================================
# Convert steering angle to servo pulse width
# ============================================================

def angle_to_pulse(angle):

    angle = max(-90, min(90, angle))

    return (
        SERVO_MIN_US
        + (angle + 90) / 180
        * (SERVO_MAX_US - SERVO_MIN_US)
    )


# ============================================================
# Set requested values
# ============================================================

def set_steer_angle(name, angle):

    angle = max(-config.MAX_STEER,
                min(config.MAX_STEER, angle))

    angles[name] = angle


def set_motor_speed(name, speed):

    speed = max(-config.MAX_SPEED,
                min(config.MAX_SPEED, speed))

    speeds[name] = speed


# ============================================================
# Servo PWM
# ============================================================

def servo_pwm():

    pins = list(config.STEERING_PINS.values())

    settings = gpiod.LineSettings(
        direction=gpiod.line.Direction.OUTPUT,
        output_value=gpiod.line.Value.INACTIVE
    )

    request = GPIO_CHIP.request_lines(
        consumer="rover-servo",
        config={tuple(pins): settings}
    )

    next_cycle = time.monotonic_ns()

    while True:

        # Start of 20 ms servo frame
        next_cycle += int(SERVO_PERIOD * 1e9)

        for name, pin in config.STEERING_PINS.items():

            pulse_us = angle_to_pulse(angles[name])
            pulse_time = pulse_us / 1_000_000

            request.set_value(
                pin,
                gpiod.line.Value.ACTIVE
            )

            time.sleep(pulse_time)

            request.set_value(
                pin,
                gpiod.line.Value.INACTIVE
            )

        # Wait for next frame
        remaining = next_cycle - time.monotonic_ns()

        if remaining > 0:
            time.sleep(remaining / 1e9)


# ============================================================
# Motor PWM
# ============================================================

def motor_pwm():

    pins = []

    for in1, in2, enable in config.MOTOR_PINS.values():
        pins.extend([in1, in2, enable])

    settings = gpiod.LineSettings(
        direction=gpiod.line.Direction.OUTPUT,
        output_value=gpiod.line.Value.INACTIVE
    )

    request = GPIO_CHIP.request_lines(
        consumer="rover-motors",
        config={tuple(pins): settings}
    )

    period_ns = int(MOTOR_PERIOD * 1e9)
    next_cycle = time.monotonic_ns()

    while True:

        next_cycle += period_ns

        for name, (in1, in2, enable) in config.MOTOR_PINS.items():

            speed = speeds[name]

            # Direction
            if speed > 0:
                request.set_value(in1, gpiod.line.Value.ACTIVE)
                request.set_value(in2, gpiod.line.Value.INACTIVE)

            elif speed < 0:
                request.set_value(in1, gpiod.line.Value.INACTIVE)
                request.set_value(in2, gpiod.line.Value.ACTIVE)

            else:
                request.set_value(in1, gpiod.line.Value.INACTIVE)
                request.set_value(in2, gpiod.line.Value.INACTIVE)

            # PWM
            duty = abs(speed) / config.MAX_SPEED

            request.set_value(
                enable,
                gpiod.line.Value.ACTIVE
            )

            time.sleep(duty * MOTOR_PERIOD)

            request.set_value(
                enable,
                gpiod.line.Value.INACTIVE
            )

        remaining = next_cycle - time.monotonic_ns()

        if remaining > 0:
            time.sleep(remaining / 1e9)


# ============================================================
# Initialise
# ============================================================

def initialise():

    servo_thread = threading.Thread(
        target=servo_pwm,
        daemon=True
    )

    motor_thread = threading.Thread(
        target=motor_pwm,
        daemon=True
    )

    servo_thread.start()
    motor_thread.start()


# ============================================================
# Main output function
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