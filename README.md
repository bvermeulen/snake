# snake
further on pygame -snake moving on a surface

python 3.6

Author: Bruno Vermeulen
Email: bruno_vermeulen2001@yahoo.com

Config file (default name ~/data/config.txt or first argument):
pattern file (17:) string
frames/ second (17:) integer
cells x (17:) integer
cells y (17:) integer
cell dim x (17:) integer
cell dim y (17:) integer

Control keys:
- o             : border to orange
- b             : border to blue
- SPACE         : toggle between pause and run
- c             : clear snakes (time keeps running)
- ESC           : stop program
- X             : stop program
- Mouse pressed : either create or delete snake by pressing on the head 

Update for 24 April, functionality now contains:
- create and delete snakes
- implementation of snake eyes and vision
- possibility to include walls
- Status pannel showing:- run/ pause symbol, status text and cell monitor window
- program parameters are set in module snake_configuration.py

Outstanding
- implement field level (dimensions)
- show vision of one snake [first one created] in status pannel
- implement holes in the wallsnake can move to a new dimension
- implement wall elements where snake can bounce
- implement a steerable snake
- create walls interactively
