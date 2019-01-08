#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

A code to run a Na activation protocol, either with a neuron model or in a true experiment.
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

sleep(1)

# usual step protocol
vc_act = voltage_clamp_acti(amp, model=model)
print 'Total time:', len(vc_act[0])*(len(vc_act[0][0])*dt + 1*second)
# dichotomy method (pblm: being sure of capturing the peak axonal current and the baseline current)
vc_act_dicho = measure_threshold_dichotomy(amp, model=model)
print 'Total time:', len(vc_act_dicho[0])*(len(vc_act_dicho[0][0])*dt + 1*second)
#savez(date + cell + '02' + rec, Vc=vc_act[0], I=vc_act[1], time=vc_act[2])
    
show(block=True)

# PLot IV curve for the two techniques
start = int(60.40*ms/dt)
end = int(79.0*ms/dt)
idx_peaks = []
i_peaks = []
v_peaks = []

for i in range(len(vc_act[0])): 
    Is = vc_act[1][i] 
    peak = argmin(Is[start:end]) + start
    #print peak
    idx_peaks.append(peak)
    i_peaks.append(Is[peak])
    v_peaks.append(vc_act[0][i][700])

idx_peaks_dicho = []
i_peaks_dicho = []
v_peaks_dicho = []

for i in range(len(vc_act_dicho[0])): 
    Is = vc_act_dicho[1][i] 
    peak = argmin(Is[start:end]) + start
    #print peak
    idx_peaks_dicho.append(peak)
    i_peaks_dicho.append(Is[peak])
    v_peaks_dicho.append(vc_act_dicho[0][i][700])
    
#idx_th = where(array(i_peaks)>=-200.)[0][-1]
#v_threshold = vs[idx_th]
#peak_i = i_peaks[idx_th+1] - i_peaks[idx_th]

figure('IV curve')
#plot(v_peaks, i_peaks, 'k-')
plot(v_peaks, i_peaks, '-o', color='black')
plot(v_peaks_dicho, i_peaks_dicho, 'ro')
xlabel('V (mV)', fontsize=16)
ylabel('Peak I (pA)', fontsize=16)
tight_layout()
  
show()

    
    
    
    
    
    
    
    
    
    
    
    
    
