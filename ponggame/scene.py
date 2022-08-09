
"""Game scenes"""
import os
import pygame
from ponggame.ball import Ball
from ponggame.paddle import OpponentAI, Paddle
from ponggame.game_overlay import Overlay

class Scene:
    """This Class Defines the Base Scene"""
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')
    title_song = os.path.join(data_dir, 'HoliznaCC0 - Complications.wav')
    game_song = os.path.join(data_dir, 'HoliznaCC0 - Dance Till You Die.wav')

    def __init__(self, screen, background_color, soundtrack=None):
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._is_valid = True
        self._playing_song = False
        self._frame_rate = 60
        self._next_scene = None
        if soundtrack:
            self._soundtrack = os.path.join(Scene.data_dir, soundtrack)
        else:
            self._soundtrack = None
        self._is_soundtrack_on = True

    def update(self):
        """This Method Defines update for usage in other classes"""
        pass

    def draw(self):
        """This Method Defines draw for usage in other classes"""
        self._screen.blit(self._background, (0, 0))

    def toggle_soundtrack(self):
        """This Method toggles whether the soundtrack plays or not"""
        self._is_soundtrack_on = not self._is_soundtrack_on
        if not self._is_soundtrack_on:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def start(self):
        """This Method initiliazes and starts a Scene"""
        self._is_valid = True
        self._is_soundtrack_on = True
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1, 0.0, 500) #fades in and plays forever
            except pygame.error as pygame_error:
                print(f'Cannot open {self._soundtrack}')
                raise SystemExit(1) from pygame_error

    def stop(self):
        """This Method Defines stopping a Scene"""
        pygame.mixer.music.unpause()
        pygame.mixer.music.fadeout(500)

    @property
    def is_valid(self):
        """This Property returns if a scene is valid"""
        return self._is_valid

    @property
    def frame_rate(self):
        """This Property returns the frame rate of a scene"""
        return self._frame_rate

    def handle_event(self, event):
        """This Method Defines basic way to handle user input"""
        if event.type == pygame.KEYDOWN and \
        event.key == pygame.K_ESCAPE:
            self._is_valid = False
            self._next_scene = 4

class TitleScene(Scene):
    """This Class Defines update for usage in other classes"""
    def __init__(self,
                 title,
                 screen,
                 background_color,
                 soundtrack='HoliznaCC0 - Complications.wav'):
        super().__init__(screen, background_color, soundtrack)
        self._title = title
        self._frame_rate = 2
        self._flasher = False
        self._next_scene = 1

    def draw(self):
        """This Method draws all title screen text"""
        super().draw()
        (width, height) = self._screen.get_size()
        # title_font = pygame.font.Font(pygame.font.match_font('lato'), 100)
        title_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        enter_font = pygame.font.Font(pygame.font.get_default_font(), 30)
        instruction_font = pygame.font.Font(pygame.font.get_default_font(), 20)

        #Creates Main title
        rendered_title = title_font.render(self._title, True, (0, 50, 0))
        title_position = rendered_title.get_rect(center=(width * 0.5, height * 0.5))
        self._screen.blit(rendered_title, title_position)

        #Creates flashing text
        if self._flasher:
            rendered_enter = enter_font.render("Press any button to continue. . .", True, 100)
            enter_position = rendered_enter.get_rect(center=(width * 0.5, height/1.5))
            self._screen.blit(rendered_enter, enter_position)
            rendered_enter = instruction_font.render("Use 'Escape' at any time to close the Game",
                                                     True,
                                                     100)
            enter_position = rendered_enter.get_rect(center=(width * 0.5, height/1.4))
            self._screen.blit(rendered_enter, enter_position)
            self._flasher = not self._flasher
        else:
            rendered_enter = enter_font.render("Press any button to continue. . .",
                                               True,
                                               (255, 255, 255))
            enter_position = rendered_enter.get_rect(center=(width * 0.5, height/1.5))
            self._screen.blit(rendered_enter, enter_position)
            rendered_enter = instruction_font.render("Use 'Escape' at any time to close the Game",
                                                     True,
                                                     (255, 255, 255))
            enter_position = rendered_enter.get_rect(center=(width * 0.5, height/1.4))
            self._screen.blit(rendered_enter, enter_position)
            self._flasher = not self._flasher

        rendered_instr = instruction_font.render("Win by being the first paddle to reach 3 points",
                                                 True,
                                                 (255, 255, 255))
        instruction_position = rendered_instr.get_rect(center=(width * 0.5, height * 0.8))
        self._screen.blit(rendered_instr, instruction_position)
        rendered_instr = instruction_font.render("by using 'W' and 'S', or the arrow keys,",
                                                 True,
                                                 (255, 255, 255))
        instruction_position = rendered_instr.get_rect(center=(width * 0.5, height * 0.84))
        self._screen.blit(rendered_instr, instruction_position)
        rendered_instr = instruction_font.render("to hit the ball past the other paddle",
                                                 True,
                                                 (255, 255, 255))
        instruction_position = rendered_instr.get_rect(center=(width * 0.5, height * 0.88))
        self._screen.blit(rendered_instr, instruction_position)

    def stop(self):
        """This Method returns the next scene number"""
        super().stop()
        return self._next_scene

    def handle_event(self, event):
        """This Method handles any key presses"""
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            self._is_valid = False
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
        #     self.toggle_soundtrack()
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        #     self._is_valid = False
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     self._is_valid = False


