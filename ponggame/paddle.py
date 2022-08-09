
"""This Module Handles Paddles"""
from random import randrange
import pygame

class Paddle:
    """This Class Handles the base Paddle and its collision"""
    def __init__(self, surface, x_pos=40, width=30, height=120):
        self._size = (width, height)
        self._speed = 5
        self._surface = surface
        self._paddle_length = 100
        self._color = pygame.Color((0, 255, 255))
        self._going_down = False
        self._going_up = False

        (_, win_height) = self._surface.get_size()
        self._lower_bound = win_height - height
        self._upper_bound = 0
        self._position = pygame.math.Vector2(x_pos, (win_height/2) - (height/2))
        self._goal_line_x = x_pos
        self._height = height

        self._rect = pygame.Rect(
            self._position,
            self._size)
        self._collide_heights = None

    def draw(self, draw_line=True):
        """This Method redraws paddle"""
        (_, win_height) = self._surface.get_size()
        self._rect = pygame.Rect(
            self._position,
            self._size
        )
        pygame.draw.rect(
            self._surface,
            self._color,
            self._rect
        )
        if draw_line:
            pygame.draw.line(
                self._surface,
                self._color,
                (self._goal_line_x, win_height),
                (self._goal_line_x, 0),
            )

    def update(self):
        """This Method updates the Paddle position"""
        if self._going_down and self._position.y <= self._lower_bound - 20:
            self._position.y = self._position.y + self._speed
        elif self._going_up and self._position.y >= self._upper_bound + 20:
            self._position.y = self._position.y - self._speed

    def move(self, event):
        """This Method handles control of the paddle"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self._going_down = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_s:
            self._going_down = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self._going_down = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            self._going_down = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            self._going_up = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_w:
            self._going_up = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self._going_up = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
            self._going_up = False

    def collide(self, x_y_position, x_y_speed, rad):
        """This Method handles the Paddle collision with the ball"""
        start_count = 4
        check_count = 10
        check_collision = False
        for i in range(start_count, check_count):
            point_x_true = x_y_position.x
            point_y_true = x_y_position.y
            point_x = x_y_position.x + (x_y_speed.x / i)
            point_y = x_y_position.y + (x_y_speed.y / i)

            if self._rect.collidepoint(point_x_true, point_y_true) \
            or self._rect.collidepoint(point_x_true, point_y_true + rad) \
            or self._rect.collidepoint(point_x_true, point_y_true - rad):
                check_collision = True
                break
            elif x_y_speed.magnitude() > rad \
            and (self._rect.collidepoint(point_x + rad/2.5, point_y + rad/2.5) \
            or self._rect.collidepoint(point_x - rad/2.5, point_y - rad/2.5) \
            or self._rect.collidepoint(point_x - rad/2.5, point_y + rad/2.5) \
            or self._rect.collidepoint(point_x + rad/2.5, point_y - rad/2.5) \
            or self._rect.collidepoint(point_x, point_y + 2 * rad) \
            or self._rect.collidepoint(point_x, point_y - 2 * rad) \
            or self._rect.collidepoint(point_x - rad, point_y) \
            or self._rect.collidepoint(point_x + rad, point_y)):
                check_collision = True
                break
        return check_collision

    def rebound_direction(self, y_position):
        """This Method determines which direction the ball should go in"""
        self._collide_heights = [
            self._position.y,                              #top_corner
            self._position.y + (self._size[1] * 0.25),     #top_quarter
            self._position.y + (self._size[1] * 0.40),     #top_near_center
            self._position.y + (self._size[1] * 0.50),     #center
            self._position.y + (self._size[1] * 0.60),     #bottom_near_center
            self._position.y + (self._size[1] * 0.75),     #bottom_near_center
            self._position.y + (self._size[1]),            #bottom
        ]
        best = 100000
        direction = -1
        for index, position in enumerate(self._collide_heights):
            if abs(position - y_position) < best:
                best = abs(position - y_position)
                direction = index
        return direction

class OpponentAI(Paddle):
    """This Class defines the AI paddle"""
    def __init__(self, surface, x_pos=20, width=30, height=120):
        super().__init__(surface, x_pos, width, height)
        self._ai_delay = 10
        self._ball_offset_timer = 0
        self._ball_offset = 0
        self._width = 30

    def draw(self, draw_line=False):
        """This Method redraws paddle"""
        super().draw(draw_line)
        (_, win_height) = self._surface.get_size()
        pygame.draw.line(
            self._surface,
            self._color,
            (self._goal_line_x + self._width, win_height),
            (self._goal_line_x + self._width, 0),
        )

    def update(self, ball):
        """This Method updates paddle position"""
        if not self._ai_delay:
            self._move(ball.get_position())
        else:
            self._ai_delay = self._ai_delay - 1

        if self._going_up:
            self._position.y = self._position.y - self._speed
        elif self._going_down:
            self._position.y = self._position.y + self._speed

    def _new_ball_offset(self):
        """This Method randomizes an offset so the paddle is imperfect"""
        if not self._ball_offset_timer:
            self._ball_offset_timer = 360
            self._ball_offset = randrange(self._height * -0.4, self._height * 0.4)
        else:
            self._ball_offset_timer -= 1

    def _move(self, x_y_position):
        """This Method determines where the paddle moves relative to ball"""
        ball_y = x_y_position[1]
        self._going_up = False
        self._going_down = False
        self._new_ball_offset()
        #moving up
        if ball_y + self._ball_offset < self._position.y + self._height * 0.4 \
        and self._position.y >= self._upper_bound + 20:
            if self._position.y <= self._upper_bound + 25:
                self._going_up = False
            elif (self._position.y + self._height * 0.25) - abs(ball_y + self._ball_offset) > 15:
                self._going_up = True
                self._ai_delay = 0
            else:
                self._going_up = False
                self._going_down = False
        #moving down
        elif ball_y + self._ball_offset > self._position.y - self._height * 0.8 \
        and self._position.y <= self._lower_bound - 20:
            if self._position.y >= self._lower_bound - 25:
                self._going_down = False
            elif (self._position.y - self._height * 0.75) - abs(ball_y + self._ball_offset) < -15:
                self._going_down = True
                self._ai_delay = 0
            else:
                self._going_up = False
                self._going_down = False
