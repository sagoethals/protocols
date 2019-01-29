"""

Read npz data

"""

import sys
#sys.path.append("/home/sarah/Documents/repositories/clamper/clamper/")
#sys.path.append("/Users/Romain/PycharmProjects/protocols/data/")
sys.path.append("/home/sarah/Storage/Data/Sarah/Patch January 2019/")

from brian2 import * 

dt = 0.02*ms

# Test pulse
data_tp = load('/data/2019.01.29_13.19.49_0101_Test Pulse.npz')

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

#  # Na activation
# data_act = load('/media/sarah/storage/Data/Sarah/Patch January 2019/28.1.2019/2019.01.28_16.04.27_0101_VC adaptation_35.0.npz')
#
# vc = data_act['Vc']
# I = data_act['I']
# time = data_act['time']
# vc_thres = data_act['thresh'][0]
# I_thres = data_act['thresh'][1]
# time_thres = data_act['thresh'][2]
#
# i_peaks = []
# vc_peaks = []
#
# cmap = plt.get_cmap('gnuplot')
# colors = [cmap(i) for i in np.linspace(0, 1, len(vc))]
#
# figure('Na act')
# subplot(211)
# for i in range(len(vc)):
#     plot(time, I[i]*1e-3, color=colors[i])
#     idx_peak = argmin(I[i][int(200.2 * ms / dt):int(219 * ms / dt)]) + int(200.2 * ms / dt)
#     i_peaks.append(I[i][idx_peak])
#     vc_peaks.append(vc[i][idx_peak])
#
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
#
# i_peaks_acc = []
# vc_peaks_acc = []
#
# figure('Thres measurement')
# subplot(211)
# for i in range(len(vc_thres)):
#     plot(time_thres, I_thres[i]*1e-3, color=colors[i])
#     idx_peak_acc = argmin(I_thres[i][int(200.2 * ms / dt):int(219 * ms / dt)]) + int(200.2 * ms / dt)
#     i_peaks_acc.append(I_thres[i][idx_peak_acc])
#     vc_peaks_acc.append(vc_thres[i][idx_peak_acc])
# ylabel('I (nA)')
#
# subplot(212)
# for i in range(len(vc_thres)):
#     plot(time_thres, vc_thres[i], color=colors[i])
#
# ylabel('V command (mV)')
# xlabel('Time (ms)')
#
# tight_layout
#
# figure('IV curve')
# plot(array(vc_peaks)-80, i_peaks, 'o')
# plot(array(vc_peaks_acc)-80, i_peaks_acc, 'o', color='red')

show()