class GameScene(Scene):
    """This Class handles the game scene logic"""
    def __init__(self, screen, background_color, soundtrack='HoliznaCC0 - Dance Till You Die.wav'):
        super().__init__(screen, background_color, soundtrack)
        self._frame_rate = 120
        self._next_screen_available = False
        self._next_scene = 0
        (width, height) = self._screen.get_size()
        self._overlay = Overlay(screen)
        self._paddle_left = Paddle(screen)
        self._paddle_right = OpponentAI(screen, width - 70)
        self._paddle_list = [self._paddle_left, self._paddle_right]
        self._ball = Ball(
            screen,
            self._paddle_list,
            width/2,
            height/2,
        )

    def start(self):
        """This Method reinitializes the Scene and starts it"""
        super().start()
        self._next_scene = 0
        (width, height) = self._screen.get_size()
        self._ball = Ball(
            self._screen,
            self._paddle_list,
            width/2,
            height/2,
        )
        self._overlay = Overlay(self._screen)

    def update(self):
        """This Method updates the ball, paddles, overlay, sound, and etc"""
        # print('I am the game scene, you will quote everything i say')
        self._ball.update()
        self._paddle_left.update()
        self._paddle_right.update(self._ball)
        self._overlay.update(self._ball)
        if not self._playing_song:
            self._playing_song = True
        if self._overlay.check_winner():
            self._next_screen_available = True
            if self._overlay.check_winner() == 1:
                self._next_scene = 2
            if self._overlay.check_winner() == 2:
                self._next_scene = 3

    def draw(self):
        """This Method redraws all game scene objects"""
        super().draw()
        self._overlay.draw()
        self._ball.draw()
        self._paddle_left.draw()
        self._paddle_right.draw()

    def handle_event(self, event):
        """This Method user inputs"""
        super().handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN \
           and self._next_screen_available:
            self._is_valid = False
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        #     if self._ball.is_moving:
        #         self._ball.stop()
        #     else:
        #         self._ball.start()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self._ball.toggle_sfx()
            self.toggle_soundtrack()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            self._overlay.toggle_tutorial()
        elif (event.type == pygame.KEYDOWN and \
        (event.key == pygame.K_s \
         or event.key == pygame.K_w \
         or event.key == pygame.K_UP \
         or event.key == pygame.K_DOWN)):
            self._paddle_left.move(event) #paddles move
        elif event.type == pygame.KEYUP:
            self._paddle_left.move(event) #paddles stop moving

    def stop(self):
        """This Method stops the current scene and returns the next scene int"""
        super().stop()
        return self._next_scene

class WinScene(Scene):
    """This Class defines the Win screen"""
    def __init__(self,
                 title,
                 screen,
                 background_color,
                 soundtrack='HoliznaCC0 - Complications.wav'):
        super().__init__(screen, background_color, soundtrack)
        self._title = title
        self._frame_rate = 2
        self._next_scene = 4

    def draw(self):
        """This Method draws all win screen text"""
        super().draw()
        (width, height) = self._screen.get_size()

        #You Win title
        title_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        rendered_title = title_font.render(self._title, True, (0, 0, 0))
        title_position = rendered_title.get_rect(center=(width * 0.5, height * 0.5))
        self._screen.blit(rendered_title, title_position)

        #Subtext to win
        subtitle = "Press 'ENTER' to play again, or 'ESC' to exit"
        subtitle_font = pygame.font.Font(pygame.font.get_default_font(), 16)
        rendered_subtitle = subtitle_font.render(subtitle, True, (0, 0, 0))
        subtitle_position = rendered_subtitle.get_rect(center=(width * 0.5, height * 0.6))
        self._screen.blit(rendered_subtitle, subtitle_position)


    def start(self):
        """This Method starts the Win screen"""
        super().start()
        self._next_scene = 4

    def stop(self):
        """This Method stops the Win screen and returns the next screen"""
        super().stop()
        return self._next_scene

    def handle_event(self, event):
        """This Method handles if the user presses Enter or Esc"""
        super().handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._is_valid = False
            self._next_scene = 1

class LoseScene(Scene):
    """This Class defines the Lose screen"""
    def __init__(self,
                 title,
                 screen,
                 background_color,
                 soundtrack='HoliznaCC0 - Complications.wav'):
        super().__init__(screen, background_color, soundtrack)
        self._title = title
        self._frame_rate = 2
        self._next_scene = 4

    def draw(self):
        """This Method draws all Lose screen text"""
        super().draw()
        (width, height) = self._screen.get_size()

        #You Lost title
        title_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        rendered_title = title_font.render(self._title, True, (255, 255, 255))
        title_position = rendered_title.get_rect(center=(width * 0.5, height * 0.5))
        self._screen.blit(rendered_title, title_position)

        #Subtext to lose
        subtitle = "...but you can try again by pressing 'ENTER', or 'ESC' if you want to exit"
        subtitle_font = pygame.font.Font(pygame.font.get_default_font(), 16)
        rendered_subtitle = subtitle_font.render(subtitle, True, (255, 255, 255))
        subtitle_position = rendered_subtitle.get_rect(center=(width * 0.5, height * 0.6))
        self._screen.blit(rendered_subtitle, subtitle_position)

    def start(self):
        """This Method starts the Lose screen"""
        super().start()
        self._next_scene = 4

    def stop(self):
        """This Method stops the Lose screen and returns the next screen"""
        super().stop()
        return self._next_scene

    def handle_event(self, event):
        """This Method handles if the user presses Enter or Esc"""
        super().handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._is_valid = False
            self._next_scene = 1
