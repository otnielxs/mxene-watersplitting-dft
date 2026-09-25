import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 1. Load data dari avg.dat
# =========================================================
data = np.loadtxt("avg.dat")
z = data[:, 0]        # posisi z (Bohr)

# Konversi Ry → eV (faktor 13.6057)
Ry_to_eV = 13.6057
V_planar = data[:, 1] * Ry_to_eV   # V_p(z) dalam eV
V_macro = data[:, 2] * Ry_to_eV    # V_m(z) dalam eV

# =========================================================
# 2. Parameter Fermi level dan work function
# =========================================================
E_F = 2.3778           # Fermi level (eV)

# Otomatis mengambil nilai potensial vakum (nilai maksimum/plateau pada V_planar)
V_vac = np.max(V_planar)
Phi = V_vac - E_F     # Work function (\Phi)

# Posisi z untuk menempatkan garis panah vertikal (misal di daerah vakum dekat z = 20 Bohr)
z_arrow = 20.0

# =========================================================
# 3. Plot
# =========================================================
plt.figure(figsize=(7, 5))
plt.plot(z, V_planar, color='purple', label=r'$V_p(z)$ - Planar')
plt.plot(z, V_macro, color='teal', label=r'$V_m(z)$ - Macroscopic')

# Garis Fermi level
plt.axhline(E_F, color='blue', linestyle='--', linewidth=1.2, label=r'$E_F$ - Fermi')

# ---------------------------------------------------------
# Tambahan: Garis vertikal otomatis (panah ganda) & Teks Value
# ---------------------------------------------------------
plt.annotate(
    '',
    xy=(z_arrow, V_vac),
    xytext=(z_arrow, E_F),
    arrowprops=dict(arrowstyle='<->', color='black', lw=1.5)
)

# Label nilai \Phi di samping panah
plt.text(
    z_arrow + 0.5, (E_F + V_vac) / 2,
    f'$\Phi \\sim {Phi:.2f}$ eV',
    va='center', ha='left', fontsize=10, color='black'
)

# =========================================================
# 4. Format plot
# =========================================================
plt.xlabel("Position z (Bohr)")
plt.ylabel("Energy (eV)")
plt.legend()
plt.grid(False)
plt.tight_layout()
plt.show()
