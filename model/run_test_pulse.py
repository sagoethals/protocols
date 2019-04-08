
"""
Run a test pulse protocol in a BrianModel.
"""

import sys
sys.path.append("/home/sarah/Documents/repositories/clampy/")
sys.path.append("/home/sarah/Documents/repositories/protocols/VC_experiment_CGC/")
sys.path.append("/home/sarah/Documents/repositories/protocols/")

import os
from brian2 import *
from clampy import *
from init_model import *
from time import sleep

do_experiment = not os.path.exists('Steps')

# Parameters
nrec = 1
Vh = -75.*mV

ion()

figure('Test pulse')

if do_experiment:
    # Make a data folder
    if not os.path.exists('data'):
        os.mkdir('data')
    path = 'data/'+ date_time()+' Test pulse'
    os.mkdir(path)
    
    # Experiment
    os.mkdir(path+'/Pulses')
    I = []
    V = []
    for rec in range(nrec): 
        sleep(1)
        print 'Rec:', rec
        Vc = sequence([constant(20*ms, dt)*Vh,
                       constant(10*ms, dt)*(Vh-10*mV),
                       constant(10*ms, dt)*(Vh+10*mV),
                       constant(20*ms, dt)*Vh])
        Ii = amplifier.acquire('I', 'Vext', Vc=Vc)
        I.append(Ii[0])
        V.append(Ii[1])
        
        t = dt*arange(len(Vc))
        
        # plot data
        subplot(211)
        plot(t/ms, array(I[rec]) / nA)
        xlabel('Time (ms)')
        ylabel('Current (nA)')
        
        subplot(212)
        plot(t/ms, array(V[rec]) / mV)
        xlabel('Time (ms)')
        ylabel('V (mV)')
        pause(0.05)
        
        tight_layout()

    show(block=True)

    # Save data
    savetxt(path+'/Pulses/I.txt',array(I)/nA)
    savetxt(path+'/Pulses/V.txt',array(V)/mV)
    savetxt(path+'/Pulses/Vc.txt',array(Vc)/mV)

else: # Loading the data after the experiment
    from clampy.setup.units import *
    path = '.'
    I = loadtxt(path+'/Pulses/I.txt')*nA
    V = loadtxt(path + '/Pulses/V.txt')*mV
    Vc = loadtxt(path + '/Pulses/Vc.txt')*mV