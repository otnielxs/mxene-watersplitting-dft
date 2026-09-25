import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

RY_UNUSED = None

def load_eps_file(fname, expected_cols=4):
    rows = []
    n_bad = 0
    with open(fname) as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # fix negative numbers
            line = re.sub(r'(\d)-', r'\1 -', line)
            tokens = line.split()
            vals = []
            for t in tokens:
                if "*" in t:
                    vals.append(np.nan)
                else:
                    try:
                        vals.append(float(t))
                    except ValueError:
                        vals.append(np.nan)

            if len(vals) != expected_cols:
                n_bad += 1
                print(f"  [WARNING] {fname} row {lineno}: get {len(vals)} "
                      f"coloumn, should be {expected_cols} -- maybe overflow "
                      f"get into (raw: {line!r}). loss coloumn will be NaN.")
                fixed = [vals[0] if vals else np.nan]
                fixed += [np.nan] * (expected_cols - 1)
                vals = fixed

            rows.append(vals)

    if n_bad:
        print(f"  -> total {n_bad} corrupted row in {fname} (check warning)")

    return np.array(rows, dtype=float)


def load_material(epsr_path, epsi_path, C_material, C_ref):
    """
    epsr_path, epsi_path: path lengkap ke file epsr_*.dat dan epsi_*.dat
    Return: energy, eps1_inplane_rescaled, eps2_inplane_rescaled
    """
    epsr = load_eps_file(epsr_path)
    epsi = load_eps_file(epsi_path)

    assert epsr.shape[0] == epsi.shape[0], (
        f"Rows epsr ({epsr.shape[0]}) and epsi ({epsi.shape[0]}) "
        "diff -- check"
        "Row that dropped (not only NaN)."
    )

    energy = epsr[:, 0]
    # coloumn 1,2,3 = x,y,z. Average in-plane (x,y).
    eps1_inplane = np.nanmean(epsr[:, [1, 2]], axis=1)
    eps2_inplane = np.nanmean(epsi[:, [1, 2]], axis=1)

    # rescale to C_ref
    scale = C_material / C_ref
    eps1_rescaled = 1.0 + (eps1_inplane - 1.0) * scale
    eps2_rescaled = eps2_inplane * scale

    return energy, eps1_rescaled, eps2_rescaled

def absorption_coeff(energy_eV, eps1, eps2):
    hbar = 1.055e-34   # J.s
    e_charge = 1.602e-19
    c = 2.998e8        # m/s
    omega = energy_eV * e_charge / hbar
    n_eff = np.sqrt(np.sqrt(eps1**2 + eps2**2) - eps1)  # can be NaN if negative -> check!
    alpha_per_m = np.sqrt(2) * omega / c * n_eff
    return alpha_per_m * 1e-2  # -> cm^-1

C_ref = 23.78628

materials = {
    "Ti2CO2": {
        "epsr": "/home/otnielsitepu/mxene-watersplitting-dft/ti2co2/epsr_ti2co2_eps.dat",
        "epsi": "/home/otnielsitepu/mxene-watersplitting-dft/ti2co2/epsi_ti2co2_eps.dat",
        "C": 21.42568, "color": "tab:blue",
    },
    "Ti2CF2": {
        "epsr": "/home/otnielsitepu/mxene-watersplitting-dft/ti2cf2/epsr_ti2cf2_eps.dat",
        "epsi": "/home/otnielsitepu/mxene-watersplitting-dft/ti2cf2/epsi_ti2cf2_eps.dat",
        "C": 21.78628, "color": "tab:orange",
    },
    "Ti2C(OH)2": {
        "epsr": "/home/otnielsitepu/mxene-watersplitting-dft/ti2coh2/epsr_ti2coh2_eps.dat",
        "epsi": "/home/otnielsitepu/mxene-watersplitting-dft/ti2coh2/epsi_ti2coh2_eps.dat",
        "C": 23.78628, "color": "tab:green",
    },
}
# NOTE: run in actual path

results = {}
for name, d in materials.items():
    energy, eps1, eps2 = load_material(d["epsr"], d["epsi"], d["C"], C_ref)
    alpha = absorption_coeff(energy, eps1, eps2)
    results[name] = dict(energy=energy, eps1=eps1, eps2=eps2, alpha=alpha, color=d["color"])

#check minimum
for name, r in results.items():
    mask = (r["energy"] >= 1.5) & (r["energy"] <= 4.0)
    eps1_range = r["eps1"][mask]
    if eps1_range.size > 0:
        print(f"{name}: min Re(ε) at 1.5–4 eV = {np.nanmin(eps1_range):.3f}")
    else:
        print(f"{name}: not found at range 1.5–4 eV")

fig, ax = plt.subplots(figsize=(7, 5))
for name, r in results.items():
    ax.plot(r["energy"], r["eps2"], color=r["color"], label=f"Im(ε) in-plane -- {name}")
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Im(ε), in-plane, rescaled")
ax.set_xlim(0, 10)
ax.legend()
plt.tight_layout()

fig, ax = plt.subplots(figsize=(7, 5))
for name, r in results.items():
    ax.plot(r["energy"], r["alpha"], color=r["color"], label=name)
ax.set_xlabel("Photon Energy (eV)")
ax.set_ylabel("Absorption coefficient (cm$^{-1}$)")
ax.set_xlim(1.5, 4.0)
ax.legend()
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(axis="y", style="sci", scilimits=(5, 5))
plt.tight_layout()

plt.show()

fig, ax = plt.subplots(figsize=(7, 5))
for name, r in results.items():
    ax.plot(r["energy"], r["eps1"], color=r["color"], label=f"Re(ε) -- {name}")
ax.set_xlabel("Photon Energy (eV)")
ax.set_ylabel("Re(ε), in-plane, rescaled")
ax.set_xlim(1.5, 4.0)
ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
ax.legend()
plt.tight_layout()

plt.show()
