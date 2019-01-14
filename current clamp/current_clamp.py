#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:52:35 2018

@author: sarah
"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/")

from devices import *
from pylab import *
from brianmodels import *

#ms = 0.001
#pA = 1e-12
#mV = 0.001
#volt = 1
#nA = 1e-9
#dt = 0.1 * ms
#pF = 1e-12
#MOhm = 1e6

model = True

if model:
    #amp = RCCell(500*MOhm, 20*ms/(500*MOhm), dt)
    from brian2 import *
    #defaultclock.dt = 0.01*ms
    #eqs = 'dV/dt = (500*Mohm*I-V)/(20*ms) : volt'
    dt = 0.1*ms
    #amp = BrianExperiment(eqs, namespace = {}, dt=dt)
    amp = AxonalInitiationModel()
#else:
#    board = NI()
#    board.sampling_rate = float(1/dt)
#    board.set_analog_input('primary', channel=0)
#    board.set_analog_input('secondary', channel=1)
#    board.set_analog_output('command', channel=0)
#
#    amp = MultiClampChannel()
#    amp.configure_board(board, primary='primary', secondary='secondary', command='command')
#
#    amp.set_bridge_balance(True)
#    Rs = amp.auto_bridge_balance()
#print "Bridge resistance:",Rs / 1e6

ntrials = 20
V = []
Ic = zeros(int(200 * ms / dt))*nA
for ampli in 0.5*linspace(-1,1,ntrials)*nA:
    Ic[int(10 * ms / dt):int(70 * ms / dt)] = ampli
    V.append(amp.acquire('V', I=Ic))

t = dt*arange(len(Ic))

#savetxt('data.txt',array(V)/mV)

for Vi in V:
    plot(t/ms, array(Vi) / mV)
show()
