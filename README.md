# Termination-Dependent Electronic and Optical Screening of Ti₂C MXene Monolayers for Photocatalytic Water Splitting: A DFT Study

A computational screening study of three termination groups (=O, =F, -OH) on the Ti₂C MXene monolayer, using periodic DFT (Quantum ESPRESSO) to evaluate their electronic structure, band-edge alignment against water redox potentials, and optical absorption — as a standalone-monolayer complement to heterostructure-based overall-water-splitting studies such as Xu *et al.* (2020) on M₂CO₂/MoS₂ (M = Ti, Zr, Hf) van der Waals heterostructures.

## Motivation

Heterostructure-based photocatalyst design (e.g. Ti₂CO₂/MoS₂ type-II heterostructures) typically begins by screening the electronic character of each constituent monolayer before pairing them. This project isolates that first step: rather than reproducing the Ti₂CO₂/MoS₂ heterostructure already studied in prior thesis work, it asks a narrower question — **can a Ti₂C MXene monolayer alone, under different terminations, satisfy the electronic requirements for overall water splitting, and how does termination change its optical response?**

This project also serves as a deliberate methods-expansion exercise: it is the first use of `epsilon.x` (dielectric function / optical absorption) in this line of work, building on the periodic-DFT + post-processing pipeline established in the prior gas-sensing project.

## Research Questions

- Which Ti₂C terminations (O, F, OH) remain semiconducting, and which become metallic?
- For the semiconducting case, does its band-edge position (referenced to vacuum) straddle both water redox potentials (H⁺/H₂ at −4.44 eV, O₂/H₂O at −5.67 eV) — i.e. is it capable of *overall* water splitting on its own, or only half the reaction?
- How does termination affect optical absorption in the visible range (1.5–4 eV), and can absorption strength alone be used to judge photocatalytic promise?

## Materials Studied

| Material | Role | Electronic character (this work) |
|---|---|---|
| Ti₂CO₂ | Baseline / primary candidate (reuses parameters established in prior thesis work) | Semiconductor, gap ≈ 0.33 eV |
| Ti₂CF₂ | New termination, contrast case | Metallic (band overlap) |
| Ti₂C(OH)₂ | New termination, contrast case | Metallic (band overlap) |

Zr and Hf (also studied in Xu *et al.* 2020) were intentionally excluded to keep the project tractable on local CPU-only hardware — see Limitations.

## Methodology (summary — full detail in [`docs/methodology.md`](docs/methodology.md))

1. **Structure & ground-state electronics**: `relax` → `scf` → `nscf`/`bands.x` (band structure) → `projwfc.x` (DOS), using PAW pseudopotentials, DFT-D3 dispersion, Marzari-Vanderbilt smearing.
2. **Work function / band-edge alignment**: `pp.x` (`plot_num=11`) planar-averaged electrostatic potential → vacuum plateau → Φ = V_vacuum − E_Fermi → VBM/CBM referenced to vacuum → compared against the −4.44 eV / −5.67 eV redox lines.
3. **Optical properties**: separate dense-k, high-`nbnd` `nscf` run with **norm-conserving** pseudopotentials (required by `epsilon.x`; not compatible with the PAW pseudopotentials used elsewhere) → `epsilon.x` → dielectric function (in-plane, x/y-averaged) → absorption coefficient.

This follows the band-edge-alignment approach used in Xu *et al.* (2020) rather than a computational-hydrogen-electrode (CHE) approach — i.e. the water redox potentials are taken as fixed literature reference values, and **no explicit DFT calculation of H₂O, H₂, or adsorbed reaction intermediates was performed**. A CHE-based Gibbs-free-energy analysis (which would require those molecule/intermediate calculations) is out of scope for this project.

## Key Results

### Electronic structure

| Material | Total energy (Ry) | HOMO/VBM (eV, internal) | LUMO/CBM (eV, internal) | E_Fermi (eV) | Gap |
|---|---|---|---|---|---|
| Ti₂CO₂ | −469.60316 | −0.2923 | 0.0412 | −0.1357 | ≈0.33 eV (semiconductor) |
| Ti₂CF₂ | −505.04060 | 0.5901 | 0.4385 | 0.4327 | Overlap (metallic) |
| Ti₂C(OH)₂ | −471.90858 | 2.6866 | 2.3676 | 2.3778 | Overlap (metallic) |

### Work function and band alignment vs. vacuum

| Material | Φ (eV) | VBM/HOMO vs vacuum (eV) | CBM/LUMO vs vacuum (eV) |
|---|---|---|---|
| Ti₂CO₂ | 5.669 | −5.825 | −5.492 |
| Ti₂CF₂ | 4.834 | −4.677 | −4.829 |
| Ti₂C(OH)₂ | 2.081 | −1.772 | −2.091 |

Compared against H⁺/H₂ (−4.44 eV) and O₂/H₂O (−5.67 eV):

- **Ti₂CO₂**: VBM (−5.825 eV) is below −5.67 eV → **OER-capable**. CBM (−5.492 eV) is *not* above −4.44 eV → **not HER-capable on its own** (short by ≈1.05 eV). Ti₂CO₂ monolayer alone can only drive half of overall water splitting.
- **Ti₂CF₂ / Ti₂C(OH)₂**: metallic — the straddling-gap criterion does not apply; both are disqualified as standalone overall-water-splitting photocatalysts regardless of band-edge position.

This directly rationalizes the heterostructure strategy in Xu *et al.* (2020): pairing Ti₂CO₂ (OER-capable) with a partner supplying a shallower CBM (e.g. MoS₂, HER-capable) is what makes the *combined* type-II heterostructure viable, where the monolayer alone is not.

