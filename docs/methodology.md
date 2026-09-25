Methodology

## 1. Computational Parameters

### 1.1 Energy Cutoff (ecutwfc / ecutrho)

Ti₂CO₂ ground-state calculations (relax, scf, bands, DOS, workfunction) reused the cutoff established in prior thesis work on the Ti₂CO₂/MoS₂ heterostructure. Ti₂CF₂ and Ti₂C(OH)₂ used the same PAW-consistent cutoff for their ground-state pipeline.

- Ground-state pipeline (all three materials): ecutwfc = 40 Ry, ecutrho = 320 Ry (PAW pseudopotentials)
- Optical pipeline (all three materials, separate run — see Section 3): norm-conserving pseudopotentials required a different, higher cutoff. Ti₂CO₂'s optical run needed ecutwfc = 60 Ry, ecutrho = 480 Ry to obtain a converged, positive Re(ε) in the 1.5–4 eV window; Ti₂CF₂ and Ti₂C(OH)₂ optical runs used ecutwfc = 40 Ry, ecutrho = 320 Ry.
- No further cutoff increase was attempted beyond what was needed to obtain a stable, physically sensible Re(ε) for Ti₂CO₂, given local CPU-only hardware constraints (see Limitations).

### 1.2 K-point Sampling

- Relax / scf / ground-state DOS: 4x4x1 / 6×6×1 / 8x8x1 / Monkhorst-Pack, Γ-centered.
- Band structure: standard high-symmetry path (Γ–K–M–Γ) for the hexagonal 2D lattice.
- Optical `nscf` (dense-k run feeding `epsilon.x`): `nosym = .true.`, `noinv = .true.` (required — `epsilon.x` does not unfold symmetry-reduced k-meshes, so an unreduced full-BZ mesh is mandatory for correct optical matrix elements). K-mesh density was increased per material to reach convergence: Ti₂CF₂/Ti₂C(OH)₂ at 12×12×1; Ti₂CO₂ required 18×18×1 before Re(ε) stabilized to a physically sensible (positive) value in the visible window.

### 1.3 Smearing and SCF Settings

- Smearing scheme: Marzari-Vanderbilt (cold smearing), `degauss = 0.02` Ry, used for **all three materials including Ti₂CO₂** — consistent with the semi-metallic/narrow-gap treatment already established for Ti₂CO₂ in prior project work, rather than switching to fixed occupations for the semiconducting case.
- Mixing beta: default, except where noted for troubleshooting metallic/optical convergence.
- `epsilon.x` reports "the system is a metal" whenever smearing-based occupations are used in the preceding `pw.x` run, regardless of the material's true gap — this is a labeling artifact of the occupation scheme, not a statement about Ti₂CO₂'s actual band structure (confirmed separately via VBM/CBM values from `nscf` output).

## 2. Slab Construction

- Vacuum thickness: ~15–18 Å equivalent in-plane, achieved via cell parameter `C`. Note that `C` differs by material because termination geometry differs physically (OH groups project further from the Ti₂C core than O or F), not purely as a vacuum-padding choice:
  - Ti₂CO₂: C = 21.42568 Å
  - Ti₂CF₂: C = 21.78628 Å
  - Ti₂C(OH)₂: C = 23.78628 Å
- Termination groups studied: =O, =F, -OH on the Ti₂C core, chosen specifically to differ from the =O-only monolayer already treated (as part of a heterostructure) in prior thesis work.
- Zr₂C / Hf₂C analogues (present in the Xu *et al.* 2020 reference paper) were not studied — see Limitations.

## 3. Pseudopotential Strategy: PAW for Ground State, Norm-Conserving for Optical

A material-specific split was required because `epsilon.x` does not support PAW or ultrasoft pseudopotentials (`grid_build` error: "USPP are not implemented"):

- **Ground-state pipeline** (relax, scf, bands, DOS, workfunction): PAW pseudopotentials (`*.pbe-*-kjpaw_psl.1.0.0.UPF`), consistent with prior project conventions.
- **Optical pipeline** (`nscf` feeding `epsilon.x`): norm-conserving pseudopotentials (plain `*.upf`, e.g. ONCV-type), required by `epsilon.x`'s dipole-matrix-element implementation.
- The PAW-relaxed geometry was reused as-is for the norm-conserving `nscf` run, rather than re-relaxing the structure with norm-conserving pseudopotentials. This is an accepted approximation for this project's scope — see Limitations.

