

"""
Gross measure of the threshold: dichotomy method.
Fine measure of the threshold: staircase method.
"""

#import sys
#sys.path.append("/home/sarah/Documents/repositories/clampy/clampy/")
#sys.path.append("/home/sarah/Documents/repositories/protocols/")

#from brian2 import *
from pylab import *
#from data_management import *
#from signals import *
import os
import shutil
from time import sleep

from init_multiclamp import *

#from init_model import *

ion()

def threshold_adaptation_dichotomy_staircase_method_CGC(do_experiment, amplifier, model=False, Vh = 0.*mV, V0 = 0.*mV, i_threshold = 0.15*nA, dt = 0.02*ms, Rs = False):
    '''
    Vh is 0 mV for true recordings in CGC (set on the Multiclamp commander).
    i_threshold is 0.15 nA for CGC, larger for neuron model.
    '''
    # Measure of the gross threshold with dichotomy method
    print 'V0:', V0
    v0_label = V0/mV
        
    figure('Gross threshold measurement V0=%s' %v0_label)
        
    if do_experiment:
        # Make a data folder
        if not os.path.exists('data'):
            os.mkdir('data')
        if Rs:
            rs_label = Rs/Mohm
            path = 'data/'+date_time()+' Voltage clamp %i' %rs_label
        else:
            path = 'data/'+date_time()+' Voltage clamp %i' %v0_label
        os.mkdir(path)
        
        # Saving current script
        shutil.copy('threshold_adaptation_dichotomy_staircase_method_CGC.py', path)
    
        # Experiment
        os.mkdir(path+'/Steps')
        I = []
        V = []
        Im = []
        INa = []
        IK = []
        Vcom = []
            
        ampli_min = 0.*mV
        ampli_current = 30.*mV
        ampli_max = 60.*mV
        spike = False
        
        n_it = 0
                                      
        while True:
            sleep(1)
            print n_it, (Vh + ampli_current)/mV
            
            # Voltage command and acquisition
            Vc = sequence([constant(200*ms, dt)*(Vh + V0), #0*mV,
                           constant(20*ms, dt)*(Vh+ampli_current),
                           constant(20 * ms, dt) * Vh])
            #Ii = amplifier.acquire('I', 'Vext', V=Vc)
            if model:
                Ii = amplifier.acquire('I', 'Vext', 'Im',  'INa', 'IK', Vc=Vc)
                I.append(Ii[0])
                V.append(Ii[1])
                Vcom.append(Vc)
                Im.append(Ii[2])
                INa.append(Ii[3])
                IK.append(Ii[4])
            else:   
                Ii = amplifier.acquire('I', 'V', V=Vc) # membrane potential
                I.append(Ii[0])
                V.append(Ii[1])
                Vcom.append(Vc)
            
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
                
            # Measuring the peak axonal current
            i_max = max(abs(Ii[0][int(200.25 * ms / dt):int(219 * ms / dt)]))
            
            if n_it > 11:
                print 'too much iterations'
                break
            if i_max >= i_threshold and abs(ampli_current - ampli_min) <= 0.5*mV and spike is False:
                print ' stop '
                break
            if i_max <= i_threshold:
                ampli_min = ampli_current
                spike = False
            else:
                ampli_max = ampli_current
                spike = True
                    
            ampli_current = 0.5*ampli_max + 0.5*ampli_min
            
            n_it += 1
            
        show(block=True)
    
        # Save data
        savetxt(path+'/Steps/I.txt', array(I)/nA)
        savetxt(path+'/Steps/V.txt', array(V)/mV)
        savetxt(path+'/Steps/Vc.txt', array(Vcom)/mV)

        if model:
            savetxt(path+'/Steps/Im.txt', array(Im)/nA)
            savetxt(path+'/Steps/INa.txt', array(INa)/nA)
            savetxt(path+'/Steps/IK.txt', array(IK)/nA)
            

        # Gross threshold
        v_threshold = ampli_current - 0.5 * mV
        print 'threshold:', v_threshold/mV, 'mV'

        # Fine measure of the threshold with the staircase methode
        figure('Fine threshold measurement V0=%s' %v0_label)

        # Experiment
        os.mkdir(path+'/small_Steps')
        I = []
        V = []
        Im = []
        Vcom = []
        INa = []
        IK = []

        # Staircase method
        ampli_range = 4.*mV
        ampli_current = v_threshold
        spike = 0

        for n_it in range(1, 21):
            sleep(1) 
            print n_it, (Vh+ampli_current)/mV
            
            # Command and acquisition
            Vc_th = sequence([constant(200*ms, dt)*(Vh + V0), #0*mV,
                            constant(20*ms, dt)*(Vh + ampli_current),
                            constant(20 * ms, dt) * Vh])
            
            if model:
                Ii = amplifier.acquire('I', 'Vext', 'Im', 'INa', 'IK', Vc=Vc_th)
                I.append(Ii[0])
                V.append(Ii[1])
                Im.append(Ii[2])
                Vcom.append(Vc_th)
                INa.append(Ii[3])
                IK.append(Ii[4])
            else:   
                Ii = amplifier.acquire('I', 'V', V=Vc_th) # membrane potential
                I.append(Ii[0])
                V.append(Ii[1])
                Vcom.append(Vc_th)
    
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
            
            # Measuring the peak axonal current
            i_max = max(abs(Ii[0][int(200.25 * ms / dt):int(219 * ms / dt)]))
            #print 'peak current:', i_max/ nA, 'nA'
            
            if i_max <= i_threshold:
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
        savetxt(path+'/small_Steps/Vc.txt', array(Vcom)/mV)
        if model:
            savetxt(path+'/small_Steps/Im.txt', array(Im)/nA)
            savetxt(path+'/small_Steps/INa.txt', array(INa)/nA)
            savetxt(path+'/small_Steps/IK.txt', array(IK)/nA)


        
    
        





