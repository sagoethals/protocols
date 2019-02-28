
"""
Exp
"""

#from vc_exp_dicho import *
from vc_experiment import *
from init_rig_multiclamp import *

do_experiment = not os.path.exists('Steps')

n_exp = 4

V0s = linspace(0., 15., n_exp) * mV

for V0 in V0s:
    #threshold_measurement_dicho(do_experiment, V0)
    #threshold_measurement_dicho_first(do_experiment, V0)
    threshold_measurement_ASA_experiment(do_experiment, V0)