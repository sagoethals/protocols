#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Patch clamp protocols.
"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
#sys.path.append("/Users/Romain/PycharmProjects/clamper/")

from devices import *  # no need with the model
from pylab import *
from brian2 import * # need to be removed for actual recording
from time import sleep

# For true recordings:
ms = 0.001
pA = 1e-12
mV = 0.001
volt = 1
nA = 1e-9
pF = 1e-12
MOhm = 1e6

#dt = 0.02 * ms

def test_pulse(amp, model = False):

    sleep(1)
    if model == False:
        dt = 0.02*ms
    else:
        dt = 0.1*ms

    Vc = 0 * ones(int(40 * ms / dt)) * volt
    I = []
    Vc[int(10 * ms / dt):int(20 * ms / dt)] = -10 * mV
    Vc[int(20 * ms / dt):int(30 * ms / dt)] = +10 * mV
    I.append(amp.acquire('I', V=Vc))
    t = dt*arange(len(Vc))
    
    figure('Test pulses')
    for Ii in I:
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        ylabel('I (pA)')
        subplot(212)
        plot(t/ms, Vc/mV)
        ylabel('Vc (mV)')
        xlabel('t (ms)')
        pause(0.05)
        
    return Vc, I, t/ms

def measure_threshold_steps(amp, model = False, v_start = -60.*mV, v_range = 4.*mV, v_rest = -80.*mV):
    """
    A voltage step protocol to measure accurately the threshold:
        v_start: voltage of the first step
        v_step: v_start + v_step is the voltage of the last step
        v_rest: clamping voltage before the steps
        
    """
    
    print 'Starting a threshold measurement protocol'
    
    if model == False:
        dt = 0.02*ms
    else:
        dt = 0.1*ms
    
    ntrials = 11
    amplis = linspace(v_start, v_start + v_range, ntrials)
    Vc = v_rest*ones(int(250 * ms / dt))
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
                         
    vr_label = v_rest/mV
    figure('Threshold with small steps V0=%s' %vr_label)
    for ampli in amplis:
        sleep(1) # 1 second between each voltage step
        print ampli
        Vc[int(200 * ms / dt):int(220 * ms / dt)] = ampli
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        ylabel('I (pA)')
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        ylabel('Vc (mV)')
        xlabel('t (ms)')
        pause(0.05)
        
    return Vcs, I, t/ms

def Na_activation_with_threshold(amp, model = False, v_rest = -80.*mV):
    """
    A VC step protocol to measure Na currents:
        v_rest: clamping voltage before the steps
    """
    
    print 'Starting Na activation protocol'
    
    if model == False:
        dt = 0.02*ms
        ntrials=11
        #amplis = linspace(-60,-20, ntrials)*mV
        amplis = linspace(20, 60, ntrials) * mV
    else:
        dt = 0.1*ms
        ntrials=16
        amplis = linspace(-80,-20, ntrials)*mV
        
    Vc = v_rest * ones(int(250 * ms / dt))
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    I_peaks = []
                         
    vr_label = v_rest/mV
    figure('VC Na activation V0=%s' %vr_label)
    for ampli in amplis:
        sleep(1) # 1 second between each voltage step
        print ampli
        Vc[int(200 * ms / dt):int(220 * ms / dt)] = ampli
        #I.append(amp.acquire('I', V=Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        I_peaks.append(min(I[-1][int(200.4 * ms / dt):int(219 * ms / dt)]))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        ylabel('I (pA)')
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        ylabel('Vc (mV)')
        xlabel('t (ms)')
        pause(0.05)
    
    print I_peaks
    idx_th = where(array(I_peaks)<=-400.)[0][0]  #it finds the peak axonal current !!! exact value has to be changed for CGC
    print idx_th, I_peaks[idx_th]
    v_threshold = Vcs[idx_th - 1][int(210 * ms / dt)] * mV
    print 'Rough threshold:', v_threshold
    
    data_threshold = measure_threshold_steps(amp, model = model, v_start = v_threshold, v_range = amplis[1] - amplis[0], v_rest = v_rest)

    return Vcs, I, t/ms, data_threshold

def Na_deactivation(amp, model = False):
    if model == False:
        dt = 0.02*ms
        ntrials=31
        #amplis = linspace(-30,-90, ntrials)*mV
        amplis = linspace(50, -10, ntrials) * mV
    else:
        dt = 0.01*ms
        ntrials=21
        amplis = linspace(-40,-100, ntrials)*mV

    Vc = -0.08*ones(int(140 * ms / dt))*volt
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    
    figure('VC Deactivation')
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(i) for i in np.linspace(0, 1, ntrials)]
    for i in range(ntrials):
        ampli = amplis[i]
        sleep(1)
        print ampli
        Vc[int(100 * ms / dt):int(100.02 * ms / dt)] = -50.* mV  #the time depends on the recording temperature, for CGC at RT 200 µs should be OK
        Vc[int(100.02 * ms / dt):int(120. * ms / dt)] = ampli
        #I.append(amp.acquire('I', V=Vc))
        #Vcs.append(array(Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA, color = colors[i])
        ylabel('I (pA)')
        subplot(212)
        plot(t/ms, array(Vc) / mV, color = colors[i])
        ylabel('Vc (mV)')
        xlabel('t (ms)')
        pause(0.05)
        
    return Vcs, I, t/ms

