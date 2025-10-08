import os
import pygame

class MainControlImages:
    @classmethod
    def load(cls):
        # main directory
        main = os.path.dirname(__file__)
        
        #sprites
            #directory button
        button = os.path.join(main, "data/sprite/button")

        #Sprite in directory button
        sprite_start = os.path.join(button, "start/start.png") # Sprite start
        sprite_1vComputer = os.path.join(button, "1vComputer/1vComputer.png") # 1 Vs Computer


        #load sprites
        cls.start_image = pygame.image.load(sprite_start).convert_alpha() # Start
        cls.sprite_1vComputer_image = pygame.image.load(sprite_1vComputer).convert_alpha() # 1 vs Computer

        width, height = cls.start_image.get_size()

        cls.start_image_data = {
            "image": cls.start_image,
            "x": 0, #position x
            "y": 0, #position y
            "width": width, #width
            "height": height, #height
            "resize_x": width * 2, #resize x
            "resize_y": height * 2, #resize y
        } #sprite button start

        cls.sprite_1vComputer_image_data = {
            "image": cls.sprite_1vComputer_image,
            "x": 0,
            "y": 0,
            "width": width,
            "height": height,
            "resize_x": width * 2,
            "resize_y": height * 2,
        } #sprite 1vC