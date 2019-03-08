#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 17:24:53 2019

@author: sarah
"""

# import sys
# sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
# sys.path.append("/home/sarah/Documents/repositories/protocols/")

from vc_experiment_pc import *
#from init_model import *
from init_multiclamp import *

do_experiment = not os.path.exists('Steps')

n_exp = 4

V0s = linspace(0., 15., n_exp) * mV

for V0 in V0s:
    #threshold_measurement(do_experiment)
    threshold_measurement_experiment_PC(do_experiment, V0)