import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 12,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.linewidth": 1.2,
    "lines.linewidth": 1.5,
})

# ==============================
# PARAMETER
# ==============================
EF = -0.1357

emin = -6
emax = 6

# POSISI HIGH-SYMMETRY POINT
# HARUS disesuaikan dengan output bands.x
k_points = [0.0000, 0.6667, 1.3333, 2.0000]
k_labels = ["Γ", "K", "M", "Γ"]

# ==============================
# LOAD BANDS
# ==============================
bands = []

with open("ti2co2.bands.gnu") as f:
    band = []

    for line in f:
        if line.strip() == "":
            if band:
                bands.append(np.array(band))
                band = []
        else:
            band.append([float(x) for x in line.split()])

    if band:
        bands.append(np.array(band))

# ==============================
# PLOT
# ==============================
fig, ax = plt.subplots(figsize=(6, 5))

for band in bands:

    k = band[:, 0]
    E = band[:, 1] - EF

    ax.plot(
        k,
        E,
        linewidth=1.5
    )

# Fermi level
ax.axhline(
    0,
    linestyle="--",
    linewidth=0.8
)

# High-symmetry lines
for x in k_points:
    ax.axvline(
        x,
        linewidth=0.6
    )

# Axis
ax.set_xlim(k_points[0], k_points[-1])
ax.set_ylim(emin, emax)

ax.set_xticks(k_points)
ax.set_xticklabels(k_labels)

ax.set_ylabel("Energy (eV)")

plt.tight_layout()
plt.show()
