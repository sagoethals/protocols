#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fine measure of the threshold with the dichotomy method.
"""


import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper")
#sys.path.append("/home/sarah/Documents/repositories/protocols/")

## to run on the rig:
#from clamper import *
#from pylab import *
#from clamper.brianmodels import *
#from clamper.data_management import *
#from clamper.signals import *
#import os
#import shutil
#from time import sleep
#
#from init_rig_multiclamp import *

# to run with the model:
#from clamper import *
from brian2 import *
from pylab import *
from brianmodels import *
from data_management import *
from signals import *
import os
import shutil
from time import sleep

from init_model import *

ion()

#do_experiment = not os.path.exists('Steps')

def threshold_measurement_dicho(do_experiment, V0 = 0.*mV):

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
        shutil.copy('threshold_adaptation_dichotomy_experiment.py', path)
    
        # Experiment
        os.mkdir(path+'/Steps')
        I = []
        I_peaks = []
        Vc_peaks = []
        V = []
        #for ampli in linspace(20,60,ntrials)*mV: # CGC
        for ampli in linspace(-60,-20,ntrials)*mV:
            sleep(1)
            print 'Amplitude ', ampli
            Vc = sequence([constant(200*ms, dt)*V0, #0*mV,
                           constant(20*ms, dt)*ampli,
                           constant(20*ms, dt)*V0]) #0*mV])
            Ii = amplifier.acquire('I', 'Vext', V=Vc)
            I.append(Ii[0])
            V.append(Ii[1])
            
            I_peaks.append(min(I[-1][int(200.2 * ms / dt):int(219 * ms / dt)]))
            print I_peaks
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

    #close('VC steps V0=%s' %v0_label)

    print I_peaks
    idx_th = where(array(I_peaks)<=-150.1e-12)[0][0]  #it finds the peak axonal current, units are A
    print idx_th, I_peaks[idx_th]
    v_threshold = Vc_peaks[idx_th-1] 
    print 'Rough threshold:', v_threshold

    ### Accurate determination of the threshold
    
    ntrials = 11
    
    figure('Threshold measurementdicho V0=%s' %v0_label)
    
    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')
    
        # Experiment
        os.mkdir(path+'/small_Steps')
        I = []
        V = []
       
#        if model == False:
#            dt = 0.02*ms
#        else:
#            dt = 0.1*ms
            
        # values for the AP model, not adapted to CGC
        ampli_min = v_threshold-4.*mV # or -80*mV?
        ampli_current = v_threshold
        ampli_max = v_threshold+4.*mV # or -30*mV?
        spike = False
                                      
        while True:
            sleep(1) # 1 second between each voltage step
            print ampli_current
            Vc = sequence([constant(200*ms, dt)*V0, #0*mV,
                           constant(20*ms, dt)*ampli_current,
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
                
            # finding the peak
            i_max = max(abs(I[-1][int(200.2 * ms / dt):int(219 * ms / dt)]))
            print i_max
                
            if i_max >= 0.15*nA and abs(ampli_current - ampli_min) <= 0.2*mV and spike == False:
                print 'stop'
                break
            if i_max <= 0.15*nA:
                ampli_min = ampli_current
                spike = False
            else: 
                ampli_max = ampli_current
                spike = True
                    
            ampli_current = 0.5*ampli_max + 0.5*ampli_min
            
        show(block=True)
    
        # Save data
        savetxt(path+'/small_Steps/I_th.txt', array(I)/nA)
        savetxt(path+'/small_Steps/V_th.txt', array(V)/mV)
        savetxt(path+'/small_Steps/Vc_th.txt', array(Vc)/mV)
    
        # Save parameter values
        save_info(dict(amplitude=ampli/mV, duration=len(Vc)*dt/ms, dt=dt/ms),
                  path+'/threshold_measurement_dicho.info')
    else: # Loading the data after the experiment
        from setup.units import *
        path = '.'
        I = loadtxt(path+'/small_Steps/I_th.txt')*nA
        V = loadtxt(path+'/small_Steps/V_th.txt')*mV
        Vc = loadtxt(path + '/small_Steps/Vc_th.txt')*mV






