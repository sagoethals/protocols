'''
Initializes for model running mode.

'''

import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")

from brian2 import *
from brianmodels import *

dt = 0.01*ms
board = AxonalInitiationModel() #RC_and_electrode(Ce = 3*pF)
amplifier = board
