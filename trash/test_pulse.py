#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:11:22 2018

@author: sarah
"""

from devices import *
from pylab import *
from protocols import test_pulse

ms = 0.001
pA = 1e-12
mV = 0.001
volt = 1
nA = 1e-9
dt = 0.1 * ms
pF = 1e-12
MOhm = 1e6

model = True

if model:
    amp = RCCell(500*MOhm, 20*ms/(500*MOhm), dt)
else:
    board = NI()
    board.sampling_rate = float(1/dt)
    board.set_analog_input('primary', channel=0)
    board.set_analog_input('secondary', channel=1)
    board.set_analog_output('command', channel=0)

    amp = MultiClampChannel()
    amp.configure_board(board, primary='primary', secondary='secondary', command='command')

    amp.set_bridge_balance(True)
    Rs = amp.auto_bridge_balance()
    
#print "Bridge resistance:",Rs / 1e6

#Vc = zeros(int(100 * ms / dt))
#I = []
#
#Vc[:int(20 * ms / dt)] = -60 * mV
#Vc[int(20 * ms / dt):int(30 * ms / dt)] = -70 * mV
#Vc[int(30 * ms / dt):int(40 * ms / dt)] = -50 * mV
#Vc[int(40 * ms / dt):] = -60 * mV
#
#I.append(amp.acquire('I', V=Vc))
#
#t = dt*arange(len(Vc))
#
##savetxt('data_test_pulse.txt',array(Vc)/mV)
#
#for Ii in I:
#    plot(t/ms, array(Ii) / mV)
#show()

result = test_pulse(amp)



