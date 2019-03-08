
"""

A deactivation experiment for cerebellar granule cells.

An axonal spike is elicited by a short prepulse (0.1 ms) at -30 mV and then the cell is successively clamped at lower potentials, from -30 mV to -90 mV. 

"""

# import sys
# sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
# sys.path.append("/home/sarah/Documents/repositories/protocols/")

from clampy import *
from pylab import *
#from clampy.brianmodels import *
from clampy.data_management import *
from clampy.signals import *
import os
import shutil
from time import sleep

#from init_model import *
from init_multiclamp import *

ion()

do_experiment = not os.path.exists('Steps')

# Parameters
ntrials = 31

figure('Deact')

if do_experiment:
    # Make a data folder
    if not os.path.exists('data'):
        os.mkdir('data')
    path = 'data/'+ date_time() +' Deactivation'
    os.mkdir(path)
    
    # Saving current script
    shutil.copy('run_deactivation_experiment_CGC.py', path)

    # Experiment
    os.mkdir(path+'/Steps')
    I = []
    V = []
    for ampli in linspace(50,-10,ntrials)*mV:
        sleep(1)
        print 'Amplitude ', ampli
        Vc = sequence([constant(100*ms, dt)*0*mV,
                       constant(0.1*ms, dt)*50*mV,
                       constant(20*ms, dt)*ampli,
                       constant(20*ms, dt)*0*mV])
        Ii = amplifier.acquire('I', 'Vext', V=Vc)
        I.append(Ii[0])
        V.append(Ii[1])
        
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
              path+'/deactivation_experiment.info')
else: # Loading the data after the experiment
    from setup.units import *
    path = '.'
    I = loadtxt(path+'/Steps/I.txt')*nA
    V = loadtxt(path+'/Steps/V.txt')*mV
    Vc = loadtxt(path + '/Steps/Vc.txt')*mV
     
    


