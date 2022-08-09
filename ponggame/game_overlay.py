
from ponggame.ball import Ball
import pygame

class Overlay:
    def __init__(self, surface, color = pygame.Color(255, 255, 255)):
        self._surface = surface
        self._color = color
        self._color_flasher = pygame.Color(0, 255, 255)
        self._color_arrow_top = self._color
        self._color_arrow_bot = self._color_flasher
        self._score_one = 0
        self._score_two = 0
        self._winning_points = 3
        self._player_one_win = False
        self._player_two_win = False
        self._show_tutorial = False
        self._tutorial_display_timer = 840
        self._arrow_flash_timer = 180

    def update(self, ball):
        score = ball.get_point()
        if not score[1] and score[0] > 0:
            self._score_one = self._score_one + score[0]
        elif score[0] > 0:
            self._score_two = self._score_two + score[0]
        self._find_if_winner(ball)
        if self._tutorial_display_timer:
            self._tutorial_display_timer -= 1
        if self._arrow_flash_timer:
            self._arrow_flash_timer -= 1

    def draw(self):
        (width, height) = self._surface.get_size()

        #Draws both of the scores
        score_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        rendered_score_one = score_font.render(str(self._score_one), True, self._color)
        rendered_score_two = score_font.render(str(self._score_two), True, self._color)
        score_one_position = rendered_score_one.get_rect(center = (width * 0.4, height * 0.1))
        score_two_position = rendered_score_two.get_rect(center = (width * 0.6, height * 0.1))
        self._surface.blit(rendered_score_one, score_one_position)
        self._surface.blit(rendered_score_two, score_two_position)

        segments = 21
        #Draws dashed centerline
        for i in range(segments):
            if not i % 2:
                point_one = ((width * 0.5), height * (i+1)/segments) 
            else:
                point_two = ((width * 0.5), height * (i+1)/segments) 
                pygame.draw.line(self._surface, self._color, point_one, point_two, 10)

        self._draw_win_lose(width, height)
        if self._tutorial_display_timer or self._show_tutorial:
            self._draw_mini_tutorial(width, height)
        if self._tutorial_display_timer:
            self._draw_countdown(width, height)
        if not self._tutorial_display_timer:
            self._draw_subtext(width, height)

    def _draw_win_lose(self, width, height):
        outcome_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        continue_font = pygame.font.Font(pygame.font.get_default_font(), 25)
        if self._player_one_win:
            # "YOU"
            rendered_player_win_1 = outcome_font.render("YOU", True, pygame.Color(0, 255, 0))
            winner_banner_position_1 = rendered_player_win_1.get_rect(center = (width * 0.3, height * 0.5))
            self._surface.blit(rendered_player_win_1, winner_banner_position_1)
            # "WON"
            rendered_player_win_2 = outcome_font.render("WON", True, pygame.Color(0, 255, 0))
            winner_banner_position_2 = rendered_player_win_2.get_rect(center = (width * 0.7, height * 0.5))
            self._surface.blit(rendered_player_win_2, winner_banner_position_2)
            # "Press Enter to Continue"
            rendered_continue = continue_font.render("Press 'Enter' to Continue", True, pygame.Color(0, 255, 0))
            continue_position = rendered_continue.get_rect(center = (width * 0.5, height * 0.7))
            self._surface.blit(rendered_continue, continue_position)
        elif self._player_two_win:
            # "You"
            rendered_comp_win_1 = outcome_font.render("You", True, pygame.Color(255, 0, 0))
            loser_banner_position_1 = rendered_comp_win_1.get_rect(center = (width * 0.3, height * 0.5))
            self._surface.blit(rendered_comp_win_1, loser_banner_position_1)
            # "Lost"
            rendered_comp_win_2 = outcome_font.render("Lost", True, pygame.Color(255, 0, 0))
            loser_banner_position_2 = rendered_comp_win_2.get_rect(center = (width * 0.7, height * 0.5))
            self._surface.blit(rendered_comp_win_2, loser_banner_position_2)
            # "Press Enter to Continue"
            rendered_continue = continue_font.render("Press 'Enter' to Continue", True, pygame.Color(255, 0, 0))
            continue_position = rendered_continue.get_rect(center = (width * 0.5, height * 0.7))
            self._surface.blit(rendered_continue, continue_position)

    def _draw_mini_tutorial(self, width, height):
        arrow_thickness = 8
        tutorial_font = pygame.font.Font(pygame.font.get_default_font(), 14)

        if self._arrow_flash_timer % 90 == 0:
            if self._color_arrow_top == self._color:
                self._color_arrow_top = self._color_flasher
            else:
                self._color_arrow_top = self._color
        
        if self._arrow_flash_timer % 90 == 0:
            if self._color_arrow_bot == self._color:
                self._color_arrow_bot = self._color_flasher
            else:
                self._color_arrow_bot = self._color

        if self._arrow_flash_timer == 0:
            self._arrow_flash_timer = 180

        #draws bottom arrow
        arrow_tip_one = (width * 0.2, height * 0.9)
        arrow_base_one = (width * 0.2, height * 0.7)
        arrow_left_one = (width * 0.19, height * 0.85)
        arrow_right_one = (width * 0.21, height * 0.85)
        pygame.draw.line(self._surface, self._color_arrow_bot, arrow_tip_one, arrow_base_one, arrow_thickness)
        pygame.draw.line(self._surface, self._color_arrow_bot, arrow_tip_one, arrow_left_one, arrow_thickness)
        pygame.draw.line(self._surface, self._color_arrow_bot, arrow_tip_one, arrow_right_one, arrow_thickness)

        #draws top arrow
        arrow_tip_two = (width * 0.2, height * 0.1)
        arrow_base_two = (width * 0.2, height * 0.3)
        arrow_left_two = (width * 0.19, height * 0.15)
        arrow_right_two = (width * 0.21, height * 0.15)
        pygame.draw.line(self._surface, self._color_arrow_top, arrow_tip_two, arrow_base_two, arrow_thickness)
        pygame.draw.line(self._surface, self._color_arrow_top, arrow_tip_two, arrow_left_two, arrow_thickness)
        pygame.draw.line(self._surface, self._color_arrow_top, arrow_tip_two, arrow_right_two, arrow_thickness)

        #instructions under top arroa
        rendered_up = tutorial_font.render("Press 'W' or 'Up'", True, self._color)
        up_position = rendered_up.get_rect(center = (width * 0.2, height * 0.35))
        self._surface.blit(rendered_up, up_position)

        #instructions above bottom arrow
        rendered_down = tutorial_font.render("Press 'S' or 'Down'", True, self._color)
        down_position = rendered_down.get_rect(center = (width * 0.2, height * 0.65))
        self._surface.blit(rendered_down, down_position)

    def _draw_countdown(self, width, height):
        countdown_font = pygame.font.Font(pygame.font.get_default_font(), 22)
        game_starts = "Beginning in " + str(self._tutorial_display_timer // 120) + " seconds . . ."
        rendered_countdown = countdown_font.render(game_starts, True, self._color)
        countdown_position = rendered_countdown.get_rect(center = (width * 0.3, height * 0.5))
        self._surface.blit(rendered_countdown, countdown_position)

    def _draw_subtext(self, width, height):
        if self.check_winner():
            subtext = "(T) Toggle Tutorial    (M) Toggle Volume    (Enter) Finish Game"
        else:
            subtext = "(T) Toggle Tutorial    (M) Toggle Volume"
        subtext_font = pygame.font.Font(pygame.font.get_default_font(), 10)
        rendered_subtext = subtext_font.render(subtext, True, self._color)
        subtext_position = rendered_subtext.get_rect(topleft = (width * 0.06, height * 0.98))
        self._surface.blit(rendered_subtext, subtext_position)
   
    def toggle_tutorial(self):
        self._show_tutorial = not self._show_tutorial

    def _find_if_winner(self, ball):
        if self._score_one == self._winning_points:
            self._player_one_win = True
            ball.set_game_over()
        elif self._score_two == self._winning_points:
            self._player_two_win = True
            ball.set_game_over()

    def check_winner(self):
        win_code = 0
        if self._player_one_win:
            win_code = 1
        elif self._player_two_win:
            win_code = 2
        return win_code
