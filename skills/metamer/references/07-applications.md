# 07 — Applications

Each application is a coordinate transform of κ into a specific domain. This file is the field reference — what `r` means in each domain, what parameter sets are in use, what's been built.

---

## 7.1 Prism — spectral sky

Per-pixel spectral ray march through a spherical atmosphere, replacing the game's precomputed inscatter LUT.

### Geometry

| Quantity | Value |
|---|---|
| Planet radius | 6,371 km |
| Atmosphere height | 100 km (Kármán line) |
| Rayleigh scale height | 8.5 km |
| Mie scale height | 1.2 km |
| Ozone layer center | 25 km altitude |
| Ozone Gaussian width | 15 km |

### Wavelength sampling

| Mode | N bands | Spacing |
|---|---|---|
| Performance | 12 | ~33 nm |
| Research | 81 | 5 nm |

Range 380–780 nm. CIE 1931 2° observer via Wyman 2013 piecewise Gaussian fit.

### Scattering coefficients

$$\beta_R(\lambda) = \frac{8\pi^3 (n^2 - 1)^2}{3 N \lambda^4}$$

$$\beta_M(\lambda) \approx \beta_0 \left(\frac{550}{\lambda}\right)^{0.8}$$

Ozone Chappuis band: Gaussian fit centered 602 nm, peak cross-section ~5×10⁻²¹ cm²/molecule. Must convert cm² → m² (factor 10⁻⁴) before multiplying by m⁻³ number density.

### March architecture

Fused march: single ray march evaluates all wavelengths. Atmospheric density depends on altitude only, not wavelength.

| Stage | Count | Cost |
|---|---|---|
| View steps | 24 | ray-sphere + EXP() |
| Light sub-steps per view step | 8 | ray-sphere + EXP() |
| Wavelength MADs per view step | 12 | cheap |
| Total density evals | 24 × 8 = 192 | |
| Total wavelength ops | 12 × 24 = 288 MADs | |
| Wall time | ~0.3 ms | |

Wavelength loop is essentially free; density evaluations dominate.

### Luminance matching

Spectral output is scaled to match game LUT luminance per pixel:

```hlsl
float gameLum = dot(sky_in_scatter, float3(0.2126, 0.7152, 0.0722));
float specLum = dot(spectralSky, float3(0.2126, 0.7152, 0.0722));
float ratio = (specLum > 1e-6 && gameLum > 1e-6) ? gameLum / specLum : 1.0;
inScatterScale = ratio * SKY_IN_SCATTER_SCALE;
```

Apply `SKY_IN_SCATTER_SCALE` exactly once. Applying it both inside the ratio and as an explicit multiply squares the scale.

Empirical calibration factor ~3×10⁻¹⁴ brings physics units into game range, matched at midday zenith.

### Cloud composite

```hlsl
cloudColor.rgb += sky_in_scatter * SKY_IN_SCATTER_SCALE * 0.15 * SKY_OUT_SCATTER;
out.color = lerp(skyColor, cloudColor.rgb, cloudColor.a);
```

0.15 factor preserves game's cloud brightness tuning while picking up the spectral sky color.

### Blog

`https://www.prismshaders.com/blog/how-we-built-a-physically-accurate-spectral-sky-for-assetto-corsa-evo`

### Linear DEV-2 — antisolar pink tint

Three compounding issues at the antisolar horizon after sunset:

**1. Multi-scatter ozone path.** Multi-scatter radiance is added to single-scatter radiance before spectral-to-RGB conversion, passing through the view-ray ozone absorption chain. Multi-scattered light is isotropic — applying the view ray's ozone optical depth to it is not physical.

At antisolar horizon at sunset: single-scatter ≈ 0 (earth shadow), multi-scatter dominates, view ray nearly horizontal → enormous ozone path length → Chappuis band removes green/yellow → pink.

Fix: convert multi-scatter to RGB before applying view-ray ozone, or apply a zenith-only ozone path to the multi-scatter term.

**2. Refraction soft-floor altitude.** Atmospheric refraction soft-floor altitude constant is ~4× too high (~4000 m vs correct ~800–1000 m). Allows additional single-scatter light to leak in below the actual earth-shadow boundary.

**3. Azimuth symmetry.** Multi-scatter ambient sun term lacks azimuthal dependence. Solar hemisphere of sky should have more illuminated atmosphere visible; multi-scatter fill should be brighter on solar side and dimmer antisolar side.

```hlsl
float3 viewHoriz = normalize(viewDir - localUp * dot(viewDir, localUp));
float3 sunHoriz  = normalize(sunDir  - localUp * dot(sunDir,  localUp));
float azimuthWeight = 1.0 + 0.3 * dot(viewHoriz, sunHoriz);
ambientSun *= azimuthWeight;
```

