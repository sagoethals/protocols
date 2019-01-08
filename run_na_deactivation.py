
"""

A code to run a Na deactivation protocol, either with a neuron model or in a true experiment.
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
    print "Bridge resistance:",Rs / 1e6

cell = 1
nrec = 1

ion()

rec = str(nrec).zfill(2)
cell = str(cell).zfill(2)

vc_deact = voltage_clamp_deacti(amp, model=model)
#savez(date + cell + 'deact' + rec, Vc=vc_act[0], I=vc_act[1], time=vc_act[2])
    
show(block=True)

# PLot IV curve 
start = int(40.07*ms/dt)
end = int(50.*ms/dt)
idx_peaks = []
i_peaks = []
v_peaks = []

for i in range(len(vc_deact[0])): 
    Is = vc_deact[1][i] 
    peak = argmin(Is[start:end]) + start
    #print peak
    idx_peaks.append(peak)
    i_peaks.append(Is[peak])
    v_peaks.append(vc_deact[0][i][5000])

figure('IV curve')
#plot(v_peaks, i_peaks, 'k-')
plot(v_peaks, i_peaks, '-o', color='black')
xlabel('V (mV)', fontsize=16)
ylabel('Peak I (pA)', fontsize=16)
tight_layout()
  
show()

    
    
    
    
    
    
    
    
    
    
    
    
    