## 4. Work Function and Band-Edge Alignment Method

- `pp.x` with `plot_num = 11` (V_bare + V_Hartree, no XC — appropriate for work function since XC is not long-range in vacuum) produces the planar-averaged electrostatic potential V(z).
- **Unit pitfall (identified and corrected during this project):** `pp.x`/`average.x` output is in **Rydberg**, not eV, while `pw.x`'s reported Fermi energy and VBM/CBM values are already in eV. An initial pass mixed these units directly, producing unphysical work functions (including a negative Φ for Ti₂C(OH)₂). Fix: multiply the potential column by 13.6057 (Ry→eV) before combining with `pw.x`-derived energies.
- Vacuum plateau value V_vacuum extracted via a gradient-threshold plateau detector (`|dV/dz| < 1e-3` eV/Bohr) rather than a manually chosen single point.
- Φ = V_vacuum − E_Fermi. Band edges referenced to vacuum: E_abs = E_internal − V_vacuum.
- Water redox reference levels (H⁺/H₂ = −4.44 eV, O₂/H₂O = −5.67 eV vs. vacuum, pH 0) taken as fixed literature constants, following the band-edge-alignment approach of Xu *et al.* (2020) — not recomputed via any DFT calculation on H₂O or H₂ molecules.

## 5. Optical Property Calculation (`epsilon.x`)

- Separate `nscf` run per material: dense, unreduced k-mesh (`nosym`/`noinv` = `.true.`), increased `nbnd` (empty bands) relative to the ground-state pipeline. `nbnd` was increased stepwise (80 → 120 → 200 for Ti₂CO₂) until Re(ε) in the 1.5–4 eV window stabilized to a physically sensible sign and magnitude.
- `epsilon.x` input: `calculation = 'eps'`, `smeartype = 'mv'`, `intersmear = 0.10` eV (all materials), `intrasmear` set to 0.0 for Ti₂CO₂ (semiconductor) and 0.10 eV for Ti₂CF₂/Ti₂C(OH)₂ (metallic, to include the intraband/Drude contribution).
- Output columns are per-Cartesian-component (x, y, z). The **in-plane average (x, y)** was used for all reported dielectric/absorption results, since normal-incidence illumination on a 2D sheet couples to the in-plane response; the out-of-plane (z) component was computed but is not the physically relevant quantity for this application.
- **Cross-material magnitude comparison** requires rescaling for differing cell height C (Section 2), since ε computed from a 3D-periodic slab is diluted inversely with vacuum thickness: `eps1_rescaled = 1 + (eps1_raw - 1) * (C / C_ref)`, `eps2_rescaled = eps2_raw * (C / C_ref)`, with C_ref taken as the largest C among the three materials (Ti₂C(OH)₂). Peak *positions* (transition energies) are unaffected by this rescaling; only magnitude comparisons require it.
- **Sub-1 eV artifacts:** all three materials show large, non-physical or only-partially-physical values immediately near ω → 0 (a single grid point at 0.001 eV in each raw output file). For the metallic materials this is a genuine (if `intrasmear`-broadened) Drude-term divergence; for Ti₂CO₂ it is attributed to Kramers-Kronig numerical noise very close to ω = 0. In both cases, results below ~1 eV are excluded from the analysis, which focuses on the 1.5–4 eV visible window relevant to solar-driven photocatalysis.
- **Interpretation caveat for metallic materials:** Ti₂CF₂ and Ti₂C(OH)₂ show large absorption coefficients in the visible window but **negative Re(ε)** there, meaning the apparent absorption is dominated by a plasmonic/reflective response (high reflectivity, short skin depth) rather than genuine interband absorption usable for electron-hole generation. This is a qualitative reading of the existing Re(ε)/Im(ε) data; a quantitative reflectivity calculation (R(ω) from the complex refractive index) was identified as a natural follow-up but not computed in this project.

## 6. Data-Processing Pipeline Issues (identified and fixed during this project)

