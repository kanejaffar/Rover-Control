import input
import control
import output
import pygame

clock = pygame.time.Clock()

input.initialise()

while True:
    try:
        inputs = input.update()
        commands = control.update(inputs)
        output.update(commands)
        clock.tick(30)  # Samples per second
    except KeyboardInterrupt:
        output.shutdown()
        exit()
        sys.exit()