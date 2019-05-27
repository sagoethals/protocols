
"""
Run a protocol to measure the threshold in a BrianModel.
"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clampy/")
sys.path.append("/home/sarah/Documents/repositories/protocols/VC_experiment_CGC/")
sys.path.append("/home/sarah/Documents/repositories/protocols/")

import os
from brian2 import *
from clampy import *
from threshold_adaptation_dichotomy_staircase_method_CGC import *
from init_model import *

do_experiment = not os.path.exists('Steps')

n_exp = 1

V0s = linspace(0., 35., n_exp) * mV

for V0 in V0s:
    #threshold_measurement_dicho_model(do_experiment, V0)
    threshold_measurement_dichotomy_staircase(do_experiment, Vh = -75.*mV, V0 = V0, i_threshold = 1*nA)