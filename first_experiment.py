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
from datetime import datetime
date = datetime.now().strftime("%Y%m%d")

from devices import *
from pylab import *
from brianmodels import *
from protocols import *

model = True

if model:
    from brian2 import *
    #defaultclock.dt = 0.01*ms
    eqs = 'dV/dt = (500*Mohm*I-V)/(20*ms) : volt'
    dt = 0.1*ms
    amp = BrianExperiment(eqs, namespace = {}, dt=dt)
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

nrec = 1
#protocols = ['test_pulse'] #, 'voltage_clamp_acti', 'voltage_clamp_deacti', \
             #'voltage_clamp_threshold_adapt', 'current_clamp']

for rec in range(nrec):
    rec = str(rec)
    #no_stimulation(amp, 1000)
    print 'Starting test pulse protocol'
    tp = test_pulse(amp)
    savez(date + '_tp' + rec, Vc=tp[0], I=tp[1][0])
    #no_stimulation(amp, 10000)
    print 'Starting VC activation protocol'
    vc_act = voltage_clamp_acti(amp)
    savez(date + '_vcact' + rec, Vc=vc_act[0], I=vc_act[1][0])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
