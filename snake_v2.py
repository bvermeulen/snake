#!/usr/bin/env python
'''     Snake around                   
                                               
        python version 3.6                      
                                               
        snake movement on a surface                 
                                                
        For more information read the           
        readme.txt!                             
                                                
        Author: Bruno Vermeulen                 
        bruno_vermeulen2001@yahoo.com           
'''
import sys
import random
import pygame
from pygame.locals import *

import snake_module_v2
from snake_module_v2 import (SnakeObject, WallObject, plot_grid, mouse_pressed, move_randomly, reset_snakes,  
                             display_text, plot_snakes, reset_snakes, randomvector
                            )
import cfg
from cfg import BLACK, BLUE, GREY, ORANGE, read_config, set_parameters

def main():
    ''' Main program of snake
    '''
    read_config()
    set_parameters()
    run = True
    pause = True
    Left = False
    Right = False
    reset_snakes()
    m = (99999, 99999)
    display_text(0)
    wall = []
    wall.append(WallObject(cfg.wall_v[0], GREY))
    wall.append(WallObject(cfg.wall_v[1], ORANGE))
    '''run indefinetaly while run is true
    '''
    while run:
        ''' when program is paused you can create new snakes or delete existing ones by clicking the mouse on the action window
            if the program is not paused the snakes move around randomly
        '''
        if pause:
            ''' update status symbol to pause
            '''
            pygame.draw.rect(cfg.screen, BLACK, pygame.Rect(cfg.r_status_window), 0)
            cfg.screen.blit(cfg.pause_SMB, cfg.status_pos)
            ''' if mouse is pressed inside action window create a snake or remove it if already
                existed
            '''
            m = mouse_pressed(m)

        else:
            ''' update status symbol to run
            '''
            pygame.draw.rect(cfg.screen, BLACK, pygame.Rect(cfg.r_status_window), 0)
            cfg.screen.blit(cfg.run_SMB, cfg.status_pos)		
            ''' move all the snakes randomly snakes randomly
            '''
            move_randomly()
            m = (99999, 99999) # if program is not pause mouse pressed is disabled
        
        ''' clear screen, plot grid, display walls and snakes
        '''
        pygame.draw.rect(cfg.screen, BLACK, pygame.Rect(cfg.r_action_window), 0)    
        plot_grid()
        for i in range(len(wall)):
            wall[i].plot_wall()
        plot_snakes()

        for event in pygame.event.get():
            ''' there are three events to be considered: QUIT (click on exit window icon), KEYDOWN, MOUSEBUTTONUP 
            '''
            if event.type == QUIT:            # stop running when Quit event type is triggered
                run = False

            elif event.type == KEYDOWN:
                ''' if event is key press (KEYDOWN) then check if following option occur
                '''
                if event.key == K_b:          # b - change border color to blue
                    cfg.bcolor = BLUE
                elif event.key == K_o:        # o - change border color to orange
                    cfg.bcolor = ORANGE
                elif event.key == K_ESCAPE:   # Escape - leave program
                    run = False
                elif event.key == K_SPACE:    # Space - change pause status, pause is not pause
                    pause = not pause
                elif event.key == K_l:        # l - load pattern
                    load_pattern()
                elif event.key == K_s:        # s - save pattern, note this overwrites the file
                    save_pattern()
                elif event.key == K_c:        # c - clear screen and pause
                    pause = True
                    reset_snakes()
                    pygame.draw.rect(cfg.screen, BLACK, pygame.Rect(cfg.r_action_window), 0)
                    plot_grid
                elif event.key == K_LEFT:     # LEFT arrow - move left
                    Left = True
                elif event.key == K_RIGHT:    # RIGHT arrow - move right
                    Right = True
								
            elif event.type == MOUSEBUTTONUP: 
                ''' if event is mouse clicked then determine the location through cell indices
                '''
                m = pygame.mouse.get_pos()
                m = [int((m[0]-cfg.a_w_o[0])/cfg.cell_dim_x),int((m[1]-cfg.a_w_o[1])/cfg.cell_dim_y)]

        ''' update the screen and display
        '''
        pygame.display.flip()
        cfg.fpsClock.tick(cfg.fps)
	        
        time = pygame.time.get_ticks()
        display_text(time)

    pygame.quit()
    sys.exit

if __name__ == "__main__" :
    main()
