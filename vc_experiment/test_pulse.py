'''
A simple voltage clamp script.
This one does experiment and analysis in the same script.
'''
import sys
sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
sys.path.append("/home/sarah/Documents/repositories/protocols/")

#from clamper import *
from pylab import *
from brianmodels import *
from data_management import *
from signals import *
import os
import shutil
from time import sleep

#from init_model import *
from init_rig_multiclamp import *

do_experiment = not os.path.exists('Pulses')

# Parameters
nrec = 2

ion()

figure('Test pulse')

if do_experiment:
    # Make a data folder
    if not os.path.exists('data'):
        os.mkdir('data')
    path = 'data/'+ date_time()+' Test pulse'
    os.mkdir(path)
    
    # Saving current script
    shutil.copy('test_pulse.py', path)

    # Experiment
    os.mkdir(path+'/Pulses')
    I = []
    for rec in range(nrec): 
        sleep(1)
        print 'Rec:', rec
        Vc = sequence([constant(20*ms, dt)*0*mV,
                       constant(10*ms, dt)*(-10*mV),
                       constant(10*ms, dt)*10*mV,
                       constant(20*ms, dt)*0*mV])
        I.append(amplifier.acquire('I', 'V', V=Vc-80*mV)) # !!!!! change that for CGC
        
        t = dt*arange(len(Vc))
        
        # plot data
        subplot(211)
        plot(t/ms, array(I[rec][0]) / nA)
        xlabel('Time (ms)')
        ylabel('Current (nA)')
        #title('Response to voltage pulses')
        
        subplot(212)
        plot(t/ms, array(I[rec][1]) / mV)
        xlabel('Time (ms)')
        ylabel('V (mV)')
        pause(0.05)
        
        tight_layout()
        
        show(block=True)
        
    # Save data
    savetxt(path+'/Pulses/I.txt',array(I[0])/nA)
    savetxt(path+'/Pulses/V.txt',array(I[1])/mV)
    savetxt(path+'/Pulses/Vc.txt',array(Vc)/mV)

    # Save parameter values
    save_info(dict(duration=len(Vc)*dt/ms, dt=dt/ms),
              path+'/test_pulse.info')

else: # Loading the data after the experiment
    from clamper.setup.units import *
    path = '.'
    I = loadtxt(path+'/Pulses/I.txt')*nA
    V = loadtxt(path + '/Pulses/V.txt')*mV
    Vc = loadtxt(path + '/Pulses/Vc.txt')*mV

    # Plotting
    figure()
    t = dt*arange(len(Vc))
    
    subplot(211)
    for Ii in I:
        plot(t/ms, array(Ii[0]) / nA)
    xlabel('Time (ms)')
    ylabel('Current (nA)')
    title('Response to voltage pulses')
    
    subplot(212)
    for Ii in I:
        plot(t/ms, array(Ii[1]) / mV)
    xlabel('Time (ms)')
    ylabel('V (mV)')















