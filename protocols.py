#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Patch clamp protocols.
"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
#sys.path.append("/Users/Romain/PycharmProjects/clamper/")

#from devices import *  # no need with the model
from pylab import *
from brian2 import * # need to be removed for actual recording
from time import sleep

## For true recordings:
#ms = 0.001
#pA = 1e-12
#mV = 0.001
#volt = 1
#nA = 1e-9
#pF = 1e-12
#MOhm = 1e6

#dt = 0.02 * ms

def test_pulse(amp, model = False):
    if model == False:
        dt = 0.02*ms
    else:
        dt = 0.1*ms
        
    Vc = -0.08*ones(int(40 * ms / dt))*volt
    I = []
    Vc[int(10 * ms / dt):int(20 * ms / dt)] = -90 * mV
    Vc[int(20 * ms / dt):int(30 * ms / dt)] = -70 * mV
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

def voltage_clamp_acti(amp, model = False):
    if model == False:
        dt = 0.02*ms
        ntrials=21
        amplis = linspace(-60,-20, ntrials)*mV
    else:
        dt = 0.1*ms
        ntrials=31
        amplis = linspace(-80,-20, ntrials)*mV
        
    Vc = -0.08*ones(int(100 * ms / dt))*volt
    #Vc = zeros(int(60 * ms / dt)) * volt
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
                         
    figure('VC - Activation')
    for ampli in amplis:
        sleep(1) # 1 second between each voltage step
        print ampli
        Vc[int(60 * ms / dt):int(80 * ms / dt)] = ampli
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

def measure_threshold_dichotomy(amp, model = False, v_start = -60.*mV, v_rest = -80.*mV):
    if model == False:
        dt = 0.02*ms
    else:
        dt = 0.1*ms
    
    Vc = v_rest*ones(int(100 * ms / dt))
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    
    # values for the AP model, not adapted to CGC
    ampli_min = -80*mV
    ampli_current = v_start
    ampli_max = -40*mV
    spike = False
    
    vr_label = v_rest/mV                     
    figure('Threshold with dichotomy - V0=%s' %vr_label)
    
    while True:
        sleep(1) # 1 second between each voltage step
        print ampli_current
        Vc[int(60 * ms / dt):int(80 * ms / dt)] = ampli_current
        #I.append(amp.acquire('I', V=Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        pause(0.05)
        
        i_max = max(abs(Ii[int(60.4 * ms / dt):int(79 * ms / dt)]))
        print i_max
        
        if i_max >= 0.5*nA and abs(ampli_current - ampli_min) <= 0.5*mV and spike == False:
            print 'stop'
            break
        if i_max <= 0.5*nA:
            ampli_min = ampli_current
            spike = False
        else: 
            ampli_max = ampli_current
            spike = True
            
        ampli_current = 0.5*ampli_max + 0.5*ampli_min
        
    return Vcs, I, t/ms

def voltage_clamp_acti_with_dicho(amp, model = False, v_rest = -80.*mV):
    if model == False:
        dt = 0.02*ms
        ntrials=21
        amplis = linspace(-60,-20, ntrials)*mV
    else:
        dt = 0.1*ms
        ntrials=31
        amplis = linspace(-80,-20, ntrials)*mV
        
    Vc = v_rest * ones(int(100 * ms / dt))
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    I_peaks = []
                         
    vr_label = v_rest/mV
    figure('VC - activation - V0=%s' %vr_label)
    for ampli in amplis:
        sleep(1) # 1 second between each voltage step
        print ampli
        Vc[int(60 * ms / dt):int(80 * ms / dt)] = ampli
        #I.append(amp.acquire('I', V=Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        I_peaks.append(min(I[-1][int(60.4 * ms / dt):int(79 * ms / dt)]))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        pause(0.05)
    
    print I_peaks
    idx_th = where(array(I_peaks)<=-1000.)[0][0]  #it finds the peak axonal current
    print idx_th, I_peaks[idx_th]
    v_threshold = Vcs[idx_th - 1][700] * mV
    print 'Rough threshold:', v_threshold
    
    data_threshold = measure_threshold_dichotomy(amp, model = model, v_start = v_threshold, v_rest = v_rest)
        
    return Vcs, I, t/ms, data_threshold

