import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("avg.dat")
z = data[:, 0]        # position z (Bohr)

Ry_to_eV = 13.6057
V_planar = data[:, 1] * Ry_to_eV   # V_p(z) dalam eV
V_macro = data[:, 2] * Ry_to_eV    # V_m(z) dalam eV

E_F = 0.4327           # Fermi from scf.out

V_vac = np.max(V_planar)
Phi = V_vac - E_F     # Work function (\Phi)

z_arrow = 20.0 # position where V plateau

plt.figure(figsize=(7, 5))
plt.plot(z, V_planar, color='purple', label=r'$V_p(z)$ - Planar')
plt.plot(z, V_macro, color='teal', label=r'$V_m(z)$ - Macroscopic')

plt.axhline(E_F, color='blue', linestyle='--', linewidth=1.2, label=r'$E_F$ - Fermi')

plt.annotate(
    '',
    xy=(z_arrow, V_vac),
    xytext=(z_arrow, E_F),
    arrowprops=dict(arrowstyle='<->', color='black', lw=1.5)
)

plt.text(
    z_arrow + 0.5, (E_F + V_vac) / 2,
    f'$\Phi \\sim {Phi:.2f}$ eV',
    va='center', ha='left', fontsize=10, color='black'
)

plt.xlabel("Position z (Bohr)")
plt.ylabel("Energy (eV)")
plt.legend()
plt.grid(False)
plt.tight_layout()
plt.show()
