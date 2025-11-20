import pygame
import sys
from menu_main import MainMenuProgram
from mainImages import MainControlImages
from gameselect.gameselect import Select_Mode
from onevscomputer.computer import Game_computer


pygame.init()
#screen = pygame.display.set_mode((800, 480), pygame.RESIZABLE)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # fullscreen automatic

MainControlImages.load()

# Roda enquanto houver telas para mostrar
current_screen = "menu"

while current_screen:
    if current_screen == "menu": # Screen Menu
        controler_screen = MainMenuProgram(screen)
        current_screen = controler_screen.run()

    elif current_screen == "gameselect": # Screen select mode game
        controler_screen = Select_Mode(screen)
        current_screen = controler_screen.run()
    elif current_screen == "computergame": # Screen select mode game
        controler_screen = Game_computer(screen)
        current_screen = controler_screen.run()

pygame.quit()
sys.exit()