def measure_threshold_with_prepulse(amp, model = False, v_start = -60.*mV, v_range = 4.*mV, v_rest = -80.*mV):
    """
    A voltage step protocol to measure accurately the threshold with a prepulse to remove inactivation:
        v_start: voltage of the first step
        v_step: v_start + v_step is the voltage of the last step
        v_rest: clamping voltage before the steps
        
    """
    
    print 'Starting a threshold measurement protocol with prepulse'
    
    if model == False:
        dt = 0.02*ms
    else:
        dt = 0.1*ms
    
    ntrials = 11
    amplis = linspace(v_start, v_start + v_range, ntrials)
    
    Vc = v_rest*ones(int(200 * ms / dt))
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    I_peaks = []
                         
    figure('Threshold with small steps with prepulse')
    for ampli in amplis:
        sleep(1) # 1 second between each voltage step
        print ampli
        Vc[int(50 * ms / dt):int(150 * ms / dt)] = -100.*mV
        Vc[int(150 * ms / dt):int(170 * ms / dt)] = ampli
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        I_peaks.append(min(I[-1][int(150.4 * ms / dt):int(169 * ms / dt)]))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        pause(0.05)
    
    print I_peaks
    idx_th = where(array(I_peaks)<=-1000.)[0][0]  #it finds the peak axonal current !!! exact value has to be changed for CGC
    print idx_th, I_peaks[idx_th]
    v_threshold = Vcs[idx_th - 1][int(160 * ms / dt)] * mV
    print 'Rough threshold:', v_threshold
    
    return Vcs, I, t/ms, v_threshold

def Na_activation_with_threshold_prepulse(amp, model = False, v_rest = -80.*mV):
    """
    A VC step protocol to measure Na currents with a prepulse to remove inactivation:
        v_rest: clamping voltage before the steps
    """
    
    print 'Starting Na activation protocol with prepulse'
    
    if model == False:
        dt = 0.02*ms
        ntrials=11
        amplis = linspace(-60,-20, ntrials)*mV
    else:
        dt = 0.1*ms
        ntrials=16
        amplis = linspace(-80,-20, ntrials)*mV
        
    Vc = v_rest * ones(int(200 * ms / dt))
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    I_peaks = []
                         
    figure('VC Na activation with prepulse')
    for ampli in amplis:
        sleep(1) # 1 second between each voltage step
        print ampli
        Vc[int(50 * ms / dt):int(150 * ms / dt)] = -100.*mV
        Vc[int(150 * ms / dt):int(170 * ms / dt)] = ampli
        #I.append(amp.acquire('I', V=Vc))
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        I_peaks.append(min(I[-1][int(150.4 * ms / dt):int(169 * ms / dt)]))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        pause(0.05)
    
    print I_peaks
    idx_th = where(array(I_peaks)<=-1000.)[0][0]  #it finds the peak axonal current !!! exact value has to be changed for CGC
    print idx_th, I_peaks[idx_th]
    v_threshold = Vcs[idx_th - 1][int(160 * ms / dt)] * mV
    print 'Rough threshold:', v_threshold
    
    data_threshold = measure_threshold_with_prepulse(amp, model = model, v_start = v_threshold, v_range = amplis[1] - amplis[0], v_rest = v_rest)

    return Vcs, I, t/ms, data_threshold

def repeat_v_step_with_prepulse(amp, model = False, v_step = -60.*mV, v_rest = -80.*mV, n_rep = 50):
    """
    A voltage step protocol to measure accurately the threshold with a prepulse to remove inactivation:
        v_start: voltage of the step
        v_rest: clamping voltage before the steps
        
    """
    
    print 'Starting repeated single step protocol'
    
    if model == False:
        dt = 0.02*ms
    else:
        dt = 0.1*ms

    Vc = v_rest*ones(int(200 * ms / dt))
    t = dt*arange(len(Vc))
    I = []
    Vcs = []
    n_trial = 0
                         
    figure('Single step with prepulse')
    while n_trial < n_rep:
        print n_trial
        sleep(1) 
        Vc[int(50 * ms / dt):int(150 * ms / dt)] = -100.*mV
        Vc[int(150 * ms / dt):int(170 * ms / dt)] = v_step
        Ii = amp.acquire('I', V=Vc)
        I.append(Ii/pA)
        Vcs.append(array(Vc/mV))
        
        subplot(211)
        plot(t/ms, array(Ii) / pA)
        subplot(212)
        plot(t/ms, array(Vc) / mV)
        pause(0.05)
        
        n_trial += 1
    
    return Vcs, I, t/ms

