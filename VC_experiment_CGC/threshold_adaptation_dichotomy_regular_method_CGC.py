

"""
Gross measure of the threshold: dichotomy method.
Fine measure of the threshold: regular steps method.
"""


#import sys
#sys.path.append("/home/sarah/Documents/repositories/clamper/clamper")
#sys.path.append("/home/sarah/Documents/repositories/protocols/")

from clamper import *
from pylab import *
from clamper.data_management import *
from clamper.signals import *
import os
import shutil
from time import sleep

from init_multiclamp import *

ion()

def threshold_measurement_dichotomy_regular(do_experiment, V0 = 0.*mV):

    ### Look for the rough threshold
    print 'V0:', V0
    v0_label = V0/mV
        
    figure('Threshold measurement dicho V0=%s' %v0_label)
        
    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')
        path = 'data/'+date_time()+' Voltage clamp %i' %v0_label
        os.mkdir(path)
        
        # Saving current script
        shutil.copy('threshold_adaptation_dichotomy_regular.py', path)
    
        # Experiment
        os.mkdir(path+'/Steps')
        I = []
        V = []
        # I_peaks = []
        # Vc_peaks = []
            
        ampli_min = 0.*mV
        ampli_current = 30.*mV
        ampli_max = 60.*mV
        spike = False
        
        n_it = 0
                                      
        while True:
            sleep(1) # 1 second between each voltage step
            print n_it, ampli_current/mV
            
            Vc = sequence([constant(200*ms, dt)*V0, #0*mV,
                           constant(20*ms, dt)*ampli_current,
                           constant(20*ms, dt)*0*mV])
            Ii = amplifier.acquire('I', 'Vext', V=Vc)
            I.append(Ii[0])
            V.append(Ii[1])
            
            #I_peaks.append(min(I[-1][int(200.15 * ms / dt):int(219 * ms / dt)]))
            #Vc_peaks.append(Vc[int(210*ms/dt)])
            
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
            i_max = max(abs(Ii[0][int(200.15 * ms / dt):int(219 * ms / dt)]))
            #print i_max
            
            if n_it > 15:
                print 'too much iterations'
                break
            if i_max >= 0.15*nA and abs(ampli_current - ampli_min) <= 0.5*mV and spike is False:
                # !!! this finds the voltage at the peak axonal current
                print 'stop'
                break
            if i_max <= 0.15*nA:
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

    v_threshold = ampli_current - 0.5*mV
    print 'threshold:', v_threshold

    ntrials = 11

    figure('VC steps V0=%s' %v0_label)

    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')

        # Experiment
        os.mkdir(path+'/small_Steps')
        I = []
        V = []

        for ampli in linspace(v_threshold/mV-1, v_threshold/mV+1, ntrials)*mV: # CGC
            sleep(1)
            print 'Amplitude ', ampli/mV
            Vc_th = sequence([constant(200*ms, dt)*V0, #0*mV,
                           constant(20*ms, dt)*ampli,
                           constant(20*ms, dt)*0*mV])
            Ii = amplifier.acquire('I', 'Vext', V=Vc_th)
            I.append(Ii[0])
            V.append(Ii[1])

            # Plotting
            t = dt*arange(len(Vc_th))

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
        savetxt(path+'/small_Steps/I.txt', array(I)/nA)
        savetxt(path+'/small_Steps/V.txt', array(V)/mV)
        savetxt(path+'/small_Steps/Vc.txt', array(Vc_th)/mV)

        # Save parameter values
        save_info(dict(amplitude=ampli/mV, duration=len(Vc_th)*dt/ms, dt=dt/ms),
                  path+'/vc_steps_experiment.info')

        
    
        





