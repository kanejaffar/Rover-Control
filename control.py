import config
import math
import time


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


scheme_names = {
    'ACKERMANN': 'ACK',
    'ACK': 'ACK',
    'TRANS': 'TRANS',
    'TRANSLATIONAL': 'TRANS',
    'ROT': 'ROT',
    'ROTATE': 'ROT'
}

scheme = scheme_names.get(config.SCHEME.upper(), 'ACK')


def ackermann(length, width, angle, forward, back):

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

    speed = forward - back

    # Limit inputs to their expected ranges
    angle = max(-1.0, min(1.0, angle))
    speed = max(-1.0, min(1.0, speed))


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


def translational(x_axis, y_axis):
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

    #print(f"x_axis: {x_axis:.2f}")
    #print(f"y_axis: {y_axis:.2f}")

    speed = math.hypot(x_axis, y_axis)
    speed = max(0.0, min(1.0, speed))
    speed = speed * config.MAX_SPEED

    if speed == 0:
        commands['FLA'] = 0
        commands['FRA'] = 0
        commands['RLA'] = 0
        commands['RRA'] = 0

        commands['FLS'] = 0
        commands['FRS'] = 0
        commands['RLS'] = 0
        commands['RRS'] = 0

        return commands
    else:
        direction = math.degrees(math.atan2(y_axis, x_axis))

    #print(f"speed: {speed:.2f}")
    #print(f"direction: {direction:.2f}")

    if direction >= 0 and direction <= 180:
        # Forward
        angle = 90 - direction
    else:
        # Backward
        angle = -90 - direction
        speed = -speed
    

    commands['FLS'] = speed
    commands['FRS'] = speed
    commands['RLS'] = speed
    commands['RRS'] = speed

    commands['FLA'] = angle
    commands['FRA'] = angle
    commands['RLA'] = angle
    commands['RRA'] = angle

    return commands

def rotate(cw, acw):
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

    theta = math.atan(config.LENGTH / config.WIDTH)
    theta = math.degrees(theta)

    commands['FLA'] = theta
    commands['FRA'] = -theta
    commands['RLA'] = -theta
    commands['RRA'] = theta

    cw_result = cw - acw

    commands['FLS'] = cw_result * config.MAX_SPEED
    commands['FRS'] = -cw_result * config.MAX_SPEED
    commands['RLS'] = -cw_result * config.MAX_SPEED
    commands['RRS'] = cw_result * config.MAX_SPEED

    return commands

def tank(move, turn):
    commands = {
        'FLA': 0,
        'FRA': 0,
        'RLA': 0,
        'RRA': 0,
        'FLS': 0,
        'FRS': 0,
        'RLS': 0,
        'RRS': 0,
    }

    if move != 0:
        commands['FLS'] = move*config.MAX_SPEED
        commands['FRS'] = move*config.MAX_SPEED
        commands['RLS'] = move*config.MAX_SPEED
        commands['RRS'] = move*config.MAX_SPEED
    elif turn != 0:
        commands['FLS'] = turn*config.MAX_SPEED
        commands['FRS'] = -turn*config.MAX_SPEED
        commands['RLS'] = turn*config.MAX_SPEED
        commands['RRS'] = -turn*config.MAX_SPEED

    return commands
        




def update(inputs):
    global scheme

    if inputs['A']:
        scheme = 'ACK'
    elif inputs['X']:
        scheme = 'TRANS'
    elif inputs['B']:
        scheme = 'ROT'
    elif inputs['Y']:
        scheme = 'TANK'

    if scheme == 'ACK':
        commands = ackermann(config.LENGTH, config.WIDTH, inputs['LX'], inputs['RT'], inputs['LT'])

    elif scheme == 'TRANS':
        commands = translational(inputs['LX'], inputs['LY'])

    elif scheme == 'ROT':
        commands = rotate(inputs['RT'], inputs['LT'])

    elif scheme == 'TANK':
        commands = tank(inputs['LY'], inputs['RX'])

    return commands

def test_update(inputs):
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

    commands['FLA'] = 0
    commands['FRA'] = 0
    commands['RLA'] = 0
    commands['RRA'] = 0

    commands['FLS'] = 0
    commands['FRS'] = 0
    commands['RLS'] = 0
    commands['RRS'] = 0

    time.sleep(0.5)

    commands['FLS'] = 0.5*config.MAX_SPEED
    commands['FRS'] = 0.5*config.MAX_SPEED
    commands['RLS'] = 0.5*config.MAX_SPEED
    commands['RRS'] = 0.5*config.MAX_SPEED

    time.sleep(0.5)

    commands['FLS'] = config.MAX_SPEED
    commands['FRS'] = config.MAX_SPEED
    commands['RLS'] = config.MAX_SPEED
    commands['RRS'] = config.MAX_SPEED

    time.sleep(0.5)

    commands['FLS'] = 0
    commands['FRS'] = 0
    commands['RLS'] = 0
    commands['RRS'] = 0

    time.sleep(0.5)

    commands['FLA'] = 0.5*config.MAX_STEER
    commands['FRA'] = 0.5*config.MAX_STEER
    commands['RLA'] = 0.5*config.MAX_STEER
    commands['RRA'] = 0.5*config.MAX_STEER

    time.sleep(0.5)

    commands['FLA'] = config.MAX_STEER
    commands['FRA'] = config.MAX_STEER
    commands['RLA'] = config.MAX_STEER
    commands['RRA'] = config.MAX_STEER
    