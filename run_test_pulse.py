"""

Test pulse protocol.

"""

import sys
#sys.path.append("/Users/Romain/PycharmProjects/clamper/")
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")

#from devices import *
from pylab import *
from brianmodels import *
from protocols import *

from datetime import datetime
from time import sleep

date = datetime.now().strftime("%Y%m%d")

model = True

if model:
    from brian2 import *
    #defaultclock.dt = 0.01*ms
    #eqs = 'dV/dt = (500*Mohm*I-V)/(20*ms) : volt'
    dt = 0.1*ms
    #amp = BrianExperiment(eqs, namespace = {}, dt=dt)
    amp = AxonalInitiationModel()
else:
    ms = 0.001
    pA = 1e-12
    mV = 0.001
    volt = 1
    nA = 1e-9
    dt = 0.02 * ms
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
    print "Bridge resistance:",Rs / 1e6

cell = 1
nrec = 1

ion()

print 'Starting test pulse protocol'

for rec in range(nrec):
    rec = str(rec).zfill(2)
    cell = str(cell).zfill(2)
    sleep(1)
    
    tp = test_pulse(amp, model = model)
    #savez(date + cell + 'tp' + rec, Vc=tp[0], I=tp[1][0], time=tp[2] )
   
show(block=True)
