"""
Robust loader + plotter untuk output epsilon.x (dielectric & absorption).

Menangani 3 masalah:
1. Overflow (****) diganti NaN di tempat -> baris TIDAK dibuang -> energi
   di file real & imaginer tetap berpasangan benar.
2. Komponen in-plane (rata-rata x,y) dipakai, bukan z (out-of-plane).
3. Rescaling terhadap C referensi supaya magnitude antar-material sebanding.
"""

import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

RY_UNUSED = None  # eps sudah dimensionless, tidak perlu konversi Ry->eV di sini

# =========================================================
# 1. Loader robust: overflow -> NaN, baris tetap utuh
# =========================================================
def load_eps_file(fname, expected_cols=4):
    rows = []
    n_bad = 0
    with open(fname) as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # fix angka negatif yang nempel (mis. "1.234-5.678" -> "1.234 -5.678")
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
                print(f"  [WARNING] {fname} baris {lineno}: dapat {len(vals)} "
                      f"kolom, harusnya {expected_cols} -- kemungkinan overflow "
                      f"bergabung (raw: {line!r}). Kolom yang hilang diisi NaN.")
                # pertahankan energi (token pertama) kalau valid, sisanya NaN
                fixed = [vals[0] if vals else np.nan]
                fixed += [np.nan] * (expected_cols - 1)
                vals = fixed

            rows.append(vals)

    if n_bad:
        print(f"  -> total {n_bad} baris bermasalah di {fname} (lihat warning di atas)")

    return np.array(rows, dtype=float)


def load_material(epsr_path, epsi_path, C_material, C_ref):
    """
    epsr_path, epsi_path: path lengkap ke file epsr_*.dat dan epsi_*.dat
    Return: energy, eps1_inplane_rescaled, eps2_inplane_rescaled
    """
    epsr = load_eps_file(epsr_path)
    epsi = load_eps_file(epsi_path)

    assert epsr.shape[0] == epsi.shape[0], (
        f"Jumlah baris epsr ({epsr.shape[0]}) dan epsi ({epsi.shape[0]}) "
        "beda -- cek apakah nw di kedua run sama, dan apakah masih ada "
        "baris yang ke-drop (bukan cuma di-NaN-kan)."
    )

    energy = epsr[:, 0]
    # kolom 1,2,3 = x,y,z. Ambil rata-rata in-plane (x,y).
    eps1_inplane = np.nanmean(epsr[:, [1, 2]], axis=1)
    eps2_inplane = np.nanmean(epsi[:, [1, 2]], axis=1)

    # rescale ke C_ref supaya magnitude antar-material sebanding
    scale = C_material / C_ref
    eps1_rescaled = 1.0 + (eps1_inplane - 1.0) * scale
    eps2_rescaled = eps2_inplane * scale

    return energy, eps1_rescaled, eps2_rescaled


# =========================================================
# 2. Hitung absorption coefficient (dalam cm^-1)
# =========================================================
def absorption_coeff(energy_eV, eps1, eps2):
    hbar = 1.055e-34   # J.s
    e_charge = 1.602e-19
    c = 2.998e8        # m/s
    omega = energy_eV * e_charge / hbar
    n_eff = np.sqrt(np.sqrt(eps1**2 + eps2**2) - eps1)  # bisa NaN kalau argumen negatif -> cek!
    alpha_per_m = np.sqrt(2) * omega / c * n_eff
    return alpha_per_m * 1e-2  # -> cm^-1


# =========================================================
# 3. Load ketiga material, pakai C terbesar (Ti2C(OH)2) sbg referensi
# =========================================================
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
# NOTE: path di atas relatif -- jalankan script ini dari sebuah folder di
# sejajar ti2co2/, ti2cf2/, ti2coh2/ (mis. taruh script di root repo), atau
# ganti jadi path absolut sesuai lokasi masing-masing file di PC-mu.

results = {}
for name, d in materials.items():
    energy, eps1, eps2 = load_material(d["epsr"], d["epsi"], d["C"], C_ref)
    alpha = absorption_coeff(energy, eps1, eps2)
    results[name] = dict(energy=energy, eps1=eps1, eps2=eps2, alpha=alpha, color=d["color"])

# =========================================================
# 7. Cek nilai minimum Re(ε) di range 1.5–4 eV
# =========================================================
for name, r in results.items():
    mask = (r["energy"] >= 1.5) & (r["energy"] <= 4.0)
    eps1_range = r["eps1"][mask]
    if eps1_range.size > 0:
        print(f"{name}: min Re(ε) di 1.5–4 eV = {np.nanmin(eps1_range):.3f}")
    else:
        print(f"{name}: tidak ada data di range 1.5–4 eV")

# =========================================================
# 4. Plot dielectric function (in-plane, rescaled)
# =========================================================
fig, ax = plt.subplots(figsize=(7, 5))
for name, r in results.items():
    ax.plot(r["energy"], r["eps2"], color=r["color"], label=f"Im(ε) in-plane -- {name}")
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Im(ε), in-plane, rescaled")
ax.set_xlim(0, 10)
ax.legend()
plt.tight_layout()
plt.savefig("dielectric_inplane_comparison.png", dpi=200)

# =========================================================
# 5. Plot absorption spectrum (in-plane, rescaled)
# =========================================================
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
plt.savefig("absorption_inplane_comparison.png", dpi=200)

plt.show()
# =========================================================
# 6. Plot Re(ε) (in-plane, rescaled) di 1.5–4 eV
# =========================================================
fig, ax = plt.subplots(figsize=(7, 5))
for name, r in results.items():
    ax.plot(r["energy"], r["eps1"], color=r["color"], label=f"Re(ε) -- {name}")
ax.set_xlabel("Photon Energy (eV)")
ax.set_ylabel("Re(ε), in-plane, rescaled")
ax.set_xlim(1.5, 4.0)
ax.axhline(0, color="black", linestyle="--", linewidth=0.8)  # garis nol
ax.legend()
plt.tight_layout()
plt.savefig("eps1_inplane_comparison.png", dpi=200)

plt.show()
