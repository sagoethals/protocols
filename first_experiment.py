#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:44:38 2018

@author: sarah

First experiment: we switch between
- peak axonal current measurements
- threshold measurements

"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/")

from devices import *
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
    eqs = 'dV/dt = (500*Mohm*I-V)/(20*ms) : volt'
    dt = 0.1*ms
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

cell = 2
nrec = 2

ion()

for rec in range(nrec):
    close('all')
    rec = str(rec).zfill(2)
    cell = str(cell).zfill(2)
    sleep(1)
    print 'Current pulse'
    cp = current_pulse(amp)
    savez(date + cell + '00' + rec, Ic=cp[0], V=cp[1][0], time=cp[2] )
    sleep(1)
#    print 'Starting current clamp protocol'
#    cc = current_clamp(amp)
#    savez(date + cell + '05' + rec, Ic=cc[0], V=cc[1][0], time=cc[2] )
#    sleep(1)
    print 'Starting test pulse protocol'
    tp = test_pulse(amp)
    savez(date + cell + '01' + rec, Vc=tp[0], I=tp[1][0], time=tp[2] )
    sleep(1)
    print 'Starting VC activation protocol'
    vc_act = voltage_clamp_acti(amp)
    savez(date + cell + '02' + rec, Vc=vc_act[0], I=vc_act[1][0], time=vc_act[2])
    sleep(1)
    print 'Starting VC deactivation protocol'
    vc_deact = voltage_clamp_deacti(amp)
    savez(date + cell + '03' + rec, Vc=vc_deact[0], I=vc_deact[1][0], time=vc_deact[2])
    sleep(1)
#    print 'Starting threshold adaptation protocol'
#    vc_ada = voltage_clamp_threshold_adapt(amp)
#    savez(date + cell + '04' + rec, Vc=vc_ada[0], I=vc_ada[1][0], time=vc_ada[2])
#    sleep(1)
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
