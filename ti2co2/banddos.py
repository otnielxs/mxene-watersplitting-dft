import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ============================================================
# STYLE
# ============================================================

mpl.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 12,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.linewidth": 1.2,
    "lines.linewidth": 1.5,
})

# ============================================================
# PARAMETER
# ============================================================

EF = -0.1357

emin = -4
emax = 3

k_points = [0.0000, 0.6667, 1.3333, 2.0000]
k_labels = ["Γ", "K", "M", "Γ"]


bands_file = "ti2co2.bands.gnu"
dos_file = "ti2co2.dos"

dos_max = None

bands = []

with open(bands_file) as f:

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


dos_data = np.loadtxt(dos_file)


E_dos = dos_data[:, 0] - EF
DOS = dos_data[:, 1]


fig, (ax_band, ax_dos) = plt.subplots(
    1,
    2,
    figsize=(8, 5.5),
    sharey=True,
    gridspec_kw={
        "width_ratios": [1.65, 1.0],
        "wspace": 0
    }
)

for band in bands:

    k = band[:, 0]

    E = band[:, 1] - EF

    ax_band.plot(
        k,
        E,
        color='#FF6666',
        linewidth=1.5
    )

ax_band.axhline(
    0,
    linestyle="--",
    linewidth=0.8
)


for x in k_points:

    ax_band.axvline(
        x,
        linewidth=0.6
    )


ax_band.set_xlim(
    k_points[0],
    k_points[-1]
)

ax_band.set_ylim(
    emin,
    emax
)

ax_band.set_xticks(k_points)
ax_band.set_xticklabels(k_labels)

ax_band.set_ylabel(r"$E-E_F$ (eV)")

ax_dos.plot(
    DOS,
    E_dos,
    color='#FF6666',
    linewidth=1.5
)

ax_dos.fill_betweenx(
    E_dos,
    0,
    DOS,
    color='#FF6666',
    alpha=0.4
)


ax_dos.axhline(
    0,
    linestyle="--",
    linewidth=0.8
)

ax_dos.set_ylim(
    emin,
    emax
)

ax_dos.set_xlabel(
    "DOS (states/eV)"
)

if dos_max is None:
    ax_dos.set_xlim(
        0,
        DOS.max() * 1.1
    )
else:
    ax_dos.set_xlim(
        0,
        dos_max
    )

ax_dos.tick_params(
    axis="y",
    left=False,
    labelleft=False
)

ax_dos.spines["left"].set_visible(False)
ax_band.spines["right"].set_visible(False)

ax_band.tick_params(
    direction="out"
)

ax_dos.tick_params(
    direction="out"
)

plt.tight_layout()

plt.show()
