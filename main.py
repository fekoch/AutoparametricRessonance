import math
import sys
import pygame
import numpy as np

black = 0, 0, 0
white = 255, 255, 255
weight_color = 255, 204, 88
size = width, height = 1220, 840

g = 9.81


class Weight:
    anchor_position = (0, 0)
    string_length = width / 5
    angle = -math.pi / 3
    velocity = 0
    acceleration = 0
    angular_velocity = 0
    mass = 1

    def _get_position(self) -> (float, float):
        relative_position = np.sin(self.angle) * self.string_length, np.cos(self.angle) * self.string_length
        return np.add(relative_position, self.anchor_position)

    position = property(_get_position)

    def __str__(self):
        return f"Weight[angle={self.angle}, a={self.acceleration}, v={self.velocity}, w={self.angular_velocity}"

    def __init__(self, anchor_pos: (float, float), init_angle=-math.pi / 3):
        self.anchor_position = anchor_pos
        if init_angle is None:
            init_angle = - math.pi / 3
        self.angle = init_angle


def calc_w_pos(weight: Weight):
    t = 0.0001

    weight.acceleration = -g * weight.mass * np.sin(weight.angle)
    weight.velocity += weight.acceleration
    weight.angular_velocity = weight.velocity / weight.string_length
    weight.angle += weight.angular_velocity * t

    # print(weight.__str__())


def game_loop(screen, trace=False, no_strings=False):
    anchor = width / 2, height * 0.05
    w = Weight(anchor)
    w2 = Weight(w.position, math.pi / 2)
    w3 = Weight(w2.position, -math.pi / 4)

    screen.fill(black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        calc_w_pos(w)
        w2.anchor_position = w.position
        calc_w_pos(w2)
        w3.anchor_position = w2.position
        calc_w_pos(w3)

        if not trace:
            screen.fill(white)

        # pendulum anchor
        pygame.draw.circle(screen, black, anchor, 4, 2, )

        # draw weight
        pygame.draw.circle(screen, weight_color, w.position, 10, 0)
        if not no_strings:
            pygame.draw.line(screen, black, start_pos=w.position, end_pos=anchor)

        pygame.draw.circle(screen, weight_color, w2.position, 10, 0)
        if not no_strings:
            pygame.draw.line(screen, black, start_pos=w2.position, end_pos=w2.anchor_position)

        pygame.draw.circle(screen, weight_color, w3.position, 10, 0)
        if not no_strings:
            pygame.draw.line(screen, black, start_pos=w3.position, end_pos=w3.anchor_position)

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()

    display_screen = pygame.display.set_mode(size)

    game_loop(display_screen, True)
