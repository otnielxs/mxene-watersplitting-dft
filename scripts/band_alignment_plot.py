"""
need some data inputs
    V_vac      -> plateau vacuum from avg.dat (Ry->eV)
    E_fermi    -> from scf.out
    E_homo     -> "highest occupied" from nscf_nbnd.out
    E_lumo     -> "lowest unoccupied" from nscf_nbnd.out

Convert to absolute vs vacuum scale:
    E_abs = E_internal - V_vac
"""

import numpy as np
import matplotlib.pyplot as plt

materials = {
    "Ti2CO2": {
        "V_vac": 5.533,
        "E_fermi": -0.1357,
        "E_homo": -0.2923,   # VBM
        "E_lumo": 0.0412,    # CBM
        "metallic": False,
    },
    "Ti2CF2": {
        "V_vac": 5.267,
        "E_fermi": 0.4327,
        "E_homo": 0.5901,
        "E_lumo": 0.4385,
        "metallic": True,
    },
    "Ti2C(OH)2": {
        "V_vac": 4.459,
        "E_fermi": 2.3778,
        "E_homo": 2.6866,
        "E_lumo": 2.3676,
        "metallic": True,
    },
}

# Water potential reduction and oxidation
E_H2   = -4.44   # H+/H2  (HER)
E_H2O  = -5.67   # O2/H2O (OER)

for name, d in materials.items():
    d["E_homo_abs"] = d["E_homo"] - d["V_vac"]
    d["E_lumo_abs"] = d["E_lumo"] - d["V_vac"]
    print(f"{name:12s}  VBM/HOMO = {d['E_homo_abs']:.3f} eV   "
          f"CBM/LUMO = {d['E_lumo_abs']:.3f} eV   "
          f"{'(metallic)' if d['metallic'] else '(semiconductor)'}")

fig, ax = plt.subplots(figsize=(7, 6))

names = list(materials.keys())
x = np.arange(len(names))
bar_half_width = 0.28

for xi, name in zip(x, names):
    d = materials[name]
    lo, hi = sorted([d["E_homo_abs"], d["E_lumo_abs"]])

    color = "tab:gray" if d["metallic"] else "tab:blue"
    ax.plot([xi - bar_half_width, xi + bar_half_width], [d["E_homo_abs"]]*2,
            color=color, lw=3)
    ax.plot([xi - bar_half_width, xi + bar_half_width], [d["E_lumo_abs"]]*2,
            color=color, lw=3)
    ax.plot([xi, xi], [lo, hi], color=color, lw=1.5, linestyle=(0, (3, 2)))

    label_gap = "metallic\n(band overlap)" if d["metallic"] else f"gap = {hi-lo:.2f} eV"
    ax.text(xi, hi + 0.15, label_gap, ha="center", fontsize=9)
    ax.text(xi - bar_half_width - 0.05, d["E_homo_abs"], f"{d['E_homo_abs']:.2f}",
            ha="right", va="center", fontsize=8)
    ax.text(xi + bar_half_width + 0.05, d["E_lumo_abs"], f"{d['E_lumo_abs']:.2f}",
            ha="left", va="center", fontsize=8)

ax.axhline(E_H2, color="green", linestyle="--", lw=1.2)
ax.axhline(E_H2O, color="orange", linestyle="--", lw=1.2)
ax.text(len(names) - 0.4, E_H2 + 0.08, r"H$^+$/H$_2$ ($-4.44$ eV)",
        color="green", fontsize=9, ha="right")
ax.text(len(names) - 0.4, E_H2O - 0.20, r"O$_2$/H$_2$O ($-5.67$ eV)",
        color="orange", fontsize=9, ha="right")

ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel("Energy vs vacuum (eV)")
ax.set_title("Band alignment: Ti$_2$CM$_2$ monolayers vs water redox potentials")
ax.set_xlim(-0.6, len(names) - 0.4 + 0.4)
ax.margins(y=0.15)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()
