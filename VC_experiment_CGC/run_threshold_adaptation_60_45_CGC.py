

"""

To run the threshold adaptation protocol for holding potentials ranging form 20 to 35 mV above the resting holding potential (-80 mV for CGC).

Different methods can be used to measure the threshold:
- large regular steps followed by small regular steps,
- large regular steps followed by dichotomy around the gross threshold,
- dichotomy followed by small regular steps around the gross threshold,
- dichotomy method followed by a staircase procedure around the gross threshold

"""

from VC_experiment_CGC import *
from init_multiclamp import *

do_experiment = not os.path.exists('Steps')

n_exp = 4

V0s = linspace(20., 35., n_exp) * mV

for V0 in V0s:
    #threshold_measurement_regular_regular(do_experiment, V0)
    #threshold_measurement_dichotomy_regular(do_experiment, V0)
    #threshold_measurement_regular_dichotomy(do_experiment, V0)
    threshold_measurement_dichotomy_staircase(do_experiment, V0)