#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:32:23 2018

@author: sarah
"""

from devices import *
from pylab import *
from protocols import voltage_clamp_threshold_adapt

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

#nstarts = 5
#ntrials = 20
#T = 100 * ms
#I = []
#for V0 in linspace(-80,-60,nstarts)*mV:
#    Vc = zeros(int(T / dt))
#    for ampli in linspace(-80,-40,ntrials)*mV:
#        Vc[:int(10 * ms / dt)] = V0
#        Vc[int(10 * ms / dt):int(70 * ms / dt)] = ampli
#        Vc[int(70 * ms / dt):] = V0
#        I.append(amp.acquire('I', V=Vc))
#
#t = dt*arange(len(Vc))
#
##savetxt('data_vc_dec.txt',array(Vc)/mV)
#
#for Ii in I:
#    plot(t/ms, array(Ii) / mV)
#show()

result = voltage_clamp_threshold_adapt(amp)