def voltage_clamp_deacti(amp, model = False):
    if model == False:
        dt = 0.02*ms
        ntrials=31
        amplis = linspace(-30,-90, ntrials)*mV
    else:
        dt = 0.01*ms
        ntrials=21
        amplis = linspace(-30,-100, ntrials)*mV

    Vc = -0.08*ones(int(80 * ms / dt))*volt
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    figure('VC - Deactivation')
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(i) for i in np.linspace(0, 1, ntrials)]
    for i in range(ntrials):
        ampli = amplis[i]
        sleep(1)
        print ampli
        Vc[int(40 * ms / dt):int(40.05 * ms / dt)] = -20 * mV  #the time depends on the recording temperature, for CGC at RT 200 µs should be OK
        Vc[int(40.05 * ms / dt):int(60. * ms / dt)] = ampli
        #I.append(amp.acquire('I', V=Vc))
        #Vcs.append(array(Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA, color = colors[i])
        subplot(212)
        plot(t/ms, array(Vc) / mV, color = colors[i])
        pause(0.05)
        
    return Vcs, I, t/ms

#def voltage_clamp_threshold_adapt(amp):
#    nstarts = 6
#    ntrials = 21
#    T = 60 * ms
#    I = []
#    Vcs = []
#    for V0 in linspace(-80,-60,nstarts)*mV:
#        Vc = V0 * ones(int(T / dt))
#        t = dt*arange(len(Vc))
#        figure('Threshold adaptation V0=%s' %V0)
#        for ampli in linspace(-80,-40,ntrials)*mV:
#            print V0, ampli
#            sleep(1)
#            Vc[int(20 * ms / dt):int(40 * ms / dt)] = ampli
#            Ii = amp.acquire('I', V=Vc)
#            I.append(Ii)
#            Vcs.append(array(Vc))
#        
#            subplot(211)
#            plot(t/ms, array(Ii) / pA)
#            subplot(212)
#            plot(t/ms, array(Vc) / mV)
#            pause(0.05)
#
#    return Vcs, I, t/ms
#
#def current_clamp(amp):
#    ntrials = 21
#    V = []
#    Ics = []
#    Ic = zeros(int(150 * ms / dt))*nA
#    t = dt*arange(len(Ic))
#    figure('Current clamp')
#    for ampli in 0.15*linspace(-1,1,ntrials)*nA:
#        print ampli
#        sleep(1)
#        Ic[int(20 * ms / dt):int(70 * ms / dt)] = ampli
#        Vi = amp.acquire('V', I=Ic)
#        V.append(Vi/mV)
#        Ics.append(array(Ic/pA))
#
#        subplot(211)
#        plot(t/ms, array(Vi) / mV)
#        subplot(212)
#        plot(t/ms, Ic / pA)
#        pause(0.05)
#
#    return Ics, V, t/ms
#
#def current_pulse(amp, ntrials = 1, color = 'k'):
#    #ntrials = 5
#    V = []
#    Ics = []
#    Ic = zeros(int(45 * ms / dt))*nA
#    t = dt*arange(len(Ic))
#    figure('Current pulse')
#    for i in range(ntrials):
#        sleep(1)
#        Ic[int(20 * ms / dt):int(25 * ms / dt)] = 0.3*nA
#        Vi = amp.acquire('V', I=Ic)
#        V.append(Vi/mV)
#        Ics.append(array(Ic/pA))
#
#        subplot(211)
#        plot(t/ms, array(Vi) / mV, color = color)
#        subplot(212)
#        plot(t/ms, Ic / pA, color = color)
#        plot(t/ms, Ic / pA)
#        pause(0.05)
#
#    return Ics, V, t/ms



















