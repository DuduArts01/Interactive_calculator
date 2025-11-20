import os
import pygame

class MainControlImages:
    @classmethod
    def load(cls):
        # main directory
        main = os.path.dirname(__file__)

        '''title'''
        #directory button
        title = os.path.join(main, "data/title")

        #image title
        interative_calculator = os.path.join(title, "calculadora_interativa.png") # calculator interactive
        selectmode = os.path.join(title, "select_mode.png") # select_mode
        PVsComputerTitle = os.path.join(title, "1VComputerTitle.png") # select_mode
        
        #load image
        cls.interative_calculator_image = pygame.image.load(interative_calculator).convert_alpha() # interative calculator
        cls.selectmode_image = pygame.image.load(selectmode).convert_alpha() # select mode
        cls.PVsComputerTitle_image = pygame.image.load(PVsComputerTitle).convert_alpha() # PVsComputerTitle

        '''sprites'''
        #directory button
        button = os.path.join(main, "data/sprite/button")

        #Sprite in directory button
        sprite_start = os.path.join(button, "start/start.png") # Sprite start
        sprite_1vComputer = os.path.join(button, "1vComputer/1vComputer.png") # 1 Vs Computer
        sprite_send = os.path.join(button, "send/send.png") # Sprite send


        #load sprites
        cls.start_image = pygame.image.load(sprite_start).convert_alpha() # Start
        cls.PvComputer_image = pygame.image.load(sprite_1vComputer).convert_alpha() # 1 vs Computer
        cls.send_image = pygame.image.load(sprite_send).convert_alpha() # send


        width, height = cls.start_image.get_size()
        
        '''Resize and position'''
        cls.interative_calculator_image_data = {
            "image": cls.interative_calculator_image,
            "x": 0,
            "y": 0,
            "width": width,
            "height": height,
            "resize_x": width * 8,
            "resize_y": height * 14,
        } #title interactive calculator

        cls.selectmode_image_data = {
            "image": cls.selectmode_image,
            "x": 0,
            "y": 0,
            "width": width,
            "height": height,
            "resize_x": width * 8,
            "resize_y": height * 14,
        } #title select mode

        cls.PVsComputerTitle_image_data = {
            "image": cls.PVsComputerTitle_image,
            "x": 0,
            "y": 0,
            "width": width,
            "height": height,
            "resize_x": width * 4,
            "resize_y": height * 6,
        } #title select mode

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
            "image": cls.PvComputer_image,
            "x": 0,
            "y": 0,
            "width": width,
            "height": height,
            "resize_x": width,
            "resize_y": height,
        } #sprite 1vC

        cls.send_imag_image_data = {
            "image": cls.send_image,
            "x": 0, #position x
            "y": 0, #position y
            "width": width, #width
            "height": height, #height
            "resize_x": width * 2, #resize x
            "resize_y": height * 2, #resize y
        } #sprite button send