Coefficient 0.3 approximate, tune against civil twilight references.

**Fix order:** Bug 1 first (largest contribution), then 2, then 3. One change at a time from known-good commit.

**Validation reference:** Salton Sea sunset, March 2026, observed in person. No antisolar pink at horizon; only solar horizon showed color. Belt of Venus should be elevated 10–25° above antisolar horizon with dark earth shadow below.

### Future work (behind feature flags)

- Spectral rainbow: Airy function, Cauchy dispersion, Descartes' law. Currently hardcoded subtle always-on; wire to game rain intensity.
- Glory and corona: backward/forward scatter colored rings.
- Polarization: Stokes vectors, Mueller matrix for Rayleigh.
- Multi-scattering LUT: Bruneton 2008 / Hillaire 2020 precomputation for twilight accuracy.
- Noctilucent clouds: 80+ km ice-crystal layer.

---

## 7.2 Prism — material shader define audit (March 2026)

Define mismatches between game shaders and Prism spectral overrides across four materials. Rule: clone 1:1, add spectral on top. Extract game defines from DXBC → set them in HLSL → spectral additions only on top. Spectral addition headers must be read-only inputs to all material shaders.

### UberInteriorMaterial (showroom, building interiors)

| Define | Game | Prism |
|---|---|---|
| Include | Material.hlsli | Vehicle.hlsli ← wrong |
| DIFFUSE_LAMBERT | yes | missing |
| MICROFIBER_BRDF | yes | missing |
| LIGHT_WRAP | yes | missing |
| ENVIRONMENT_DYNAMIC_SPECULAR_GI | 1 | missing |
| DISABLE_DECALS | no | YES ← wrong |
| VEHICLE_PROBE | no | YES ← wrong |

### UberMaterial / EnvironmentObject (concrete, barriers)

Game uses Material.hlsli; Prism used Vehicle.hlsli (wrong). Missing on Prism side: ANISOTROPY_BRDF, CLOTH_BRDF, MICROFIBER_BRDF, MULTIBOUNCE_AO, LIGHT_WRAP, HAS_CLEARCOAT, COCKPIT_PROBE, HERO_SHADOW, DISABLE_BREAK_LIGHTS_FROM_OPPONENTS.

### Fence (metal grates)

Game uses Material.hlsli. Missing: MICROFIBER_BRDF, LIGHT_WRAP, OPT_TRIPLANAR, ENVIRONMENT_DYNAMIC_SPECULAR_GI, LIGHT_WRAP_HEADLIGHTS, DISABLE_SSS, FORWARD_SHADOW_MAPPING. Extra: DISABLE_DECALS (game has no).

### UberVehicleInteriorMaterial (dashboard, gauges)

Vehicle.hlsli correct. Missing: DIFFUSE_DISNEY (used DIFFUSE_LAMBERT), MICROFIBER_BRDF.

### Probe semantics

COCKPIT_PROBE and VEHICLE_PROBE are not interchangeable. COCKPIT_PROBE has asymmetric blend alphas:

```
COCKPIT_RADIANCE_ALPHA   = 0.4f
COCKPIT_IRRADIANCE_ALPHA = 0.75f
```

The asymmetry is physically meaningful: more global irradiance penetrates a cabin than coherent specular reflection does. VEHICLE_PROBE without this blend will drop ambient grounding for interior materials.

### Pattern

MICROFIBER_BRDF missing on all four materials suggests a systematic gap in the original porting pass — likely extracted from an incomplete reference predating the microfiber sheen layer. Worth checking LIGHT_WRAP for the same pattern.

---

## 7.3 Prism — thin-film interference

Thin-film interference on car paint clearcoat must be a per-material flag, not a global shader addition.

### Symptom

Global thin-film produced chroma-flip on saturated colors (especially reds) at grazing angles on cars that should have solid single-stage paint (no interference pigments).

### Material DB schema

```
thin_film_enabled: bool
film_thickness_nm: float    // 200-500 for pearlescent, 0 for solid
```

Pearlescent and metallic paints have mica flakes or aluminum particles creating real thin-film layers — enable.

Solid single-stage colors have plain clearcoat with no interference structure — disable.

### Diagnostic protocol

Paint a test surface with flat spectral reflectance (constant 0.5 across all 81 bands, bypassing JSC entirely). If chroma flip persists at grazing angles, the cause is Fresnel/clearcoat model. If it disappears, the cause was JSC spectral error amplified by Fresnel geometry.

---

## 7.4 Photometric stereo with κ BRDF

Replace Lambert BRDF in photometric stereo with κ(θ) as the angular response.

### Coordinate

