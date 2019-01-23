"""

Read npz data

"""

import sys
#sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
#sys.path.append("/Users/Romain/PycharmProjects/protocols/data/")

from brian2 import * 

# Test pulse
data_tp = load('data/2019.01.23_15.00.46_0104_Test Pulse.npz')

vc_tp = data_tp['Vc']
I_tp = data_tp['I']
time_tp = data_tp['time']

figure('Tp')
subplot(211)
plot(time_tp, I_tp*1e9)
ylabel('I (nA)')

subplot(212)
plot(time_tp, vc_tp*1e3)
ylabel('V command (mV)')
xlabel('Time (ms)')

tight_layout

# # Na activation
# data = load('20190109_14:13_01VCstepvr_str05.npz')
#
# vc = data['Vc']
# I = data['I']
# time = data['time']
#
# cmap = plt.get_cmap('gnuplot')
# colors = [cmap(i) for i in np.linspace(0, 1, len(vc))]
# figure('Na act')
# subplot(211)
# for i in range(len(vc)):
#     plot(time, I[i]*1e-3, color=colors[i])
# ylabel('I (nA)')
#
# subplot(212)
# for i in range(len(vc)):
#     plot(time, vc[i], color=colors[i])
#
# ylabel('V command (mV)')
# xlabel('Time (ms)')
#
# tight_layout

show()