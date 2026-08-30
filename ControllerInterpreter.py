import pygame
import math
from gpiozero import Motor, AngularServo
from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockPWMPin

Device.pin_factory = MockFactory(pin_class=MockPWMPin)

pygame.init()
pygame.joystick.init()

# Axes return floats between -1 and 1, vertical axes are inverted, only read when changed
# Buttons return button presses and releases

# LT -> 4 | RT -> 5
# LB -> 4 | RB -> 5
# LX -> 0 | LY -> 1 | RX -> 2 | RY -> 3
# A -> 0 | B -> 1 | X -> 2 |  Y -> 3
# LS -> 8 | RS -> 9
# DL DR DU DD
# Central four buttons all trigger various Windows shortcuts, so don't use

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except:
    print("No controller connected.")
    quit()

clock = pygame.time.Clock()

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

def set_steer_angle(name, angle_deg):
    angle_deg = max(-90, min(90, angle_deg))
    steer_servos[name].angle = angle_deg

def set_motor_speed(name, speed):
    speed = max(-1, min(1, speed))
    drive_motors[name].value = speed

controller = {
    'LX': 0.0,
    'LY': 0.0,
    'RX': 0.0,
    'RY': 0.0,

    'LT': 0.0,
    'RT': 0.0

    #'A': False,
    #'B': False,
    #'X': False,
    #'Y': False,

    #'LB': False,
    #'RB': False
}

axis_map = {
    0: 'LX',
    1: 'LY',
    2: 'RX',
    3: 'RY',
    4: 'LT',
    5: 'RT'
}

button_map = {
    0: 'A',
    1: 'B',
    2: 'X',
    3: 'Y',
    4: 'LB',
    5: 'RB'
}

motors = {
    'FLS': 0,
    'FRS': 0,
    'RLS': 0,
    'RRS': 0,
    'FLA': 0,
    'FRA': 0,
    'RLA': 0,
    'RRA': 0
}

def ackermann_outer_angle(inner_angle, width, length):
    if inner_angle == 0:
        return 0.0

    sign = 1 if inner_angle > 0 else -1
    inner_angle_rad = math.radians(abs(inner_angle))

    cot_i = 1 / math.tan(inner_angle_rad)
    cot_o = cot_i + (width / length)
    outer_angle_rad = math.atan2(1, cot_o)  # atan2 avoids div-by-zero if cot_o == 0
    outer_angle_deg = math.degrees(outer_angle_rad)

    return round(sign * outer_angle_deg)


max_steer = 90
max_speed = 1
width = 78
length = 101

def deadzone(value, threshold=0.05):
    if abs(value) < threshold:
        return 0
    return value


while True:
    #print(pygame.event.get())
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1 or event.axis == 3:
                controller[axis_map[event.axis]] = deadzone(round(-event.value, 2))
            elif event.axis == 4 or event.axis == 5:
                controller[axis_map[event.axis]] = deadzone(round((event.value + 1) / 2, 2), 0.01)
            else:
                controller[axis_map[event.axis]] = deadzone(round(event.value, 2))
        elif event.type == pygame.JOYBUTTONDOWN:
            controller[button_map[event.button]] = True
        elif event.type == pygame.JOYBUTTONUP:
            controller[button_map[event.button]] = False
        #if event.type == pygame.JOYHATMOTION:
            #print("Hat", event.value)

    '''print(f"LX: {controller['LX']}\n"
          f"LY: {controller['LY']}\n"
          f"RX: {controller['RX']}\n"
          f"RY: {controller['RY']}\n"
          f"LT: {controller['LT']}\n"
          f"RT: {controller['RT']}")'''

    steer = round(controller['LX']*max_steer)
    if controller['RT'] > controller['LT']:
        speed = round(controller['RT']*max_speed)
    else:
        speed = -round(controller['LT']*max_speed)

    set_motor_speed('FLS', speed)
    set_motor_speed('FRS', speed)
    set_motor_speed('RLS', speed)
    set_motor_speed('RRS', speed)

    #motors['FLS'], motors['FRS'], motors['RLS'], motors['RRS'] = speed, speed, speed, speed

    '''print(f"Steer: {steer}\n"
          f"Speed: {speed}")'''

    if steer > 0:
        motors['FRA'] = steer
        motors['FLA'] = ackermann_outer_angle(steer, width, length)
    elif steer < 0:
        motors['FLA'] = steer
        motors['FRA'] = ackermann_outer_angle(steer, width, length)
    else:
        motors['FLA'], motors['FRA'] = 0, 0

    for key, value in drive_motors.items():
        print(f"{key}: {value}")


    clock.tick(60)