`r` = angular deviation. Commonly r = sin θ or r = θ directly. Transform from bare manifold's parameter t to θ is not written in closed form; fit parameters implicitly encode it.

### Single-tile fit (example)

With κ₀ free and four parameters:

| Parameter | Value |
|---|---|
| β | 19.71 |
| γ | 0.80 |
| λ | 13.18 |
| RMS | 0.2459 |

### MERL database benchmark

κ vs GGX on 100 MERL materials:

| Metric | κ (4 params fit) | GGX |
|---|---|---|
| Mean RMS | 0.3469 | 0.3922 |
| Win rate | 99.9% | — |

κ has four fitted parameters; GGX has one or two. Difference in parameter counts should be stated when reporting the comparison.

### Polarimetric separation

Lens-side CPL + light-side linear polarizer from the same manufacturer gives two captures per position:

- Parallel polarizers: specular + diffuse
- Crossed polarizers: diffuse only
- Difference: pure specular lobe

Test A (specular isolation): plot specular-only intensity vs θ, compare to κ(θ), GGX, and Fresnel. κ_base(θ) = 1/(1 + sin²θ) predicts grazing-angle floor of 0.5 — distinct from Lambert (→0) and Fresnel (→1).

Test B (diffuse): crossed-pol capture. Should follow Lambert for ideal diffuse. If κ fits instead, coupling is encoding subsurface transport rather than surface reflection.

### Capture pipeline (Photometric Studio)

288 frames per tile: 24 turntable positions × 2 illuminants (2 CCTs) × 3 HDR brackets × 2 polarization states.

Dual normal map output: flat surface normal for specular, PS-recovered subsurface normal for diffuse (conceptually equivalent to clearcoat PBR).

---

## 7.5 Ceramic mode (Photometric Studio)

Per-wavelength Saunderson correction at glaze/air interface, operating on spectral reflectance. Not κ; standard optical model. Listed here because it's the IP moat for Photometric Studio and integrates with JSC spectral output.

$$R_\text{ext}(\lambda) = k_1 + \frac{(1 - k_1)(1 - k_2) R_\text{int}(\lambda)}{1 - k_2 R_\text{int}(\lambda)}$$

k₁ = external Fresnel reflection at glaze/air interface (~0.04 for typical glaze IOR 1.5).
k₂ = internal Fresnel reflection for light trying to exit (~0.6).
R_int = per-wavelength internal reflectance from spectral scan.

Nonlinear in R_int. Cannot be computed in RGB and produce correct glazed-ceramic appearance — this is the technical basis for the "RGB export is incomplete; viewer is the delivery" business model.

Not available as turnkey mode in Arnold, V-Ray, Redshift, RenderMan, or Cycles (verified via search, 2026).

---

## 7.6 Chronon-GI — light transport

Canonical skill exists at `/mnt/skills/user/chronon-gi/SKILL.md`. This file does not duplicate it. Summary only.

### What κ replaces

Direct light + indirect bounces + shadows + caustics + SSS + volumetrics. One κ evaluation per complete path.

### Coordinate

`r` = optical distance = ∫ n(s) ds along the refracted geometric path. Meters.

### The one rule

κ(total_optical_path) — not κ(a) · κ(b). Chaining double-counts the exponential decay.

### Refraction vs optical distance

