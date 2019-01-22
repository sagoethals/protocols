'''
Initializes data acquisition on the rig.
This is specific for the Multiclamp 700B.
'''

from clamper import *
from clamper.devices import *
#from clamper.devices.gains.axoclamp2b import gains
from acquisition.units import *

board = NI()

dt = 0.02*ms
board.sampling_rate = float(1/dt)

board.set_analog_input('primary', channel=0)
board.set_analog_input('secondary', channel=1)

board.set_analog_output('command', channel=0)

amp = MultiClampChannel()
amp.configure_board(board, primary='primary', secondary='secondary', command='command')


