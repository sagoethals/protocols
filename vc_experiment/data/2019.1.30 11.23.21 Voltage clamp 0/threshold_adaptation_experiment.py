#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:45:20 2019

@author: sarah
"""

# import sys
# sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
# sys.path.append("/home/sarah/Documents/repositories/protocols/")

from clamper import *
from pylab import *
from clamper.brianmodels import *
from clamper.data_management import *
from clamper.signals import *
import os
import shutil
from time import sleep

#from init_model import *
from init_rig_multiclamp import *

ion()

do_experiment = not os.path.exists('Steps')

def threshold_measurement(do_experiment, V0 = 0.*mV):

    ### Look for the rough threshold
    print 'V0:', V0
    v0_label = V0/mV
    
    # Parameters
    ntrials = 11
    
    figure('VC steps V0=%s' %v0_label)
    
    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')
        path = 'data/'+date_time()+' Voltage clamp %i' %v0_label
        os.mkdir(path)
        
        # Saving current script
        shutil.copy('threshold_adaptation_experiment.py', path)
    
        # Experiment
        os.mkdir(path+'/Steps')
        I = []
        I_peaks = []
        Vc_peaks = []
        V = []
        for ampli in linspace(20,60,ntrials)*mV:
            sleep(1)
            print 'Amplitude ', ampli
            Vc = sequence([constant(200*ms, dt)*V0, #0*mV,
                           constant(20*ms, dt)*ampli,
                           constant(20*ms, dt)*V0]) #0*mV])
            Ii = amplifier.acquire('I', 'Vext', V=Vc)
            I.append(Ii[0])
            V.append(Ii[1])
            
            I_peaks.append(min(I[-1][int(200.02 * ms / dt):int(219 * ms / dt)]))
            Vc_peaks.append(Vc[int(210*ms/dt)])
            
            # Plotting
            t = dt*arange(len(Vc))
            
            subplot(211)
            plot(t/ms, array(Ii)[0] / nA)
            xlabel('Time (ms)')
            ylabel('Current (nA)')
            title('Response to voltage pulses')
            
            subplot(212)
            plot(t/ms, array(Ii)[1] / mV)
            xlabel('Time (ms)')
            ylabel('V (mV)')
            pause(0.05)
            
            tight_layout()
            
        show(block=True)
    
        # Save data
        savetxt(path+'/Steps/I.txt', array(I)/nA)
        savetxt(path+'/Steps/V.txt', array(V)/mV)
        savetxt(path+'/Steps/Vc.txt', array(Vc)/mV)
    
        # Save parameter values
        save_info(dict(amplitude=ampli/mV, duration=len(Vc)*dt/ms, dt=dt/ms),
                  path+'/vc_steps_experiment.info')
    else: # Loading the data after the experiment
        from setup.units import *
        path = '.'
        I = loadtxt(path+'/Steps/I.txt')*nA
        V = loadtxt(path+'/Steps/V.txt')*mV
        Vc = loadtxt(path + '/Steps/Vc.txt')*mV
     
    print I_peaks
    idx_th = where(array(I_peaks)<=-200.1e-12)[0][0]  #it finds the peak axonal current, units are A
    print idx_th, I_peaks[idx_th]
    v_threshold = Vc_peaks[idx_th] #V[idx_th - 1][int(210 * ms / dt)]
    print 'Rough threshold:', v_threshold

    show(block=False)

    ### Accurate determination of the threshold
    
    ntrials = 11
    
    figure('Threshold measurement V0=%s' %v0_label)
    
    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')
    
        # Experiment
        os.mkdir(path+'/small_Steps')
        I = []
        V = []
        for ampli in linspace(v_threshold, v_threshold + 4.*mV, ntrials):
            sleep(1)
            print 'Amplitude ', ampli
            Vc = sequence([constant(200*ms, dt)*V0, #0*mV,
                           constant(20*ms, dt)*ampli,
                           constant(20*ms, dt)*V0]) #0*mV])
            Ii = amplifier.acquire('I', 'Vext', V=Vc)
            I.append(Ii[0])
            V.append(Ii[1])
            
            # Plotting
            t = dt*arange(len(Vc))
            
            subplot(211)
            plot(t/ms, array(Ii)[0] / nA)
            #xlabel('Time (ms)')
            ylabel('Current (nA)')
            #title('Response to voltage pulses')
            
            subplot(212)
            plot(t/ms, array(Ii)[1] / mV)
            xlabel('Time (ms)')
            ylabel('V (mV)')
            pause(0.05)
            
            tight_layout()
            
        show(block=True)
    
        # Save data
        savetxt(path+'/small_Steps/I_th.txt', array(I)/nA)
        savetxt(path+'/small_Steps/V_th.txt', array(V)/mV)
        savetxt(path+'/small_Steps/Vc_th.txt', array(Vc)/mV)
    
        # Save parameter values
        save_info(dict(amplitude=ampli/mV, duration=len(Vc)*dt/ms, dt=dt/ms),
                  path+'/threshold_measurement.info')
    else: # Loading the data after the experiment
        from setup.units import *
        path = '.'
        I = loadtxt(path+'/small_Steps/I_th.txt')*nA
        V = loadtxt(path+'/small_Steps/V_th.txt')*mV
        Vc = loadtxt(path + '/small_Steps/Vc_th.txt')*mV


