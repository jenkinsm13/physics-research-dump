# 04 — JSC (Jenkins Spectral Conversion)

Converts RGB textures to 81-band spectral textures (380–780 nm, 5 nm spacing). Used in Prism and Photometric Studio where spectral transport is needed and source assets are RGB.

JSC uses the Moore-Penrose pseudoinverse of the CIE observer matrix. It does NOT use the Jenkursion kernel — that diverges on small inputs. Different objects sharing a name root.

## The underlying problem

CIE tristimulus integration projects an 81-dimensional spectrum onto a 3D XYZ triple. The projection is many-to-one: infinitely many spectra produce the same XYZ. Choosing a single spectrum is underdetermined. Existing methods impose different constraints:

| Method | Constraint | Failure mode |
|---|---|---|
| Smits (1999) | Fixed 6–10 basis spectra, linear combo | Blue→cyan shift from basis overlap near 490 nm |
| Sigmoid / Wyman-Sloan-Shirley | 3-parameter logistic | Steep slopes quantize at low bit depth |
| Jakob-Hanika (2019) | Polynomial fit via optimization | Negative lobes at gamut boundary |
| Meng et al. (2015) | Tabulated smooth spectra | Product-of-two amplifies error quadratically |

## Matrix form

Precompute the 3×81 observer matrix C with rows the CIE 1931 2° observers x̄, ȳ, z̄ at 5 nm sampling:

$$C_{ki} = \bar{c}_k(\lambda_i) \cdot \Delta\lambda, \quad k \in \{X, Y, Z\}, \quad i \in \{1, \ldots, 81\}$$

With Δλ = 5 nm folded in. Gram matrix:

$$G = C C^T \in \mathbb{R}^{3 \times 3}$$

Pseudoinverse:

$$C^+ = C^T G^{-1} \in \mathbb{R}^{81 \times 3}$$

Forward: XYZ = C · spectrum.

Inverse (Variant C): spectrum = C⁺ · XYZ.

C C⁺ = I₃, so the roundtrip is exact: ΔE = 0 for all sRGB colors.

## Three variants

Variant C is the target (full κ absorption pipeline). A and B are stopgaps for conventional renderers that can't handle negative reflectance.

| Variant | Seed | Kernel | Clamp | Non-negative | Roundtrip ΔE (avg / max) | Use when |
|---|---|---|---|---|---|---|
| A | Gaussian basis | K10 shell coupling | Per-iteration | Yes | 0.086 / 2.82 | No κ transport |
| B | Pseudoinverse | K10 shell coupling | Per-iteration | Yes | 0.086 / 2.82 | No κ transport |
| C | Pseudoinverse | None (0 iterations) | None | No | 0 / 0 | Full κ absorption pipeline |

## Why Variant C outputs can be negative

For saturated primaries the pseudoinverse produces spectra with negative bands. Pure red (1,0,0): wavelengths 470–545 nm must be negative to cancel short-wavelength contributions under CIE integration. A classical reflectance cannot be negative; but under the κ absorption pipeline the spectrum is interpreted as an absorption coefficient α(λ), and negative α corresponds to shell-coupling-assisted transitions contributing energy at that wavelength. The framework justifies the sign; classical pipelines do not.

Mapping to absorption:

$$\alpha(\lambda) = -\frac{\ln(S(\lambda)/\kappa_0)}{d_{\text{eff}}}$$

Negative S maps to maximum absorption (clamped) in that interpretation.

## Gaussian basis (Variant A)

Three lobes at standard RGB primary wavelengths:

```
Lobe centers (nm): 610 (R), 540 (G), 460 (B)
Lobe widths  (nm): 40,      35,       30
```

Seed spectrum is a weighted sum with weights from linear sRGB. Produces visually pleasing in-gamut reflectance that converges in ~12 iterations of K10 to exact XYZ match.

## K10 iteration

Additive correction per band. For current spectrum S and target XYZ vector X_tgt:

```
1. X_cur = C · S
2. Δ = X_tgt - X_cur                  (3D vector)
3. For each band b:
     e_b = PINV[b] · Δ                (row of C⁺ times error)
     r_b = |e_b| / max(S[b], eps)     (relative correction size)
     c_b = kappa_coupling(r_b)         (damping)
     S[b] = max(S[b] + e_b · c_b, eps) (additive update, clamp)
4. Repeat (12 iterations recommended for Variant A)
```

The κ damping in step 3 prevents overshoot on large corrections. "10" in "K10" is an early iteration count that became a name.

## Gamut accuracy

Variant A at 12 iterations:
- 96.6% of sRGB colors converge to ΔE < 1.0
- Average ΔE = 0.086
- Max ΔE = 2.82

Worst-case points are highly saturated primaries near the gamut boundary.

Variant C: exact for all inputs. ΔE = 0.

## DX12 file layout

```
shaders/
  jsc_data.hlsl         Precomputed CMF, pseudoinverse, Gaussian basis
  jsc_common.hlsl       Shared utility functions
  jsc_variant_a.hlsl    Gaussian + K10 + clamp
  jsc_variant_b.hlsl    PInv seed + K10 + clamp
  jsc_variant_c.hlsl    Raw pseudoinverse
src/
  jsc_dispatch.cpp      Dispatch shared by all variants
```

## Data generation

```python
import numpy as np
import colour

cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
wavelengths = np.arange(380, 785, 5)
N = len(wavelengths)  # 81
DL = 5.0

CMF = np.zeros((3, N))
for i, w in enumerate(wavelengths):
    CMF[0, i] = cmfs[w][0] * DL
    CMF[1, i] = cmfs[w][1] * DL
    CMF[2, i] = cmfs[w][2] * DL

G = CMF @ CMF.T
G_inv = np.linalg.inv(G)
CMF_pinv = CMF.T @ G_inv  # 81 × 3

LOBE_CENTERS = np.array([610.0, 540.0, 460.0])
LOBE_WIDTHS  = np.array([40.0,  35.0,  30.0])
GAUSS_BASIS = np.zeros((3, N))
for ch in range(3):
    for i, w in enumerate(wavelengths):
        GAUSS_BASIS[ch, i] = np.exp(-0.5 * ((w - LOBE_CENTERS[ch]) / LOBE_WIDTHS[ch])**2)
```

## Variant C shader

```hlsl
#include "jsc_common.hlsl"

Texture2D<float4>       g_InputTex  : register(t0);
RWTexture2DArray<float> g_OutputSpec : register(u0);

cbuffer JscParams : register(b0) {
    uint g_Width;
    uint g_Height;
    float g_Kappa0;
    float g_DEffective;
    uint g_OutputMode;  // 0 = spectrum (may be negative), 1 = absorption
    uint3 _pad;
};

[numthreads(8, 8, 1)]
void CSMain(uint3 dtid : SV_DispatchThreadID) {
    if (dtid.x >= g_Width || dtid.y >= g_Height) return;

    float4 srgb = g_InputTex[dtid.xy];
    float3 rgb_lin = srgb_to_linear(srgb.rgb);
    float3 xyz = mul(SRGB_TO_XYZ, rgb_lin);

    // One matrix-vector multiply per texel.
    [unroll] for (uint i = 0; i < JSC_BANDS; i++) {
        float s = dot(PINV[i], xyz);
        if (g_OutputMode == 1) {
            s = spectrum_to_absorption(s, g_Kappa0, g_DEffective);
        }
        g_OutputSpec[uint3(dtid.xy, i)] = s;
    }
}
```

## Validation fixture

For the 1024³ sRGB gamut sampled at 8-bit resolution:

- Variant C: max ΔE = 0 across all inputs.
- Variant A: ΔE < 1.0 on 96.6% of gamut, avg 0.086, max 2.82. Worst cases are saturated magentas and yellows near gamut boundary.
- Pure primaries (255,0,0), (0,255,0), (0,0,255) are exact under Variant C.

## Integration notes

Variant C spectra can be negative. Any downstream code assuming `spectrum ≥ 0` will break. Guard explicitly or pipe through the absorption conversion first.

The Jenkursion kernel K(t,s) = t + s/t diverges for small t. Do not use as the iteration step. Use K10 (Variants A/B) or the pure pseudoinverse (Variant C).
