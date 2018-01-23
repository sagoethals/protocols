#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:09:50 2018

@author: sarah
"""

from devices import *
from pylab import *

ms = 0.001
pA = 1e-12
mV = 0.001
volt = 1
nA = 1e-9
dt = 0.1 * ms
pF = 1e-12
MOhm = 1e6

def test_pulse(amp, V1=-70 * mV, V2=-50 * mV):
    Vc = zeros(int(100 * ms / dt))
    I = []
    Vc[:int(20 * ms / dt)] = -60 * mV
    Vc[int(20 * ms / dt):int(30 * ms / dt)] = V1
    Vc[int(30 * ms / dt):int(40 * ms / dt)] = V2
    Vc[int(40 * ms / dt):] = -60 * mV
    I.append(amp.acquire('I', V=Vc))
    t = dt*arange(len(Vc))
    
    #savetxt('data_test_pulse.txt',array(Vc)/mV)

    for Ii in I:
        plot(t/ms, array(Ii) / mV)

def voltage_clamp_acti(amp, ntrials=30):
    Vc = zeros(int(100 * ms / dt))
    I = []
    for ampli in linspace(-100,20,ntrials)*mV:
        Vc[int(10 * ms / dt):int(70 * ms / dt)] = ampli
        I.append(amp.acquire('I', V=Vc))
    t = dt*arange(len(Vc))

    #savetxt('data_vc_inc.txt',array(Vc)/mV)

    for Ii in I:
        plot(t/ms, array(Ii) / mV)

def voltage_clamp_deacti(amp, ntrials = 30):
    Vc = zeros(int(100 * ms / dt))
    I = []
    for ampli in linspace(20,-100,ntrials)*mV:
        Vc[int(10 * ms / dt):int(15 * ms / dt)] = 20 * mV
        Vc[int(15 * ms / dt):int(75 * ms / dt)] = ampli
        I.append(amp.acquire('I', V=Vc))

    t = dt*arange(len(Vc))

    #savetxt('data_vc_dec.txt',array(Vc)/mV)

    for Ii in I:
        plot(t/ms, array(Ii) / mV)

def voltage_clamp_threshold_adapt(amp, nstarts = 10, ntrials = 20):
    T = 100 * ms
    I = []
    for V0 in linspace(-80,-60,nstarts)*mV:
        Vc = zeros(int(T / dt))
        for ampli in linspace(-80,-40,ntrials)*mV:
            Vc[:int(10 * ms / dt)] = V0
            Vc[int(10 * ms / dt):int(70 * ms / dt)] = ampli
            Vc[int(70 * ms / dt):] = V0
            I.append(amp.acquire('I', V=Vc))

    t = dt*arange(len(Vc))

    #savetxt('data_vc_dec.txt',array(Vc)/mV)

    for Ii in I:
        plot(t/ms, array(Ii) / mV)


