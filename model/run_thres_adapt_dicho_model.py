
"""
Model
"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
sys.path.append("/home/sarah/Documents/repositories/protocols/")

import os
from brian2 import *
from model import *
from init_model import *
#from init_rig_multiclamp import *

do_experiment = not os.path.exists('Steps')

n_exp = 2

V0s = linspace(0., 35., n_exp) * mV

for V0 in V0s:
    V0 = V0 - 75*mV # for model!
    threshold_measurement_dicho_model(do_experiment, V0)