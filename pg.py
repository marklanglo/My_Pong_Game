#! /usr/bin/env python3
# Mark Wiedeman
# CPSC 386-01
# 2022-08-05
# markwiedeman5@csu.fullerton.edu
# @marklanglo
#
# Lab 04-00
#
# This is a Program is Pong against an AI
#

"""This Module acts as the main and runs the whole game"""
from ponggame import game


def main():
    """This function defines main"""
    the_game_obj = game.PongGame()
    the_game_obj.build_scene_graph()
    return the_game_obj.run()


if __name__ == '__main__':
    main()
