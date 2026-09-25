import numpy as np

data = np.loadtxt("avg.dat")
z = data[:, 0]              # position z (Bohr)
V_planar = data[:, 1] * 13.6057   # Ry → eV
V_macro = data[:, 2] * 13.6057

grad = np.gradient(V_planar, z)

mask_plateau = np.abs(grad) < 1e-3

if np.any(mask_plateau):
    V_vac = np.mean(V_planar[mask_plateau])
    print(f"Plateau vacuum found: V_vac ≈ {V_vac:.3f} eV")
else:
    print("Plateau vacuum did not found.")

# compare to macroscopic
grad_macro = np.gradient(V_macro, z)
mask_plateau_macro = np.abs(grad_macro) < 1e-3
if np.any(mask_plateau_macro):
    V_vac_macro = np.mean(V_macro[mask_plateau_macro])
    print(f"Plateau vacuum (macroscopic): V_vac ≈ {V_vac_macro:.3f} eV")
