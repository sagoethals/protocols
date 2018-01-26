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
from time import sleep

#ms = 0.001
#pA = 1e-12
#mV = 0.001
#volt = 1
#nA = 1e-9
dt = 0.1 * ms
#pF = 1e-12
#MOhm = 1e6

def test_pulse(amp):
    Vc = -0.07*ones(int(100 * ms / dt))*volt
    I = []
    Vc[int(20 * ms / dt):int(30 * ms / dt)] = -80 * mV
    Vc[int(30 * ms / dt):int(40 * ms / dt)] = -60 * mV
    I.append(amp.acquire('I', V=Vc))
    t = dt*arange(len(Vc))
    
    figure('Test pulses')
    for Ii in I:
        subplot(211)
        plot(t/ms, array(Ii) / pamp)
        subplot(212)
        plot(t/ms, Vc/mV)
        
    return Vc/mV, I/pamp, t/ms

def voltage_clamp_acti(amp):
    ntrials=31
    Vc = -0.07*ones(int(60 * ms / dt))*volt
    I = []
    Vcs = []
    for ampli in linspace(-100,20,ntrials)*mV:
        sleep(1)
        print ampli
        Vc[int(20 * ms / dt):int(40 * ms / dt)] = ampli
        I.append(amp.acquire('I', V=Vc))
        Vcs.append(array(Vc))
    t = dt*arange(len(Vc))

    figure('VC - Activation')
    for Ii in I:
        subplot(211)
        plot(t/ms, array(Ii) / pamp)
    for Vci in Vcs:
        subplot(212)
        plot(t/ms, array(Vci) / mV)
        
    return Vcs/mV, I/pamp, t/ms

def voltage_clamp_deacti(amp):
    ntrials = 31
    Vc = -0.07*ones(int(65 * ms / dt))*volt
    I = []
    Vcs = []
    for ampli in linspace(20,-100,ntrials)*mV:
        print ampli
        sleep(1)
        Vc[int(20 * ms / dt):int(25 * ms / dt)] = 20 * mV
        Vc[int(25 * ms / dt):int(45 * ms / dt)] = ampli
        I.append(amp.acquire('I', V=Vc))
        Vcs.append(array(Vc))
    t = dt*arange(len(Vc))

    figure('VC - Deactivation')
    for Ii in I:
        subplot(211)
        plot(t/ms, array(Ii) / pamp)
    for Vci in Vcs:
        subplot(212)
        plot(t/ms, array(Vci) / mV)
        
    return Vcs/mV, I/pamp, t/ms

def voltage_clamp_threshold_adapt(amp):
    nstarts = 11
    ntrials = 21
    T = 60 * ms
    I = []
    Vcs = []
    for V0 in linspace(-80,-60,nstarts)*mV:
        Vc = V0 * ones(int(T / dt))
        for ampli in linspace(-80,-40,ntrials)*mV:
            print V0, ampli
            sleep(1)
            Vc[int(20 * ms / dt):int(40 * ms / dt)] = ampli
            I.append(amp.acquire('I', V=Vc))
            Vcs.append(array(Vc))
    t = dt*arange(len(Vc))
    
    figure('VC - threshold adaptation')
    for Ii in I:
        subplot(211)
        plot(t/ms, array(Ii) / pamp)
    for Vci in Vcs:
        subplot(212)
        plot(t/ms, array(Vci) / mV)

    return Vcs/mV, I/pamp, t/ms

def current_clamp(amp):
    ntrials = 21
    V = []
    Ics = []
    Ic = zeros(int(45 * ms / dt))*nA
    for ampli in 0.5*linspace(-1,1,ntrials)*nA:
        print ampli
        sleep(1)
        Ic[int(20 * ms / dt):int(25 * ms / dt)] = ampli
        V.append(amp.acquire('V', I=Ic))
        Ics.append(array(Ic))

    t = dt*arange(len(Ic))

    figure('Current clamp')
    for Vi in V:
        subplot(211)
        plot(t/ms, array(Vi) / mV)
    for Ici in Ics:
        subplot(212)
        plot(t/ms, Ici / pamp)

    return Ics/pamp, V/mV, t/ms

def current_pulse(amp):
    ntrials = 5
    V = []
    Ic = zeros(int(45 * ms / dt))*nA
    for i in range(ntrials):
        sleep(1)
        Ic[int(20 * ms / dt):int(25 * ms / dt)] = 0.2*nA
        V.append(amp.acquire('V', I=Ic))

    t = dt*arange(len(Ic))

    figure('Current clamp')
    for Vi in V:
        subplot(211)
        plot(t/ms, array(Vi) / mV)
        subplot(212)
    plot(t/ms, Ic / pamp)

    return Ic/pamp, V/mV, t/ms



















