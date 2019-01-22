'''
An oscilloscope showing the voltage response to a pulse

TODO:
* maybe add slider or so for current amplitude and duration
* calculate resistance, V0 etc
'''

import sys
sys.path.append("/Users/Romain/PycharmProjects/Paramecium/")
sys.path.append("/Users/Romain/PycharmProjects/clamper/")

from acquisition import *
from pylab import *
from signals import *
import os
from init_rig_multiclamp import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

V0 = - 10.*mV
T0 = 50*ms
T1 = 10*ms
T2 = 50*ms
Vc = sequence([constant(T0, dt) * 0 * mV,
               constant(T1, dt) * V0,
               constant(T2, dt) * 0 * mV])

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
plt.xlabel('Time (ms)')
plt.ylabel('I (nA)')
#resistance_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

t = dt*arange(len(Vc))
xlim(0,max(t/ms))
#ylim(-150,100)
line, = plot(t/ms,0*t)

def update(i):

    I = amp.acquire('I', V=Vc)
        #V = board.acquire('V', I=Ic)
    ## Calculate offset and resistance
    #V0 = median(V[:int(T0/dt)]) # calculated on initial pause
    #Vpeak = median(V[int((T0+2*T1/3.)/dt):int((T0+T1)/dt)]) # calculated on last third of the pulse
    #R = (Vpeak-V0)/I0
    # Plot
    line.set_ydata(I/pA)
    #resistance_text.set_text('{:.1f} MOhm'.format(R/Mohm))
    return line,

anim = animation.FuncAnimation(fig,update)

show()
