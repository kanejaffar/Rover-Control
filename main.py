import input
import control
import output
import pygame

clock = pygame.time.Clock()

input.initialise()

while True:
    pygame.event.pump()
    inputs = input.update()
    commands = control.update(inputs)
    output.update(commands)
    clock.tick(4)  # Samples per second
    