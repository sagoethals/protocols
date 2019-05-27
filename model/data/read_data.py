
"""
Read data.
"""

#path = '.'

from brian2 import * 
import glob

dt = 0.02*ms

# Plot an example

dir_name = glob.glob("*" + 'Voltage clamp 0')
print dir_name

# Load data
I = loadtxt( dir_name[0] + '/Steps/I.txt')*nA
V = loadtxt( dir_name[0] + '/Steps/V.txt')*mV
Vc = loadtxt( dir_name[0] + '/Steps/Vc.txt')*mV

t = dt*arange(len(Vc))

cmap = plt.get_cmap('gnuplot')
cols = [cmap(i) for i in np.linspace(0, 1, len(V))]

figure('Gross threshold')
subplot(211)
for i in range(len(V)):
    plot(t/ms, array(I[i])/nA, color=cols[i]) 
ylabel('I (nA)')
xlim(199, 221)
ylim(-15, 15)

subplot(212)
for i in range(len(V)):
    plot(t/ms, array(V[i])/mV, color=cols[i])
ylabel('V command (mV)')
xlabel('Time (ms)')
xlim(199, 221)

tight_layout()

# Load data
I_acc = loadtxt( dir_name[0] + '/small_Steps/I.txt')*nA
V_acc = loadtxt( dir_name[0] + '/small_Steps/V.txt')*mV
Vc_acc = loadtxt( dir_name[0] + '/small_Steps/Vc.txt')*mV

t = dt*arange(len(Vc_acc))

cmap = plt.get_cmap('gnuplot')
cols = [cmap(i) for i in np.linspace(0, 1, len(V_acc))]

figure('Fine threshold')
subplot(211)
for i in range(len(V_acc)):
    plot(t/ms, array(I_acc[i])/nA, color=cols[i]) 
ylabel('I (nA)')
xlim(199, 221)
ylim(-5, 5)

subplot(212)
for i in range(len(V_acc)):
    plot(t/ms, array(V_acc[i])/mV, color=cols[i])
ylabel('V command (mV)')
xlabel('Time (ms)')
xlim(199, 221)

tight_layout()

show()

