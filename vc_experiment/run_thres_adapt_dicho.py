
"""
Exp
"""

from vc_exp_dicho import *
from init_rig_multiclamp import *

do_experiment = not os.path.exists('Steps')

n_exp = 8

V0s = linspace(0., 35., n_exp) * mV

for V0 in V0s:
    threshold_measurement_dicho(do_experiment, V0)