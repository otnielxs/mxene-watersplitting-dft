import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": ["DejaVu Serif"],
    "font.serif": ["Times New Roman"],
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "axes.linewidth": 1.2,
    "lines.linewidth": 1.5,
})

EF = 0.4327   # ganti sesuai scf.out
emin = -6
emax = 6

# ==============================
# LOAD DOS
# ==============================
dos_data = np.loadtxt("ti2cf2.dos")  # sesuaikan nama file DOS Anda
E = dos_data[:, 0] - EF           # kolom pertama: energi
DOS = dos_data[:, 1]              # kolom kedua: DOS total

# ==============================
# PLOT DOS SAJA
# ==============================
fig, ax = plt.subplots(figsize=(5, 5))

# plot kurva halus
ax.plot(E, DOS, color='darkblue', linewidth=1.5)

# fill area di bawah kurva
ax.fill_between(E, DOS, color='lightblue', alpha=0.6)

# Fermi level
ax.axvline(0, linestyle='--', color='gray', linewidth=1)

ax.set_xlim(emin, emax)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("DOS (states/eV)")
ax.set_ylim(0, max(DOS)*1.1)

plt.tight_layout()
plt.show()
