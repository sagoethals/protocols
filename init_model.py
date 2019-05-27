'''
Initializes for model running mode.

'''

import sys
sys.path.append("/home/sarah/Documents/repositories/clampy/") #clampy/clampy/")

from clampy import *
from brian2 import *
from clampy.brianmodels import *

dt = 0.02*ms
board = AxonalInitiationModel() #RC_and_electrode(Ce = 3*pF)
amplifier = board
board.set_aliases(Ic='I', Ic1='I', Vc='Vc', V1='V', V2='V', I_TEVC='I', Vext='V')