import numpy as np

# =========================================================
# 1. Load data avg.dat
# =========================================================
data = np.loadtxt("avg.dat")
z = data[:, 0]              # posisi z (Bohr)
V_planar = data[:, 1] * 13.6057   # konversi Ry → eV
V_macro = data[:, 2] * 13.6057

# =========================================================
# 2. Cari daerah datar (gradien kecil)
# =========================================================
# Hitung turunan numerik sederhana
grad = np.gradient(V_planar, z)

# Threshold gradien (misalnya |dV/dz| < 1e-3 eV/Bohr dianggap datar)
mask_plateau = np.abs(grad) < 1e-3

# Ambil rata-rata nilai potensial di daerah datar
if np.any(mask_plateau):
    V_vac = np.mean(V_planar[mask_plateau])
    print(f"Plateau vakum terdeteksi: V_vac ≈ {V_vac:.3f} eV")
else:
    print("Tidak ada daerah datar yang jelas terdeteksi.")

# =========================================================
# 3. (Opsional) Bandingkan dengan V_macro
# =========================================================
grad_macro = np.gradient(V_macro, z)
mask_plateau_macro = np.abs(grad_macro) < 1e-3
if np.any(mask_plateau_macro):
    V_vac_macro = np.mean(V_macro[mask_plateau_macro])
    print(f"Plateau vakum (makroskopik): V_vac ≈ {V_vac_macro:.3f} eV")
