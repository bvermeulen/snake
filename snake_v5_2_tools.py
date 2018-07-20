#!/usr/bin/env python
'''  Python 3.6

     module snake_v5_2_tools has the following classes and functions
     Class:
            - Setup
            - Cell
            - PlotObject
            - Monitor
            - Tools
'''
import re
import sys
import os
import random
from PIL import ImageTk
from tkinter import Tk, Canvas, Label, BOTH, YES
from Utils.plogger import set_logger

'''  set the constants
'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
ORANGE = (255, 100, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
LIGHTGREY = (200, 200, 200)
NOCOLOR = (999, 999, 999)
PADDING = 5
LWIDTH = 3
BWIDTH = 4
STATUS_X = 60
STATUS_Y = 68


class Setup:
    '''  Setup of variables environment for the program
         Input are the parameters from the configuration file
         Methods:
         - __init__
         - read_config
         - __repr__
    '''
    def read_config():
        '''  read config file in 1st argument (otherwise default is
        data/config.txt). Optionally 2nd argument is pattern file
        otherwise defined in config file returns values for:
        pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y
        '''
        if len(sys.argv) >= 2:
            config_file = sys.argv[1]

        else:
            config_file = os.path.join("data", "config.txt")

        try:
            with open(config_file) as cfile:
                pattern_file = cfile.readline()[17:]
                fps = int(cfile.readline()[17:])
                cells_x = int(cfile.readline()[17:])
                cells_y = int(cfile.readline()[17:])
                cell_dim_x = int(cfile.readline()[17:])
                cell_dim_y = int(cfile.readline()[17:])
        except: # noqa E722
            sys.exit('Unable to read the config file ...')

        if len(sys.argv) == 3:
            pattern_file = sys.argv[2]

        # remove return /r, new line /n or spaces /s from pattern_file
        pattern_file = re.sub(r'[\r\n\s]', '', pattern_file)

        return pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y

    '''  set the parameters
    '''
    # read the configuration file
    _pattern_file, _fps, _cells_x, _cells_y, _cell_dim_x, _cell_dim_y \
        = read_config()

    # set the variable from the configuration file
    pattern_file = _pattern_file
    fps = _fps
    cells_x = _cells_x
    cells_y = _cells_y
    cell_dim_x = _cell_dim_x
    cell_dim_y = _cell_dim_y

    #  set window boundaries - abbrevations stand for: a_ [action],
    #  m_ [monitor], s_ [status]
    a_w_o = (PADDING, PADDING)
    a_w_x = cells_x * cell_dim_x
    a_w_y = cells_y * cell_dim_y
    r_action_window = (a_w_o[0], a_w_o[1],
                       a_w_o[0] + a_w_x, a_w_o[1] + a_w_y)
    s_w_o = (a_w_o[0] + a_w_x - STATUS_X,
             a_w_o[1] + a_w_y + PADDING)
    t_w_o = (a_w_o[0], a_w_o[1] + a_w_y + PADDING)

    m_dim_x = 2
    m_dim_y = 2
    m_w_x = cells_x * m_dim_x + 2*PADDING
    m_w_y = cells_y * m_dim_y + 2*PADDING
    status_y = max(STATUS_Y, 0)
    m_w_o = (PADDING, PADDING)
    r_monitor_window = (m_w_o, m_w_o[0] + m_w_x - 2*PADDING,
                        m_w_o[1] + m_w_y - 2*PADDING)

    v_dim_x = 30
    v_dim_y = 30
    v_w_o = (s_w_o[0] - 3 * (PADDING + v_dim_x), s_w_o[1])
    r_v_w = []
    r_v_w.append((v_w_o[0], v_w_o[1],
                  v_w_o[0] + v_dim_x, v_w_o[1] + v_dim_y))

    r_v_w.append((r_v_w[0][0] + PADDING + v_dim_x, v_w_o[1],
                  r_v_w[0][0] + PADDING +
                  2 * v_dim_x, v_w_o[1] + v_dim_y))

    r_v_w.append((r_v_w[1][0] + PADDING + v_dim_x, v_w_o[1],
                  r_v_w[1][0] + PADDING +
                  2 * v_dim_x, v_w_o[1] + v_dim_y))

    _bwidth = BWIDTH*16
    _bheight = 36
    b_w_o = []
    b_w_o.append((v_w_o[0] - 3*(PADDING+_bwidth), s_w_o[1]))
    b_w_o.append((v_w_o[0] - 2*(PADDING+_bwidth), s_w_o[1]))
    b_w_o.append((v_w_o[0] - 1*(PADDING+_bwidth), s_w_o[1]))
    b_w_o.append((v_w_o[0] - 3*(PADDING+_bwidth), s_w_o[1] + _bheight))
    b_w_o.append((v_w_o[0] - 2*(PADDING+_bwidth), s_w_o[1] + _bheight))
    b_w_o.append((v_w_o[0] - 1*(PADDING+_bwidth), s_w_o[1] + _bheight))

    text_x = b_w_o[0][0] - 2*PADDING

    _bwidth = BWIDTH*10
    color_buttons = {
          GREY: (b_w_o[0][0] - 5*(PADDING+_bwidth), s_w_o[1]),
          GREEN: (b_w_o[0][0] - 4*(PADDING+_bwidth), s_w_o[1]),
          ORANGE: (b_w_o[0][0] - 3*(PADDING+_bwidth), s_w_o[1]),
          BLUE: (b_w_o[0][0] - 2*(PADDING+_bwidth), s_w_o[1]),
          WHITE: (b_w_o[0][0] - 1*(PADDING+_bwidth), s_w_o[1])}

    main_x = PADDING * 2 + a_w_x
    main_y = PADDING * 3 + a_w_y + status_y

    # set windows and root parameters; only do this once controlled
    # by set_window
    logfile = 'snake_v5_2.log'
    logformat = '%(asctime)s:%(levelname)s:%(message)s'
    logger = set_logger(logfile, logformat, 'DEBUG')

    root = Tk()
    root.title("Snakes ...")
    root.geometry(f"{main_x}x{main_y}")
    root.configure(background='black')

    mroot = Tk()
    mroot.title("Monitor ...")
    mroot.geometry(f"{m_w_x}x{m_w_y}")
    mroot.configure(background='white')

    aw = Canvas(root, width=main_x, height=main_y, bg='grey')
    aw.place(x=0, y=0)

    label_SMB = []
    pause_SMB = ImageTk.PhotoImage(file='data/Pause.png')
    label_SMB.append(Label(aw, image=pause_SMB, bg='grey'))
    label_SMB[0].image = pause_SMB

    run_SMB = ImageTk.PhotoImage(file='data/Triangle.png')
    label_SMB.append(Label(aw, image=run_SMB, bg='grey'))
    label_SMB[1].image = run_SMB

    mw = Canvas(mroot, width=m_w_x, height=m_w_y, bg='white')
    mw.pack(fill=BOTH, expand=YES)

    # set some other parameters
    snake_length = 10  # this is the maximum snake length
    wall_v = []
    wall_v.append([(int(0.10*cells_x), int(0.10*cells_y)),
                   (int(0.10*cells_x), int(0.90*cells_y)),
                   (int(0.80*cells_x), int(0.90*cells_y)),
                   (int(0.80*cells_x), int(0.40*cells_y))])
    wall_v.append([(int(0.25*cells_x), int(0.25*cells_y)),
                   (int(0.65*cells_x), int(0.25*cells_y))])
    brick_size = (int(0.8*cell_dim_x), int(0.8*cell_dim_y))
    myfont = "Calibri 12"

    # setup view_field
    view_field = []
    view_field.append(((1, 0), (1, 1), (1, -1),
                       (2, 0), (2, 1), (2, -1)))       # -> E
    view_field.append(((1, 1), (1, 0), (0, 1),
                       (2, 2), (2, 1), (1, 2)))        # -> SE
    view_field.append(((0, 1), (-1, 1), (1, 1),
                       (0, 2), (-1, 2), (1, 2)))       # -> S
    view_field.append(((-1, 1), (0, 1), (-1, 0),
                       (-2, 2), (-1, 2), (-2, 1)))     # -> SW
    view_field.append(((-1, 0), (-1, 1), (-1, -1),
                       (-2, 0), (-2, 1), (-2, -1)))    # -> W
    view_field.append(((-1, -1), (-1, 0), (0, -1),
                       (-2, -2), (-2, -1), (-1, -2)))  # -> NW
    view_field.append(((0, -1), (1, -1), (-1, -1),
                       (0, -2), (1, -2), (-1, -2)))    # -> N
    view_field.append(((1, -1), (0, -1), (1, 0),
                       (2, -2), (1, -2), (2, -1)))     # -> NE

    def __repr__(cls):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in cls.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self='__class__'))+s
        return s


class Cell:
    '''  class Cell to represent the play environment and status with
         following methods:
         - __init__
         - cell_color
         - __repr__
    '''
    def __init__(self, i, j, plot, content):
        ''' method to initialise cell
        '''
        self.i = i
        self.j = j
        self.plot = plot
        self.content = content
        assert self.content in ['empty', 'wall', 'snake'], \
            "content is limited to empty, wall or snake"

    def cell_color(self):
        ''' method to set the cell color for display
        '''
        if self.content == 'empty':
            color = WHITE
        elif self.content == 'snake':
            color = RED
        elif self.content == 'wall':
            color = GREEN
        else:
            assert False, "this option can not be possible, check code"

        return color

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


class PlotObject:
    '''  class PlotObject to create a point with attibutes to be plotted
         Methods:
         - __init__
         - __repr__
    '''
    def __init__(self, origin, i, j, dimension, size, fcolor, ocolor, owidth,
                 shape):
        self.x1 = origin[0] + i * dimension[0]
        self.y1 = origin[1] + j * dimension[1]
        self.x2 = self.x1 + size[0]
        self.y2 = self.y1 + size[1]
        self.fcolor = fcolor
        self.ocolor = ocolor
        self.owidth = owidth
        self.shape = shape

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


class Monitor:
    '''  Class Monitor to handle functions of monitor display of status of cell
         Methods:
         - plot
         - clear
         - __repr__
    '''
    def __init__(self, cell):
        self.cell = cell

    def plot(self):
        '''  plot the cell status in the monitor window
             note only the head and the emptied tail need to be plotted so just
             2 per snake
        '''
        plotlist = []

        for i in range(setup.cells_x):
            for j in range(setup.cells_y):

                if self.cell[i][j].plot:
                    plotlist.append(PlotObject(origin=setup.m_w_o,
                                    i=self.cell[i][j].i, j=self.cell[i][j].j,
                                    dimension=(setup.m_dim_x, setup.m_dim_y),
                                    size=(setup.m_dim_x, setup.m_dim_y),
                                    fcolor=self.cell[i][j].cell_color(),
                                    ocolor='',
                                    owidth=0,
                                    shape='rectangle'))
                    self.cell[i][j].plot = False

        m = tools.plot_window(canvas=setup.mw,
                              rectangle=setup.r_monitor_window,
                              background='', border_color=BLACK,
                              border_width=2, plotlist=plotlist)

        setup.mroot.update()
        return m

    def clear(self, m_counter, monitor_clear):
        '''  method to clear the monitor bufffer
        '''
        m_counter += 1
        if (m_counter % monitor_clear == 0):
            setup.mw.delete("all")
            # m_counter = 0

            for i in range(setup.cells_x):
                for j in range(setup.cells_y):
                    if self.cell[i][j].content != 'empty':
                        self.cell[i][j].plot = True

        return m_counter

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


class Tools:
    '''   class with the methods:
          - init_cells
          - plot_window
          - plot_status
          - display_text
          - eye
          - randomvector
          - hex_color
          - __repr__
    '''
    def init_cells(self):
        '''  initialise the cells to capture status of the field
             Cell. cell.x and cell.y are the monitor cell positions
        '''
        cell = [[Cell(
                i, j,
                False, 'empty') for j in range(setup.cells_y)]
                for i in range(setup.cells_x)]
        return cell

    def plot_window(self, canvas, rectangle, background,
                    border_color, border_width, plotlist):
        '''  draw  window border and background, then plot all the points in
             the plot list
        '''
        canvas.create_rectangle(rectangle,
                                outline=self.hex_color(border_color),
                                fill=self.hex_color(background),
                                width=border_width)
        p = []
        for plotpoint in plotlist:
            if plotpoint.shape == 'rectangle':
                p.append(canvas.create_rectangle(plotpoint.x1, plotpoint.y1,
                         plotpoint.x2, plotpoint.y2,
                         fill=self.hex_color(plotpoint.fcolor),
                         outline=self.hex_color(plotpoint.ocolor),
                         width=plotpoint.owidth))

            elif plotpoint.shape == 'oval':
                p.append(canvas.create_oval(plotpoint.x1, plotpoint.y1,
                         plotpoint.x2, plotpoint.y2,
                         fill=self.hex_color(plotpoint.fcolor),
                         outline=self.hex_color(plotpoint.ocolor),
                         width=plotpoint.owidth))

            else:
                assert False, "shape can only be 'rectangle' or 'oval'"

        return p

    def plot_status(self, pause_status):
        '''  display status pause or run
        '''
        if pause_status:
            setup.label_SMB[0].lift()
            setup.label_SMB[0].place(x=setup.s_w_o[0], y=setup.s_w_o[1])

        else:
            setup.label_SMB[1].lift()
            setup.label_SMB[1].place(x=setup.s_w_o[0], y=setup.s_w_o[1])

    def display_text(self, t_elapsed, snakes, select):
        '''  display number snakes and time passed in seconds in status window
             left every 1 s and refresh the windows according to refresh_rate
        '''
        s_num = lambda x: str(x) if x > 0 else 'None'  # noqa: E731
        # display text only once a second
        if t_elapsed % 1000 < 80:
            text = 'Number of snakes: ' + s_num(snakes) + '\n' + \
                   'Selected snake: ' + s_num(select) + '\n' + \
                   'Elapsed time: ' + str(int(t_elapsed/1000)) + ' seconds.'
            label = Label(setup.aw, text=text, wraplength=setup.text_x,
                          bg='grey', font=setup.myfont, justify='left')
            label.place(x=setup.t_w_o[0], y=setup.t_w_o[1])

    def eye(self, head, cell, a):
        ''' captures a value of the view depending on looking vector a
        '''
        v = 0
        for i in range(len(a)):
            if cell[(head[0]+a[i][0]) % setup.cells_x][(head[1]+a[i][1]) %
               setup.cells_y].content != 'empty':
                if i == 0:
                    v = v + 4
                else:
                    v = v + 1
        return v

    def randomvector(self):
        ''' calculate a random vector ([-1,0-1],[-1,0,-1]) but not (0,0))
        '''
        vector = (0, 0)
        while vector == (0, 0):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            vector = (x, y)
        return vector

    def hex_color(self, color):
        ''' converts color (R, G, B) to a Hex string for tkinter
        '''
        if color != '':
            hcolor = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        else:
            hcolor = ''

        return hcolor

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


setup = Setup
tools = Tools()
