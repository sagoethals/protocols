

"""
PC:
Fine measure of the threshold with first the dichotomy method and second a staircase procedure.
"""


import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper")
#sys.path.append("/home/sarah/Documents/repositories/protocols/")

from pylab import *
from clamper.data_management import *
from clamper.signals import *
import os
import shutil
from time import sleep

from init_rig_multiclamp import *

ion()

def threshold_measurement_experiment_PC(do_experiment, V0 = 0.*mV):

    ### Look for the rough threshold
    print 'V0:', V0
    v0_label = V0/mV
        
    figure('Threshold measurement dicho V0=%s' %v0_label)
        
    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')
        path = 'data/'+date_time()+' Voltage clamp PC %i' %v0_label
        os.mkdir(path)
        
        # Saving current script
        shutil.copy('threshold_adaptation_ASA_PC.py', path)
    
        # Experiment
        os.mkdir(path+'/Steps')
        I = []
        V = []
#        I_peaks = []
#        Vc_peaks = []
            
        ampli_min = 0.*mV
        ampli_current = 30.*mV
        ampli_max = 60.*mV
        spike = False
        
        n_it = 0
                                      
        while True:
            sleep(1)
            print n_it, ampli_current/mV
            
            Vc = sequence([constant(200*ms, dt)*V0, #0*mV,
                           constant(50*ms, dt)*ampli_current,
                           constant(20 * ms, dt) * 0 * mV])
            Ii = amplifier.acquire('I', 'Vext', V=Vc)
            I.append(Ii[0])
            V.append(Ii[1])
#            
#            I_peaks.append(min(I[-1][int(200.5 * ms / dt):int(249 * ms / dt)]))
#            Vc_peaks.append(Vc[int(220*ms/dt)])
            
            # Plotting
            t = dt*arange(len(Vc))
            
            subplot(211)
            plot(t/ms, array(Ii)[0] / nA)
            ylabel('Current (nA)')
            #title('Response to voltage pulses')
            
            subplot(212)
            plot(t/ms, array(Ii)[1] / mV)
            xlabel('Time (ms)')
            ylabel('V (mV)')
            pause(0.05)
            
            tight_layout()
                
            # finding the peak
            i_max = max(abs(Ii[0][int(200.3 * ms / dt):int(249 * ms / dt)]))
            
            # finding the threshold
            if n_it > 15:
                print 'too much iterations'
                break
            if i_max >= 2.*nA and abs(ampli_current - ampli_min) <= 0.5*mV and spike is False:
                # finds the peak axonal current
                print ' stop '
                break
            if i_max <= 2.*nA:
                ampli_min = ampli_current
                spike = False
            else:
                ampli_max = ampli_current
                spike = True
                    
            ampli_current = 0.5*ampli_max + 0.5*ampli_min
            
            n_it += 1
            
        show(block=True)
    
        # Save data
        savetxt(path+'/Steps/I_th.txt', array(I)/nA)
        savetxt(path+'/Steps/V_th.txt', array(V)/mV)
        savetxt(path+'/Steps/Vc_th.txt', array(Vc)/mV)

    v_threshold = ampli_current - 0.5 * mV
    print 'threshold:', v_threshold/mV, 'mV'

    figure('VC steps V0=%s' %v0_label)

    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')

        # Experiment
        os.mkdir(path+'/small_Steps')
        I = []
        V = []

        # ASA method
        ampli_range = 4.*mV
        ampli_current = v_threshold
        spike = 0

        for n_it in range(1, 11):
            sleep(1) 
            print n_it, ampli_current/mV
            
            Vc_th = sequence([constant(200*ms, dt)*V0, #0*mV,
                            constant(50*ms, dt)*ampli_current,
                            constant(20 * ms, dt) * 0 * mV])
    
            Ii = amplifier.acquire('I', 'Vext', V=Vc_th)
            I.append(Ii[0])
            V.append(Ii[1])
            
            # Plotting
            t = dt*arange(len(Vc))
            
            subplot(211)
            plot(t/ms, array(Ii)[0] / nA)
            ylabel('Current (nA)')
            
            subplot(212)
            plot(t/ms, array(Ii)[1] / mV)
            xlabel('Time (ms)')
            ylabel('V (mV)')
            pause(0.05)
            
            tight_layout()
            
            # finding the peak
            i_max = max(abs(Ii[0][int(200.5 * ms / dt):int(249 * ms / dt)]))
            print 'peak current:', i_max/ nA, 'nA'
            
            if i_max <= 2.*nA:
                spike = 0
            else: 
                spike = 1
            
            if n_it < 3:
                ampli_current = ampli_current - ampli_range/n_it * (spike - 0.5)
            else:
                ampli_current = ampli_current - ampli_range/(2 + n_it) * (spike - 0.5)
        
        show(block=True)

        # Save data
        savetxt(path+'/small_Steps/I.txt', array(I)/nA)
        savetxt(path+'/small_Steps/V.txt', array(V)/mV)
        savetxt(path+'/small_Steps/Vc.txt', array(Vc_th)/mV)


        
    
        





