#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:09:50 2018

@author: sarah
"""

import sys
sys.path.append("/Users/Romain/PycharmProjects/clamper/")

from devices import *
from pylab import *
#from brian2 import *
from time import sleep

ms = 0.001
pA = 1e-12
mV = 0.001
volt = 1
nA = 1e-9
dt = 0.1 * ms
pF = 1e-12
MOhm = 1e6

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
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, Vc/mV)
        pause(0.05)
        
    return Vc, I, t/ms

def voltage_clamp_acti(amp):
    ntrials=31
    Vc = -0.07*ones(int(60 * ms / dt))*volt
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    figure('VC - Activation')
    for ampli in linspace(-100,20,ntrials)*mV:
        sleep(1) # 1 second between each voltage step
        print ampli
        Vc[int(20 * ms / dt):int(40 * ms / dt)] = ampli
        #I.append(amp.acquire('I', V=Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        pause(0.05)
        
    return Vcs, I, t/ms

def voltage_clamp_deacti(amp):
    ntrials = 31
    Vc = -0.07*ones(int(65 * ms / dt))*volt
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    figure('VC - Deactivation')
    for ampli in linspace(20,-100,ntrials)*mV:
        sleep(1)
        print ampli
        Vc[int(20 * ms / dt):int(25 * ms / dt)] = 20 * mV
        Vc[int(25 * ms / dt):int(45 * ms / dt)] = ampli
        #I.append(amp.acquire('I', V=Vc))
        #Vcs.append(array(Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        pause(0.05)
        
    return Vcs, I, t/ms

def voltage_clamp_threshold_adapt(amp):
    nstarts = 6
    ntrials = 21
    T = 60 * ms
    I = []
    Vcs = []
    for V0 in linspace(-80,-60,nstarts)*mV:
        Vc = V0 * ones(int(T / dt))
        t = dt*arange(len(Vc))
        figure('Threshold adaptation V0=%s' %V0)
        for ampli in linspace(-80,-40,ntrials)*mV:
            print V0, ampli
            sleep(1)
            Vc[int(20 * ms / dt):int(40 * ms / dt)] = ampli
            Ii = amp.acquire('I', V=Vc)
            I.append(Ii)
            Vcs.append(array(Vc))
        
            subplot(211)
            plot(t/ms, array(Ii) / pA)
            subplot(212)
            plot(t/ms, array(Vc) / mV)
            pause(0.05)

    return Vcs, I, t/ms

def current_clamp(amp):
    ntrials = 21
    V = []
    Ics = []
    Ic = zeros(int(150 * ms / dt))*nA
    t = dt*arange(len(Ic))
    figure('Current clamp')
    for ampli in 0.15*linspace(-1,1,ntrials)*nA:
        print ampli
        sleep(1)
        Ic[int(20 * ms / dt):int(70 * ms / dt)] = ampli
        Vi = amp.acquire('V', I=Ic)
        V.append(Vi/mV)
        Ics.append(array(Ic/pA))

        subplot(211)
        plot(t/ms, array(Vi) / mV)
        subplot(212)
        plot(t/ms, Ic / pA)
        pause(0.05)

    return Ics, V, t/ms

def current_pulse(amp):
    ntrials = 5
    V = []
    Ics = []
    Ic = zeros(int(45 * ms / dt))*nA
    t = dt*arange(len(Ic))
    figure('Current pulse')
    for i in range(ntrials):
        sleep(1)
        Ic[int(20 * ms / dt):int(25 * ms / dt)] = 0.2*nA
        Vi = amp.acquire('V', I=Ic)
        V.append(Vi/mV)
        Ics.append(array(Ic/pA))

        subplot(211)
        plot(t/ms, array(Vi) / mV)
        subplot(212)
        plot(t/ms, Ic / pA)
        pause(0.05)

    return Ics, V, t/ms



















