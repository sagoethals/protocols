'''

A test pulse for cerebellar granule cells, repeated 5 times.

The voltage is clamped at resting holding potential during 20 ms, then 10 mV below and above the resting holding potential, during 10 ms each.

'''


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
from init_multiclamp import *

do_experiment = not os.path.exists('Pulses')

# Parameters
nrec = 5

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
    V = []
    for rec in range(nrec): 
        sleep(1)
        print 'Rec:', rec
        Vc = sequence([constant(20*ms, dt)*0*mV,
                       constant(10*ms, dt)*(-10*mV),
                       constant(10*ms, dt)*10*mV,
                       constant(20*ms, dt)*0*mV])
        Ii = amplifier.acquire('I', 'Vext', V=Vc)
        I.append(Ii[0])
        V.append(Ii[1])
        
        t = dt*arange(len(Vc))
        
        # plot data
        subplot(211)
        plot(t/ms, array(I[rec]) / nA)
        xlabel('Time (ms)')
        ylabel('Current (nA)')
        #title('Response to voltage pulses')
        
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

    # Save parameter values
    save_info(dict(duration=len(Vc)*dt/ms, dt=dt/ms),
              path+'/test_pulse.info')

else: # Loading the data after the experiment
    from clamper.setup.units import *
    path = '.'
    I = loadtxt(path+'/Pulses/I.txt')*nA
    V = loadtxt(path + '/Pulses/V.txt')*mV
    Vc = loadtxt(path + '/Pulses/Vc.txt')*mV

    # # Plotting
    # figure()
    # t = dt*arange(len(Vc))
    #
    # subplot(211)
    # for Ii in I:
    #     plot(t/ms, array(Ii[0]) / nA)
    # xlabel('Time (ms)')
    # ylabel('Current (nA)')
    # title('Response to voltage pulses')
    #
    # subplot(212)
    # for Ii in I:
    #     plot(t/ms, array(Ii[1]) / mV)
    # xlabel('Time (ms)')
    # ylabel('V (mV)')















