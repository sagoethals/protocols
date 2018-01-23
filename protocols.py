#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:09:50 2018

@author: sarah
"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/")

from devices import *
from pylab import *
from brian2 import *

#ms = 0.001
#pA = 1e-12
#mV = 0.001
#volt = 1
#nA = 1e-9
dt = 0.1 * ms
#pF = 1e-12
#MOhm = 1e6

def test_pulse(amp):
    Vc = zeros(int(100 * ms / dt))*volt
    I = []
    Vc[:int(20 * ms / dt)] = -60 * mV
    Vc[int(20 * ms / dt):int(30 * ms / dt)] = -70 * mV
    Vc[int(30 * ms / dt):int(40 * ms / dt)] = -50 * mV
    Vc[int(40 * ms / dt):] = -60 * mV
    I.append(amp.acquire('I', V=Vc))
    t = dt*arange(len(Vc))
    
    #savetxt(date + '_tp.txt',array(Vc)/mV)
    figure('tp')
    for Ii in I:
        plot(t/ms, array(Ii) / pamp)
        
    return Vc/mV, I/pamp

def voltage_clamp_acti(amp, ntrials=30):
    Vc = zeros(int(100 * ms / dt))*volt
    I = []
    for ampli in linspace(-100,20,ntrials)*mV:
        Vc[int(10 * ms / dt):int(70 * ms / dt)] = ampli
        I.append(amp.acquire('I', V=Vc))
    t = dt*arange(len(Vc))

    #savetxt('data_vc_inc.txt',array(Vc)/mV)
    figure('vc')
    for Ii in I:
        plot(t/ms, array(Ii) / pamp)
        
    return Vc/mV, I/pamp

def voltage_clamp_deacti(amp, ntrials = 30):
    Vc = zeros(int(100 * ms / dt))*volt
    I = []
    for ampli in linspace(20,-100,ntrials)*mV:
        Vc[int(10 * ms / dt):int(15 * ms / dt)] = 20 * mV
        Vc[int(15 * ms / dt):int(75 * ms / dt)] = ampli
        I.append(amp.acquire('I', V=Vc))

    t = dt*arange(len(Vc))

    #savetxt('data_vc_dec.txt',array(Vc)/mV)
    for Ii in I:
        plot(t/ms, array(Ii) / mV)
    
    return Vc, I

def voltage_clamp_threshold_adapt(amp, nstarts = 10, ntrials = 20):
    T = 100 * ms
    I = []
    for V0 in linspace(-80,-60,nstarts)*mV:
        Vc = zeros(int(T / dt))*volt
        for ampli in linspace(-80,-40,ntrials)*mV:
            Vc[:int(10 * ms / dt)] = V0
            Vc[int(10 * ms / dt):int(70 * ms / dt)] = ampli
            Vc[int(70 * ms / dt):] = V0
            I.append(amp.acquire('I', V=Vc))

    t = dt*arange(len(Vc))

    #savetxt('data_vc_dec.txt',array(Vc)/mV)
    
    for Ii in I:
        plot(t/ms, array(Ii) / mV)

    return Vc, I

def current_clamp(amp):
    ntrials = 20
    V = []
    Ic = zeros(int(200 * ms / dt))*nA
    for ampli in 0.1*linspace(-1,1,ntrials)*nA:
        Ic[int(10 * ms / dt):int(70 * ms / dt)] = ampli
        V.append(amp.acquire('V', I=Ic))

    t = dt*arange(len(Ic))

    #savetxt('data.txt',array(V)/mV)

    for Vi in V:
        plot(t/ms, array(Vi) / mV)

    return Ic, V




















