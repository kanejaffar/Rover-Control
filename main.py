import input
import control
import output
import pygame

clock = pygame.time.Clock()

input.initialise()

while True:
    inputs = input.update()
    commands = control.update(inputs)
    output.update(commands)
    output.display(commands)
    clock.tick(4)  # Samples per second
    