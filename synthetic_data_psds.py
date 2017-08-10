"""
#################################################################################
History for synthetic_data_psds.py
#################################################################################
"""

import sys
sys.path.append("/Users/vasilis")
sys.path.append("/home/vasileios")
import vaspy
from vaspy import synthetic_data, mem
from vaspy import markow_fitter
import numpy as np
from matplotlib import pyplot as plt

plt.ion()
plt.close("all")

z, d18 = synthetic_data.synthetic_AR1(dt = 0.001, N = 20001, a1 = 0.5, variance = 80)
d18_diff = synthetic_data.diffuse(z, d18, diff_len = 0.07)
plt.figure(12)
plt.plot(z, d18)
plt.plot(z, d18_diff, "r", linewidth = 2)
z_5, d18_diff_5 = synthetic_data.sample(z, d18_diff, dt = 0.05, measurement_noise = 0.09)
print z_5
plt.plot(z_5, d18_diff_5, "g", linewidth = 2)
print z_5[-1]
print(z[-1])

f, P = mem.Mem(z_5, d18_diff_5)(z_5, d18_diff_5, M = 30, N = 2000)
plt.figure(13)
plt.semilogy(f, P)

fiter = markow_fitter.Markow_Fitter(f,P)
psd_fit = fiter.run(dt = 0.05)
P_fit = psd_fit[0]
p_fit = psd_fit[1]
noise_model = fiter.model_noise_markow(f, dt = 0.05, variance = p_fit[1], a1 = p_fit[3])
ps_model = fiter.model_Ps(f, p_fit[0], p_fit[2])
print(p_fit)
plt.semilogy(f, P_fit, linewidth = 2)
plt.semilogy(f, noise_model, linewidth = 2)
plt.semilogy(f, ps_model, linewidth = 2)

fil = open("./single_isotope_psd_synthetic.txt", "w")
outdata = np.transpose(np.vstack((f, (2*np.pi*f)**2, P, P_fit, noise_model, ps_model)))
fil.write("f\tk2\tP\tP_fit\tP_n\tP_s\n")
np.savetxt(fil, outdata, fmt = "%0.4f\t%0.4f\t%0.4e\t%0.4e\t%0.4e\t%0.4e")

fil.close()
