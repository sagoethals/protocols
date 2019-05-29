
"""

To run the threshold adaptation protocol for holding potentials ranging form 0 to 15 mV above the resting holding potential (-80 mV for CGC).

Different methods can be used to measure the threshold:
- large regular steps followed by small regular steps,
- large regular steps followed by dichotomy around the gross threshold,
- dichotomy followed by small regular steps around the gross threshold,
- dichotomy method followed by a staircase procedure around the gross threshold


"""

import os
from brian2 import *
from VC_experiment_CGC import *
from init_multiclamp import *

do_experiment = not os.path.exists('Steps')

n_exp = 4

V0s = linspace(0., 15., n_exp) * mV

for V0 in V0s:
    threshold_adaptation_dichotomy_staircase_method_CGC(do_experiment, amplifier, model=False, V0=V0)