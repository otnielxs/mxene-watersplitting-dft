import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

epsr = np.loadtxt("epsr_fixed.dat")
epsi = np.loadtxt("epsi_clean.dat")

n = min(len(epsr), len(epsi))
epsr = epsr[:n]
epsi = epsi[:n]

energy = epsr[:,0]
eps1 = epsr[:,3]
eps2 = epsi[:,3]

c = 2.998e8
omega = energy * 1.602e-19 / 1.055e-34
alpha = np.sqrt(2) * omega / c * np.sqrt(np.sqrt(eps1**2 + eps2**2) - eps1)

plt.figure(figsize=(6,5))
plt.plot(energy, alpha*1e-2, color="#707070", label="Absorption spectrum")

plt.xlabel("Photon Energy (eV)")
plt.ylabel("Absorption (×10⁵ cm⁻¹)")
plt.legend()

# batas sesuai Xu2020
plt.xlim(1.5, 4.0)
plt.ylim(0, 6e5)

# format sumbu y agar tampil ×10⁵
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(axis='y', style='sci', scilimits=(5,5))

plt.tight_layout()
plt.show()