### Optical properties (visible range, 1.5–4 eV, in-plane component)

- All three materials show absorption coefficients on the order of 10⁵ cm⁻¹ in the visible range, typical for 2D materials.
- Ti₂CO₂'s Re(ε) is positive and well-behaved in this window once `nbnd`/`ecutwfc`/k-mesh were converged, consistent with genuine semiconductor interband absorption.
- Ti₂CF₂ and Ti₂C(OH)₂ show **negative Re(ε)** in this window, indicating their large absorption coefficients reflect plasmonic/reflective screening response rather than genuine interband absorption available for photocatalysis. This is consistent with, and reinforces, their disqualification on electronic-structure grounds.

## Answers to the Research Questions

**Q1 — Which terminations remain semiconducting?** Only Ti₂CO₂, matching the majority-consensus GGA-PBE literature that Ti₂CF₂ and Ti₂C(OH)₂ remain metallic even after full termination.

**Q2 — Does Ti₂CO₂ alone satisfy overall water splitting?** No. It satisfies the OER half-reaction requirement but not HER — consistent with why the literature pursues it as a heterostructure component rather than a standalone photocatalyst.

**Q3 — Does absorption strength alone indicate photocatalytic promise?** No. Ti₂CF₂ shows the strongest apparent absorption of the three, but this is dominated by a plasmonic/reflective (negative Re(ε)) response rather than usable interband absorption — a caution against reading absorption magnitude in isolation from electronic-structure results.

## Limitations

- Only the Ti₂C family was studied (Zr₂C, Hf₂C from Xu *et al.* 2020 excluded) to keep the project feasible on local CPU-only hardware (WSL2, no working GPU-accelerated QE build).
- No AIMD-based thermal stability check was performed; stability is inferred only from successful structural relaxation.
- Band-edge-alignment method only — no computational-hydrogen-electrode (CHE) Gibbs-free-energy analysis, and no explicit DFT calculation of H₂O/H₂ or adsorbed reaction intermediates.
- PBE is known to underestimate band gaps; no scissor correction (`shift`) was applied to the optical spectra, so reported gaps/transition energies are PBE-level, not experimental-level.
- Optical calculations required switching from PAW to norm-conserving pseudopotentials (`epsilon.x` does not support PAW/USPP); the PAW-relaxed geometry was reused as-is for the norm-conserving `nscf`/`epsilon.x` run rather than re-relaxing with norm-conserving pseudopotentials.
- `epsilon.x`'s standard interband formalism diverges near ω→0 for metallic systems even with `intrasmear` active; results below ~1 eV were excluded from analysis for all three materials.
- Absolute optical magnitudes are only directly comparable across materials after rescaling by cell height (C), since Ti₂CO₂, Ti₂CF₂, and Ti₂C(OH)₂ were built with different vacuum/cell thicknesses (21.43 / 21.79 / 23.79 Å respectively).
- Absorption coefficients for the metallic materials (Ti₂CF₂, Ti₂C(OH)₂) should be read qualitatively (relative peak positions), not as absolute usable-absorption figures, since they are dominated by a negative-Re(ε) plasmonic response rather than pure interband absorption.
- Ti₂CF₂'s reported local magnetic moment in some literature was not tested here (all calculations non-spin-polarized); this remains an open item.
- Convergence parameters for the optical calculations were pushed as far as local hardware allowed (up to `nbnd=200`, `ecutwfc=60` Ry, 18×18×1 k-mesh for Ti₂CO₂) and were not pushed further given laptop resource constraints; results are considered converged for the purposes of this project but not exhaustively stress-tested.

## Repository Structure

```
mxene-watersplitting-dft/
├── README.md
├── ti2co2/
│   ├── relax/  scf/  bands/  dos/  workfunction/  optical/
├── ti2cf2/
│   ├── relax/  scf/  bands/  dos/  workfunction/  optical/
├── ti2coh2/
│   ├── relax/  scf/  bands/  dos/  workfunction/  optical/
├── scripts/
│   ├── Vplateau.py              # workfunction: plateau detection, Ry->eV fix
│   ├── band_alignment_plot.py   # VBM/CBM vs vacuum, vs redox potentials
│   └── optical.py               # dielectric/absorption: in-plane averaging,
│                                 # C-rescaling, overflow-safe parsing
├── figures/
└── docs/
    └── methodology.md
```

## Software Used

- [Quantum ESPRESSO](https://www.quantum-espresso.org/) — periodic DFT calculations (`pw.x`, `pp.x`, `projwfc.x`, `epsilon.x`)
- Python (NumPy, Matplotlib) — post-processing, plotting

## Reproducing the Results

```bash
# Ground state
cd ti2co2/relax  && pw.x < relax.in  > relax.out
cd ../scf        && pw.x < scf.in    > scf.out
cd ../bands      && pw.x < nscf.in   > nscf.out && bands.x < bands.in > bands.out
cd ../dos        && projwfc.x < dos.in > dos.out

# Work function / band alignment
cd ../workfunction && pp.x < pp.in > pp.out
python3 ../../scripts/Vplateau.py
python3 ../../scripts/band_alignment_plot.py

# Optical (note: separate norm-conserving pseudopotentials required)
cd ../optical && pw.x < nscf_optical.in > nscf_optical.out
epsilon.x < epsilon.in > eps.out
python3 ../../scripts/optical.py
```

Repeat for `ti2cf2/` and `ti2coh2/`.
