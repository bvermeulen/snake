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
from pygame.locals import (QUIT, KEYDOWN,MOUSEBUTTONUP, 
                           K_o, K_b, K_l, K_s, K_c, 
                           K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT)

import snake_module_v3
from snake_module_v3 import (SnakeObject, WallObject, Cell, plot_grid_walls, init_walls, init_cells, mouse_pressed, 
                             move_randomly, reset_snakes, display_text, plot_snakes, reset_snakes, plot_monitor,
                             randomvector 
                            )
import snake_configuration
from snake_configuration import BLACK, WHITE, BLUE, GREY, ORANGE, read_config, SnakeSetup

def main():
    ''' Main program of snake
    '''
    global run, pause, Left, Right, m, wall, time, bcolor, setup# set to global to have access at interrupt
    ''' initialise the global snake set up paramaters
    '''
    setup = SnakeSetup()
    print(repr(setup))

    ''' initialise the local variables
    '''
    run = True
    pause = True
    Left = False
    Right = False
    reset_snakes()
    m = (99999, 99999)
    bcolor = BLUE
    display_text(0)
    init_cells()
    wall = init_walls()
    plot_monitor()

    '''run indefinetaly while run is true
    '''
    while run:
        ''' when program is paused you can create new snakes or delete existing ones by clicking the mouse on the action window
            if the program is not paused the snakes move around randomly
        '''
        if pause:
            ''' update status symbol to pause
            '''
            pygame.draw.rect(setup.screen, BLACK, pygame.Rect(setup.r_status_window), 0)
            setup.screen.blit(setup.pause_SMB, setup.s_w_o)
            ''' if mouse is pressed inside action window create a snake or remove it if already
                existed
            '''
            m = mouse_pressed(m)

        else:
            ''' update status symbol to run
            '''
            pygame.draw.rect(setup.screen, BLACK, pygame.Rect(setup.r_status_window), 0)
            setup.screen.blit(setup.run_SMB, setup.s_w_o)		
            ''' move all the snakes randomly snakes randomly
            '''
            move_randomly()
            m = (99999, 99999) # if program is not pause mouse pressed is disabled
        
        ''' clear screen, plot grid, display walls and snakes
        '''
        pygame.draw.rect(setup.screen, BLACK, pygame.Rect(setup.r_action_window), 0)    
        plot_grid_walls(bcolor, wall)
        plot_snakes()
        plot_monitor()

        for event in pygame.event.get():
            ''' there are three events to be considered: QUIT (click on exit window icon), KEYDOWN, MOUSEBUTTONUP 
            '''
            if event.type == QUIT:            # stop running when Quit event type is triggered
                run = False

            elif event.type == KEYDOWN:
                ''' if event is key press (KEYDOWN) then check if following option occur
                '''
                if event.key == K_b:          # b - change border color to blue
                    bcolor = BLUE
                elif event.key == K_o:        # o - change border color to orange
                    bcolor = ORANGE
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
                    init_cells()
                    wall = init_walls()
                    pygame.draw.rect(setup.screen, BLACK, pygame.Rect(setup.r_action_window), 0)
                    plot_grid_walls(bcolor, wall)
                elif event.key == K_LEFT:     # LEFT arrow - move left
                    Left = True
                elif event.key == K_RIGHT:    # RIGHT arrow - move right
                    Right = True
								
            elif event.type == MOUSEBUTTONUP: 
                ''' if event is mouse clicked then determine the location through cell indices
                '''
                m = pygame.mouse.get_pos()
                m = [int((m[0]-setup.a_w_o[0])/setup.cell_dim_x),int((m[1]-setup.a_w_o[1])/setup.cell_dim_y)]

        ''' update the screen and display
        '''
        pygame.display.flip()
        setup.fpsClock.tick(setup.fps)
	        
        time = pygame.time.get_ticks()
        display_text(time)

    pygame.quit()
    sys.exit

    return run, pause, Left, Right, m, wall, cell, time, bcolor, setup

if __name__ == '__main__':
    run, pause, Left, Right, m, cell, wall, time, bcolor, setup = \
    main() # on normal completion of program maintain the variables for inspection
