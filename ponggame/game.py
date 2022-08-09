
"""This module contains the main game loop"""

import pygame

from ponggame.scene import TitleScene, GameScene, WinScene, LoseScene

class VideoGame():
    """This class defines the basic video game loop"""
    def __init__(self,
                 window_width=1200,
                 window_height=800,
                 window_title='Wowee, PONG'):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        self._title = window_title
        pygame.display.set_caption(self._title)
        self._game_is_over = False

        if not pygame.font:
            print('Warning: fonts are disabled.')
        if not pygame.mixer:
            print('Warning: sound is disabled')

        self._scene_graph = None


    def build_scene_graph(self):
        """This method defines the scene graph"""
        self._scene_graph = [
            TitleScene("Wowee, PONG", self._screen, (255, 100, 200)),
            GameScene(self._screen, (0, 0, 0)),
            WinScene("YOU WON!", self._screen, (0, 255, 255)),
            LoseScene("You Lost", self._screen, (255, 0, 0))
        ]


    def run(self):
        """This is the main run function for the whole program"""
        # while not self._game_is_over:
        pos = 0 # scene number
        while pos < len(self._scene_graph):
            self._scene_graph[pos].start()
            while self._scene_graph[pos].is_valid:
                self._clock.tick(self._scene_graph[pos].frame_rate)
                for event in pygame.event.get():
                    self._scene_graph[pos].handle_event(event)
                self._scene_graph[pos].update()
                self._scene_graph[pos].draw()
                pygame.display.update()
            pos = self._scene_graph[pos].stop()

        pygame.display.quit()
        pygame.quit()
        return 0

class PongGame(VideoGame):
    """This class defines the basic pong game loop"""
    def __init__(self, window_width=800, window_height=500, window_title='Wowee, PONG'):
        super().__init__(window_width, window_height, window_title)