Refraction changes ray direction (Snell's law at interfaces). Optical distance changes coupling strength (κ evaluation). Both are needed; neither substitutes for the other. Trace the geometric path with refraction, accumulate optical length along that path, evaluate κ once on the total.

---

## 7.7 Shell-model Navier-Stokes

### Shell wavenumbers

$$k_n = k_0 \cdot \varphi^n$$

### Evolution

$$\frac{dE_n}{dt} = T_{n-1 \to n} - T_{n \to n+1} - 2\nu k_n^2 E_n + R_n(t)$$

### Resonance term

$$R_n(t) = r \sum_m c_{nm} E_m \cos(\omega_{nm} t), \quad \omega_{nm} = k_n - k_m$$

### Numerical observation

Under strong resonance with sufficiently low ν and high amplitude, enstrophy Ω = Σ_n k_n² E_n exhibits super-exponential growth Ω ~ exp(c·t²). BKM integral diverges. Energy E = Σ_n E_n remains bounded (viscous dissipation removes energy at high k; Ω grows because energy concentrates at high k).

### Observed scaling

Shell coupling c_nm with κ form. Resonance amplification factor 4× maximizes growth rate. Critical viscosity threshold ν < 10⁻⁴ for blowup in numerical runs. Amplitude A ≥ 15 and perturbation ε ≥ 0.5 accelerate.

### Relationship to Clay Millennium Prize

This is a shell-model result. Shell models (GOY, Sabra) are known to blow up; the specific κ-based shell coupling here produces blowup as well. Whether this shell model faithfully represents the full 3D PDE is the open question Clay asks.

---

## 7.8 CMB / gravitational wave overlays

### CMB angular power spectrum

Proposed test: map κ(k) to C(ℓ) via coordinate transform from ordinal k to multipole ℓ. Public data: Planck 2018 release. Coordinate transform not yet written in closed form; this is the single biggest observational-program gap.

### Gravitational wave analysis (GWTC-4.0)

182 events analyzed with Jenkursion transform on mass ratios.

| Quantity | Value |
|---|---|
| Events clustered near φ in mass ratio | 34/182 (18.7%) |
| Scale invariance preservation | 98.4% |
| Power-law fit α | 0.66 |
| Power-law R² | 0.929 |
| Highest-mass event of interest | M₁ = 137 M☉ (shell 137 candidate) |
| Closest-to-φ event | GW240109 at 0.08% from φ |

Null hypothesis in the original analysis was uniform over mass ratios; astrophysical prior is strongly non-uniform. Look-elsewhere corrections over shell candidates were not applied. Confirmation-grade claims require: realistic astrophysical prior, trials correction, held-out validation split.

---

## 7.9 BP-REX (Boundary-Programmed Reactive Exchange)

Power electronics efficiency via time-programmed parametric modulation of existing magnetic storage.

### Instantaneous boundary power

$$P_\partial = -\tfrac{1}{2} I^2 \frac{dL}{dt}$$

Programming dL/dt synchronized with I² such that cycle-averaged work is zero but timing of transfers improves → reduced overlap loss.

### Coordinate

`r` = time offset or phase offset within a switching cycle.

### Boundary actuators

| Actuator | Power range | Frequency |
|---|---|---|
| Auxiliary winding | 100 W – 1 kW | < 500 kHz |
| Varactor networks | — | > 500 kHz |
| Saturable inductor trim | high power | < 100 kHz |

### Control levers (all existing-hardware)

- Dead-time micro-scheduling (50–500 ns per cycle)
- SR window shaping (soft-gating synchronous rectifiers)
- Interleave phase offsets (VRM phase ± few degrees)
- Active clamp timing
- Resonant valley switching (LLC, phase-shifted full-bridge)
- Mode scheduling (continuous / discontinuous / burst)

### Lineage

Parametric amplification (Rugar & Grütter 1991), energy-recovery circuits (Kazimierczuk 2014), time-varying network theory (Mandelshtam 1972). Novelty is closed-loop energy-ledger feedback specifically for partial-load converter efficiency.

---

## 7.10 Unified κ-sim architecture

Real-time simulation combining rendering, audio, thermal, structural — all on one KPM mesh.

### Principle

The mesh IS the manifold. Every vertex carries material properties. Every edge is a κ junction. All transport — acoustic, thermal, spectral, structural — is one κ evaluation per edge per timestep.

No separate subsystems. No pipe cell arrays. No SDF geometry. No probe lattices independent of the mesh.

### SM 6.6 wave intrinsics mapping

| Intrinsic | Audio role |
|---|---|
| WaveActiveSum | CIE integration, collective pressure sums |
| WavePrefixSum | Delay lines |
| WaveBallot | Misfire detection |
| QuadSwap | Surface transport |

### Platform dispatch

```rust
#[cfg(target_os = "windows")]
const BACKENDS: Backends = Backends::DX12;

#[cfg(not(target_os = "windows"))]
const BACKENDS: Backends = Backends::VULKAN.union(Backends::METAL);
```

### wgpu 23 specifics

- `Instance::new` takes owned `InstanceDescriptor`, not `&ref`
- `window.inner_size()` for surface config; never hardcode WIDTH/HEIGHT
- `max_storage_buffer_binding_size` default is too small; set to ≥ 256 MB:

```rust
required_limits: wgpu::Limits {
    max_storage_buffer_binding_size: 256 * 1024 * 1024,
    ..Default::default()
}
```

### cpal audio

Do not hardcode `StreamConfig`. Use `device.default_output_config()`, compute downsample ratio from GPU rate to device rate, fill all channels via `chunks_mut(out_channels)`.

### Spec location

Design specs at `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`. Implementation plans generated separately via writing-plans skill after spec approval.

### KPM vertex

```rust
#[repr(C)]
struct KpmVertex {
    position: [f32; 3],       // mesh coords
    material: u32,            // index into material table
    kappa_params: [f32; 4],   // κ₀, β, γ, λ (per-vertex or per-material)
    shell_ord: f32,           // if applicable
    _pad: [f32; 3],
}
```

Edge coupling at each timestep reads κ_params from both endpoint vertices and evaluates κ on the edge length.