- **Row misalignment risk from overflow handling:** `epsilon.x` output can contain overflow tokens (`***...`) when a value exceeds its fixed field width. An initial cleaning approach (`grep -v '\*\*\*'`) dropped offending lines independently from the real-part and imaginary-part files; because overflow can occur on different rows in each file, this risked pairing Re(ε) and Im(ε) values from *different* energy grid points after naive index-based truncation. Fix: replace overflow tokens with `NaN` in place (never drop rows), so row count and energy-grid alignment between the real and imaginary files is always preserved. Confirmed in practice: raw `epsr_*.dat`/`epsi_*.dat` files for all three materials had identical line counts (1002 = 1 header + 1001 grid points from `nw = 1000`).
- **Fortran fixed-width column merging:** two adjacent overflowing fields (no separator when both fields are entirely filled with `*`) can merge into a single whitespace-delimited token, silently reducing the apparent column count for that row. Fix: rows with fewer than the expected 4 columns (energy, x, y, z) are flagged with an explicit warning (file name, line number, raw content) and padded with `NaN` for the missing columns rather than mis-assigned to the wrong column. In practice this affected exactly one row per file (the ω = 0.001 eV point, already excluded per Section 5), for all three materials.
- **Negative-sign concatenation:** Fortran fixed-format output does not always insert a space between a positive number and an immediately following negative number; regex-based insertion of a space before `-` when preceded by a digit resolves this without affecting legitimate scientific-notation tokens (not applicable here, since no `E`-notation is used in ε output).

## 7. Limitations and Assumptions

- Only the Ti₂C family (O, F, OH terminations) was studied; Zr₂C and Hf₂C from the reference paper were excluded to keep the project tractable on local, CPU-only hardware (WSL2, RTX 3050 with no working GPU-accelerated QE build).
- No AIMD-based thermal/dynamical stability check was performed for any of the three monolayers.
- Band-edge-alignment method only, following Xu *et al.* (2020); no computational-hydrogen-electrode (CHE) Gibbs-free-energy pathway was computed, and no explicit DFT calculation of H₂O, H₂, or adsorbed intermediates (H*, OH*, O*, OOH*) was performed.
- PBE band gaps are known to be underestimated relative to experiment; no scissor correction (`shift` in `epsilon.x`) was applied.
- Geometry used for the optical (norm-conserving) pipeline was carried over from the PAW-relaxed structure without re-relaxing under norm-conserving pseudopotentials.
- Ti₂CF₂'s reported local magnetic moment in parts of the literature was not tested; all calculations here are non-spin-polarized (`nspin` default).
- Convergence testing for the optical pipeline was pushed as far as practical on available hardware (up to `nbnd = 200`, `ecutwfc = 60` Ry, 18×18×1 k-mesh for Ti₂CO₂) and stopped once Re(ε) stabilized; no further stress-testing (e.g. even higher `nbnd`/k-mesh) was pursued given local resource constraints.
- Quantitative reflectivity R(ω) for the metallic materials was identified as a useful follow-up to substantiate the "plasmonic, not absorptive" interpretation but was not computed.

## Revision Log

| Stage | Change |
|---|---|
| Scoping | Defined project as standalone Ti₂CM₂ monolayer screening (O, F, OH), distinct from prior Ti₂CO₂/MoS₂ heterostructure thesis work; decided to add `epsilon.x` as a new method |
| Ground state | Relax, scf, nscf, bands, DOS, workfunction completed for all three materials |
| Workfunction debugging | Identified and fixed Ry→eV unit bug in `pp.x`/`average.x` post-processing |
| Band alignment | Computed VBM/CBM vs. vacuum for all three; established Ti₂CO₂ as OER-only, Ti₂CF₂/Ti₂C(OH)₂ as disqualified (metallic) |
| Optical, first pass | `epsilon.x` failed with PAW pseudopotentials (USPP not implemented); switched to norm-conserving pseudopotentials for the optical pipeline |
| Optical, convergence | Iteratively increased `nbnd`/`ecutwfc`/k-mesh for Ti₂CO₂ until Re(ε) in the visible window converged to a physically sensible positive value |
| Data pipeline fixes | Replaced line-dropping overflow cleanup with in-place NaN substitution to preserve energy-grid alignment; switched from out-of-plane (z) to in-plane (x,y) dielectric components; added C-rescaling for cross-material magnitude comparison |
| Interpretation | Attributed high apparent absorption in metallic materials to plasmonic/negative-Re(ε) response rather than genuine interband absorption |
