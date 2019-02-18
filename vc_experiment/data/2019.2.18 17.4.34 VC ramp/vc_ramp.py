
'''
A simple voltage clamp script.
Ramp protocol.
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
from init_rig_multiclamp import *

do_experiment = not os.path.exists('Pulses')

ion()

figure('VC ramp')

if do_experiment:
    # Make a data folder
    if not os.path.exists('data'):
        os.mkdir('data')
    path = 'data/'+ date_time()+' VC ramp'
    os.mkdir(path)
    
    # Saving current script
    shutil.copy('vc_ramp.py', path)

    # Experiment
    os.mkdir(path+'/Ramp')
    I = []
    V = []

    dV = 0.1*mV
    ramp_range = 100.*mV
    ramp_duration = ramp_range/dV
    
    Vc = sequence([constant(20*ms, dt)*0*mV,
                   ramp(ramp_duration*ms, dt)*100.*mV,
                   constant(20*ms, dt)*0*mV])
    
    Ii = amplifier.acquire('I', 'Vext', V=Vc)
    I.append(Ii[0])
    V.append(Ii[1])

    print 'Finished ramp protocol'

    t = dt*arange(len(Vc))
    
    # plot data
    subplot(211)
    plot(t/ms, array(Ii[0]) / nA)
    xlabel('Time (ms)')
    ylabel('Current (nA)')
    #title('Response to voltage pulses')
    
    subplot(212)
    plot(t/ms, array(Ii[1]) / mV)
    xlabel('Time (ms)')
    ylabel('V (mV)')
    pause(0.05)
    
    tight_layout()

    show(block=True)

    # Save data
    savetxt(path+'/Ramp/I.txt',array(I)/nA)
    savetxt(path+'/Ramp/V.txt',array(V)/mV)
    savetxt(path+'/Ramp/Vc.txt',array(Vc)/mV)

    # Save parameter values
    save_info(dict(duration=len(Vc)*dt/ms, dt=dt/ms),
              path+'/vc_ramp.info')

else: # Loading the data after the experiment
    from clamper.setup.units import *
    path = '.'
    I = loadtxt(path+'/Ramp/I.txt')*nA
    V = loadtxt(path + '/Ramp/V.txt')*mV
    Vc = loadtxt(path + '/Ramp/Vc.txt')*mV

















