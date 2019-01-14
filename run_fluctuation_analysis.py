
"""

A code to run a Na deactivation protocol, either with a neuron model or in a true experiment.
"""

import sys
#sys.path.append("/Users/Romain/PycharmProjects/clamper/")
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")

#from devices import *
from pylab import *
from brianmodels import *
from vc_protocols import *

from datetime import datetime
from time import sleep

date = datetime.now().strftime("%Y%m%d_%H:%M_")

model = True

if model:
    from brian2 import *
    #defaultclock.dt = 0.01*ms
    #eqs = 'dV/dt = (500*Mohm*I-V)/(20*ms) : volt'
    dt = 0.01*ms
    #amp = BrianExperiment(eqs, namespace = {}, dt=dt)
    amp = AxonalInitiationModel()
else:
    ms = 0.001
    pA = 1e-12
    mV = 0.001
    volt = 1
    nA = 1e-9
    dt = 0.02*ms #0.1 * ms
    pF = 1e-12
    MOhm = 1e6

    board = NI()
    board.sampling_rate = float(1/dt)
    board.set_analog_input('primary', channel=0)
    board.set_analog_input('secondary', channel=1)
    board.set_analog_output('command', channel=0)

    amp = MultiClampChannel()
    amp.configure_board(board, primary='primary', secondary='secondary', command='command')

    amp.set_bridge_balance(True)
    Rs = amp.auto_bridge_balance()
    print "Bridge resistance:", Rs / 1e6

cell = 1
nrec = 1

ion()

rec = str(nrec).zfill(2)
cell = str(cell).zfill(2)

sleep(1)

# Measure accurately the voltage 
vc_act = Na_activation_with_threshold_prepulse(amp, model=model, v_rest = -80.*mV)
#savez(date + cell + 'VCstep' + rec, Vc=vc_act_full[0], I=vc_act_full[1], time=vc_act_full[2], thresh = vc_act_full[3])
v_threshold = vc_act[3][3]

# We stimulate repetitively 1 mV above threshold to open Na channels at the AIS
rep_pulses = repeat_v_step_with_prepulse(amp, model=model, v_step = v_threshold + 1.*mV, v_rest = -80.*mV, n_rep = 5)
#savez(date + cell + 'fluct_ana' + rec, Vc=vc_act_full[0], I=vc_act_full[1], time=vc_act_full[2], thresh = vc_act_full[3])

show(block=True)

    
    
    
    
    
    
    
    
    
    
    
    
    
