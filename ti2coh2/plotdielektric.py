import numpy as np
import matplotlib.pyplot as plt

def load_file(fname):
    data = []
    with open(fname) as f:
        for line in f:
            if line.strip().startswith("#"):
                continue
            try:
                vals = [float(x) for x in line.split()]
                data.append(vals)
            except ValueError:
                continue
    return np.array(data)

epsr = load_file("epsr_clean.dat")
epsi = load_file("epsi_clean.dat")

# samakan panjang
n = min(len(epsr), len(epsi))
energy = epsr[:n,0]
eps_real_z = epsr[:n,3]
eps_imag_z = epsi[:n,3]

plt.figure(figsize=(6,5))
plt.plot(energy, eps_real_z, label="Re(ε) z", color="blue")
plt.plot(energy, eps_imag_z, label="Im(ε) z", color="red")
plt.xlabel("Energy (eV)")
plt.ylabel("Dielectric function")
plt.legend()
plt.tight_layout()
plt.show()