#def voltage_clamp_acti(amp, model = False):
#    if model == False:
#        dt = 0.02*ms
#        ntrials=21
#        amplis = linspace(-60,-20, ntrials)*mV
#    else:
#        dt = 0.1*ms
#        ntrials=31
#        amplis = linspace(-80,-20, ntrials)*mV
#        
#    Vc = -0.08*ones(int(100 * ms / dt))*volt
#    #Vc = zeros(int(60 * ms / dt)) * volt
#    t = dt*arange(len(Vc))
#    I = []
#    Vcs = []
#                         
#    figure('VC - Activation')
#    for ampli in amplis:
#        sleep(1) # 1 second between each voltage step
#        print ampli
#        Vc[int(60 * ms / dt):int(80 * ms / dt)] = ampli
#        #I.append(amp.acquire('I', V=Vc))
#        Ii = amp.acquire('I', V=Vc)
#        I.append(Ii/pA)
#        Vcs.append(array(Vc/mV))
#        
#        subplot(211)
#        plot(t/ms, array(Ii) / pA)
#        subplot(212)
#        plot(t/ms, array(Vc) / mV)
#        pause(0.05)
#        
#    return Vcs, I, t/ms

#def measure_threshold_dichotomy(amp, model = False, v_start = -60.*mV, v_rest = -80.*mV):
#    if model == False:
#        dt = 0.02*ms
#    else:
#        dt = 0.1*ms
#    
#    Vc = v_rest*ones(int(250 * ms / dt))
#    t = dt*arange(len(Vc))
#    I = []
#    Vcs = []
#    
#    # values for the AP model, not adapted to CGC
#    ampli_min = -80*mV
#    ampli_current = v_start
#    ampli_max = -40*mV
#    spike = False
#    
#    vr_label = v_rest/mV                     
#    figure('Threshold with dichotomy - V0=%s' %vr_label)
#    
#    while True:
#        sleep(1) # 1 second between each voltage step
#        print ampli_current
#        Vc[int(200 * ms / dt):int(220 * ms / dt)] = ampli_current
#        #I.append(amp.acquire('I', V=Vc))
#        Ii = amp.acquire('I', V=Vc)
#        I.append(Ii/pA)
#        Vcs.append(array(Vc/mV))
#        
#        subplot(211)
#        plot(t/ms, array(Ii) / pA)
#        subplot(212)
#        plot(t/ms, array(Vc) / mV)
#        pause(0.05)
#        
#        i_max = max(abs(Ii[int(200.4 * ms / dt):int(219 * ms / dt)]))
#        print i_max
#        
#        if i_max >= 0.5*nA and abs(ampli_current - ampli_min) <= 0.5*mV and spike == False:
#            print 'stop'
#            break
#        if i_max <= 0.5*nA:
#            ampli_min = ampli_current
#            spike = False
#        else: 
#            ampli_max = ampli_current
#            spike = True
#            
#        ampli_current = 0.5*ampli_max + 0.5*ampli_min
#        
#    return Vcs, I, t/ms


#def voltage_clamp_acti_with_dicho(amp, model = False, v_rest = -80.*mV):
#    if model == False:
#        dt = 0.02*ms
#        ntrials=21
#        amplis = linspace(-60,-20, ntrials)*mV
#    else:
#        dt = 0.1*ms
#        ntrials=31
#        amplis = linspace(-80,-20, ntrials)*mV
#        
#    Vc = v_rest * ones(int(250 * ms / dt))
#    t = dt*arange(len(Vc))
#    I = []
#    Vcs = []
#    I_peaks = []
#                         
#    vr_label = v_rest/mV
#    figure('VC - activation - V0=%s' %vr_label)
#    for ampli in amplis:
#        sleep(1) # 1 second between each voltage step
#        print ampli
#        Vc[int(200 * ms / dt):int(220 * ms / dt)] = ampli
#        #I.append(amp.acquire('I', V=Vc))
#        Ii = amp.acquire('I', V=Vc)
#        I.append(Ii/pA)
#        Vcs.append(array(Vc/mV))
#        I_peaks.append(min(I[-1][int(200.4 * ms / dt):int(219 * ms / dt)]))
#        
#        subplot(211)
#        plot(t/ms, array(Ii) / pA)
#        subplot(212)
#        plot(t/ms, array(Vc) / mV)
#        pause(0.05)
#    
#    print I_peaks
#    idx_th = where(array(I_peaks)<=-500.)[0][0]  #it finds the peak axonal current
#    print idx_th, I_peaks[idx_th]
#    v_threshold = Vcs[idx_th - 1][int(210 * ms / dt)] * mV
#    print 'Rough threshold:', v_threshold
#    
#    # dichotomy method
#    data_threshold = measure_threshold_dichotomy(amp, model = model, v_start = v_threshold, v_rest = v_rest)
#
#    return Vcs, I, t/ms, data_threshold



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



















