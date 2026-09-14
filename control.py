import config
import math


commands = {
    'FLA': 0,
    'FRA': 0,
    'RLA': 0,
    'RRA': 0,
    'FLS': 0,
    'FRS': 0,
    'RLS': 0,
    'RRS': 0
}


def ackermann(length, width, angle, speed):

    commands = {
        'FLA': 0,
        'FRA': 0,
        'RLA': 0,
        'RRA': 0,
        'FLS': 0,
        'FRS': 0,
        'RLS': 0,
        'RRS': 0
    }

    # Limit inputs to their expected ranges
    angle = max(-1.0, min(1.0, angle))
    speed = max(0.0, min(1.0, speed))


    # ---------------------------------------------------------
    # Straight ahead
    # ---------------------------------------------------------

    if abs(angle) < 1e-6:

        wheel_speed = speed * config.MAX_SPEED

        commands['FLA'] = 0
        commands['FRA'] = 0
        commands['RLA'] = 0
        commands['RRA'] = 0

        commands['FLS'] = wheel_speed
        commands['FRS'] = wheel_speed
        commands['RLS'] = wheel_speed
        commands['RRS'] = wheel_speed

        return commands


    # ---------------------------------------------------------
    # Maximum steering angle of inside wheel
    # ---------------------------------------------------------

    inside_angle = math.radians(
        abs(angle) * config.MAX_STEER
    )


    # ---------------------------------------------------------
    # Turning radius
    # ---------------------------------------------------------

    inside_radius = length / math.tan(inside_angle)


    # ---------------------------------------------------------
    # Outside wheel steering angle
    # ---------------------------------------------------------

    outside_radius = inside_radius + width

    outside_angle = math.atan(
        length / outside_radius
    )


    # ---------------------------------------------------------
    # Steering direction
    # ---------------------------------------------------------

    if angle > 0:

        # RIGHT TURN
        #
        # FR = inside wheel
        # FL = outside wheel

        commands['FRA'] = math.degrees(inside_angle)
        commands['FLA'] = math.degrees(outside_angle)

    else:

        # LEFT TURN
        #
        # FL = inside wheel
        # FR = outside wheel

        commands['FLA'] = -math.degrees(inside_angle)
        commands['FRA'] = -math.degrees(outside_angle)


    # Rear wheels don't steer in this configuration

    commands['RLA'] = 0
    commands['RRA'] = 0


    # ---------------------------------------------------------
    # Wheel path radii
    # ---------------------------------------------------------

    inside_rear_radius = inside_radius
    outside_rear_radius = inside_radius + width

    inside_front_radius = math.sqrt(
        length**2 + inside_rear_radius**2
    )

    outside_front_radius = math.sqrt(
        length**2 + outside_rear_radius**2
    )


    # ---------------------------------------------------------
    # Assign wheel radii
    # ---------------------------------------------------------

    if angle > 0:

        # RIGHT TURN
        #
        # FR and RR are inside
        # FL and RL are outside

        commands['FRS'] = inside_front_radius
        commands['FLS'] = outside_front_radius
        commands['RRS'] = inside_rear_radius
        commands['RLS'] = outside_rear_radius

    else:

        # LEFT TURN
        #
        # FL and RL are inside
        # FR and RR are outside

        commands['FLS'] = inside_front_radius
        commands['FRS'] = outside_front_radius
        commands['RLS'] = inside_rear_radius
        commands['RRS'] = outside_rear_radius


    # ---------------------------------------------------------
    # Normalise wheel speeds
    # ---------------------------------------------------------

    fastest = max(
        commands['FLS'],
        commands['FRS'],
        commands['RLS'],
        commands['RRS']
    )

    speed_scale = (
        speed * config.MAX_SPEED / fastest
    )


    commands['FLS'] *= speed_scale
    commands['FRS'] *= speed_scale
    commands['RLS'] *= speed_scale
    commands['RRS'] *= speed_scale


    return commands


def update(inputs):

    commands = ackermann(
        config.LENGTH,
        config.WIDTH,
        inputs['LX'],
        inputs['RT']
    )

    return commands