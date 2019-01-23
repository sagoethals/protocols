
"""

A code to run a threshold adaptation protocol, either with a neuron model or in a true experiment.
We measure the threshold thanks to 2 step protocols.

"""

import sys
sys.path.append("/Users/Romain/PycharmProjects/clamper/")
#sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")

from clamper.devices import *
from pylab import *
from clamper.brianmodels import *
from vc_experiment import *

from datetime import datetime
from time import sleep

date = datetime.now().strftime("%Y.%m.%d_%H.%M.%S_")

model = False

if model:
    from brian2 import *
    #defaultclock.dt = 0.01*ms
    #eqs = 'dV/dt = (500*Mohm*I-V)/(20*ms) : volt'
    dt = 0.1*ms #0.1*ms
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

rec = str(nrec).zfill(2)
cell = str(cell).zfill(2)

ion()

save_path = "/Users/Romain/PycharmProjects/protocols/data/"

if model: # lower threshold in the model
    vrs = linspace(-80., -70., 2)*mV
else: # higher threshold in CGC
    vrs = linspace(-80., -45., 9)*mV

for vr in vrs:
    vr_str = str(abs(vr/mV)).zfill(2)
    print 'Threshold adaptation protocol, Vr = ', vr 
    vc_act_full = Na_activation_with_threshold(amp, model=model, v_rest = vr)
    savez(save_path + date + cell  +  rec + '_VC adaptation_' + vr_str, Vc=vc_act_full[0], I=vc_act_full[1], time=vc_act_full[2], thresh = vc_act_full[3])
    
    show(block=True)
    
    # PLot IV curve for the two techniques
    start = int(200.40*ms/dt)
    end = int(219.0*ms/dt)
    idx_peaks = []
    i_peaks = []
    v_peaks = []
    
    for i in range(len(vc_act_full[0])): 
        Is = vc_act_full[1][i] 
        peak = argmin(Is[start:end]) + start
        #print peak
        idx_peaks.append(peak)
        i_peaks.append(Is[peak])
        v_peaks.append(vc_act_full[0][i][int(210. * ms / dt)])
    
    idx_peaks_dicho = []
    i_peaks_dicho = []
    v_peaks_dicho = []
    
    for i in range(len(vc_act_full[3][0])): 
        Is = vc_act_full[3][1][i] 
        peak = argmin(Is[start:end]) + start
        #print peak
        idx_peaks_dicho.append(peak)
        i_peaks_dicho.append(Is[peak])
        v_peaks_dicho.append(vc_act_full[3][0][i][int(210. * ms / dt)])
    
    figure('IV curve V0=%s' %vr_str)
    #plot(v_peaks, i_peaks, 'k-')
    plot(v_peaks, i_peaks, '-o', color='black')
    plot(v_peaks_dicho, i_peaks_dicho, 'ro')
    xlabel('V (mV)', fontsize=16)
    ylabel('Peak I (pA)', fontsize=16)
    tight_layout()
      
    show()

    
    
    
    
    
    
    
    
    
    
    
    
    
