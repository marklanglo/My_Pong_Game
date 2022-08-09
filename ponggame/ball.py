
import pygame
import os

class Ball:

    main_dir = os.path.split(os.path.abspath(__file__))[0]  #this gives the directory that the file is in
    data_dir = os.path.join(main_dir, 'data')               #this puts the data directory into the main_dir
    bounce_sound = os.path.join(data_dir, 'ball_bounce.wav') #replace this with a bounce sound

    default_radius = 5

    def __init__(self, surface, paddle_list, x_pos = 0, y_pos = 0, x_velocity = 0, y_velocity = 0):
        self._start_position = pygame.math.Vector2(x_pos, y_pos) #initializes ball position with a vector
        self._position = pygame.math.Vector2(x_pos, y_pos) #initializes ball position with a vector
        self._velocity = pygame.math.Vector2(x_velocity, y_velocity)
        self._max_velocity = Ball.default_radius * 2
        self._surface = surface
        self._paddle_list = paddle_list
        self._radius = Ball.default_radius
        self._color = pygame.Color((0, 255, 0))
        self._is_sound_on = True
        self._scored_left = False
        self._round_in_progress = False         #used to reset ball
        self._game_is_over = False              #used to stop ball
        self._score = 0
        self._rebound_frames = 0
        self._reset_timer = 840

        
        try:
            self._bounce_sound = pygame.mixer.Sound(Ball.bounce_sound)
            pygame.mixer.Sound.set_volume(self._bounce_sound, 0.2)
            self._bounce_channel = pygame.mixer.Channel(2)
        except pygame.error as pygame_error:
            print(f'Cannot open {Ball.bounce_sound}')
            raise SystemExit(1) from pygame_error


    def draw(self):
        pygame.draw.circle(
            self._surface, 
            self._color, 
            self._position, 
            self._radius
        )

    def update(self):
        self._position = self._position + self._velocity
        self._bounce()
        if self._rebound_frames:
            self._rebound_frames = self._rebound_frames - 1
        if not self._round_in_progress and not self._reset_timer:
            self.start()
        elif not self._game_is_over:
            self._reset_timer -= 1
        

    def start(self):
        if self._scored_left:
            self._velocity = pygame.math.Vector2(Ball.default_radius * 0.3, Ball.default_radius * 0.1)
        else: 
            self._velocity = pygame.math.Vector2(Ball.default_radius * -0.3, Ball.default_radius * -0.1)
        self._round_in_progress = True

    def stop(self):
        self._velocity = pygame.math.Vector2(0, 0)

    def _reset(self):
        self._position = self._start_position
        self._velocity = pygame.math.Vector2(0, 0)
        self._color = pygame.Color((0, 255, 0))
        self._round_in_progress = False
        self._reset_timer = 60

    def get_position(self):
        return [self._position.x, self._position.y]

    def get_point(self):
        score = (self._score, self._scored_left) #returns int and boolean of who scored
        self._score = 0
        return score

    @property
    def is_moving(self):
        return self._velocity.length_squared() > 0 #we use length_squared because it is faster to do a^2 + b^2 rather than sqrt(a^2 + b^2)

    def toggle_sfx(self):
        self._is_sound_on = not self._is_sound_on

    def set_game_over(self):
        self._game_is_over = True
        self._color = pygame.Color(0, 0, 0)

    def _play_sfx(self):
        if self._is_sound_on:
            self._bounce_channel.play(self._bounce_sound)

    def _change_angle(self, direction):

        #negative angle sends upwards, positive sends downwards
        if direction == 0:
            new_angle = -70
        elif direction == 1:
            new_angle = -45
        elif direction == 2:
            new_angle = -20
        elif direction == 3:
            new_angle = 0
        elif direction == 4:
            new_angle = 20
        elif direction == 5:
            new_angle = 45
        elif direction == 6:
            new_angle = 70

        new_vec = pygame.math.Vector2(self._velocity.length())
        new_vec.y = 0
        new_vec = new_vec.rotate(new_angle)
        if self._velocity.x > 0 and direction in (0, 1, 2, 3):
            new_vec.x = -1 * new_vec.x
        elif self._velocity.x > 0 and direction in (4, 5, 6):
            new_vec.x = -1 * new_vec.x

        self._velocity = new_vec


    def _bounce(self):
        (width, height) = self._surface.get_size()
        bounced_paddle = False
        if self._position.x >= width - 30 or self._position.x <= 30:
            if self._position.x >= width / 2:
                self._scored_left = False
            else:
                self._scored_left = True
            self._score = 1
            self._reset()
        if self._position.y >= height or self._position.y <= 0:
            bounced_paddle = True
            self._velocity = pygame.math.Vector2(self._velocity.x, self._velocity.y * -1)
        for _, paddle in enumerate(self._paddle_list):
            if paddle.collide(self._position, self._velocity, self._radius):
                if self._position.x < width / 2 and not self._rebound_frames:
                    self._change_angle(paddle.rebound_direction(self._position.y))
                    #self._velocity.x = abs(self._velocity.x)
                    bounced_paddle = True
                    self._rebound_frames = 40
                elif self._position.x > width / 2 and not self._rebound_frames:
                    self._change_angle(paddle.rebound_direction(self._position.y))
                    #self._velocity.x = -1 * abs(self._velocity.x)
                    bounced_paddle = True
                    self._rebound_frames = 40
        # this will play the sound of the ball bouncing when it bounces and it will increase the ball's velocity
        if bounced_paddle:
            self._play_sfx()
            if self._velocity.length_squared() < (self._max_velocity ** 2):
                self._velocity.x = self._velocity.x * 1.1
                self._velocity.y = self._velocity.y * 1.1
                red = self._color.r
                green = self._color.g
                if red + 10 <= 255 and green - 10 >= 0:
                    self._color.update(red + 15, green - 15, 0)
            # else:
            #     print(f'max velocity reached: x={self._velocity.x}, y={self._velocity.x}')
            
        
