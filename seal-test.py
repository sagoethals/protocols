
"""
Seal-test to monitor the different steps in a patch experiment.
"""
import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/")

from devices import *
from pylab import *
from brianmodels import *

from datetime import datetime
from time import sleep

date = datetime.now().strftime("%Y%m%d")

model = True

if model:
    from brian2 import *
    defaultclock.dt = 0.01*ms
    eqs = 'dV/dt = (500*Mohm*I-V)/(20*ms) : volt'
    #dt = 0.1*ms
    amp = BrianExperiment(eqs, namespace = {}, dt=dt)
    #amp = AxonalInitiationModel()
else:
    ms = 0.001
    pA = 1e-12
    mV = 0.001
    volt = 1
    nA = 1e-9
    dt = 0.1 * ms
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


ion()

fig = figure('1')

while fignum_exists('1'):
    sleep(1)
    Vc = zeros(int(100 * ms / dt))*volt
    I = []
    Vc[int(40 * ms / dt):int(60 * ms / dt)] = 10 * mV
    I.append(amp.acquire('I', V=Vc))
    t = dt*arange(len(Vc))
    
    ylim(-100,100)
    for Ii in I:
        plot(t/ms, array(Ii) / pA)
        pause(0.05)
    show()