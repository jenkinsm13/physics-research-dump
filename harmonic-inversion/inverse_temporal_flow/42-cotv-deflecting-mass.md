# 42 — COTV Is the Deflecting Mass: Center-Shift (Scalar) vs Profile (the Right Lever)

*Two questions raised by notes 40/41: (a) is the Call-of-the-Void (COTV) potential the
"deflecting mass" the GR test kept asking about? (b) Since COTV is a per-shell *potential*,
isn't it more than "one number per shell" — and could that extra structure supply the $g_{rr}$
the scalar worldline missed? **Both instincts are right, and they sharpen the negative into a
specific target.** COTV *is* the mass; the earlier "scalar" framing conflated two distinct COTV
objects; the per-shell radial profile is exactly the structure $g_{rr}$ needs — but the corpus
only propagates the scalar part, and Birkhoff still demands a field equation. Verified in
`verify/verify_cotv-tensor.py` (4/4, exit 0).*

---

## Yes — COTV is the deflecting mass

The corpus is explicit (metamer note 06): COTV's attractive Gaussian "shows up macroscopically
as gravitational mass," and the mass$\to$geometry step carries the Newtonian shape,
$$\Delta r_i(x) = -\frac{Gm}{c^2}\cdot\frac{1}{|x-x_m|}\cdot e^{-\lambda|i-i_m|}.$$
That $1/|x-x_m|$ is the Newtonian potential, reproducing the $g_{tt}$ (time-dilation) sector
exactly. So COTV is precisely the channel notes 40/41 tested — the question is whether it carries
*more* than a scalar.

## Two COTV objects — the conflation, corrected

Notes 40/41 said "$\Delta r_i$ is one number per shell, a scalar." That is incomplete. There are
**two** distinct COTV objects:

- **Object 1 — the distortion a distant mass *causes*:** $\Delta r_i(x)$ above. One number per
  shell — a scalar field, a *center shift* of shell radii. This is what notes 40/41 tested.
- **Object 2 — the COTV potential that *defines* the particle:**
  $$W(r) = -V_1\,e^{-(r-R_1)^2/2\sigma_1^2} + V_2\,e^{-(r-R_2)^2/2\sigma_2^2},$$
  a full **radial profile**, six degrees of freedom per shell. **Not** a scalar.

Per shell, COTV is *not* one number — it is a radial profile. The correction is right, and it
matters.

## Why it matters: $g_{rr}$ is radial structure, and a profile can carry it

$g_{rr}$ governs proper radial length $\sqrt{g_{rr}}\,dr$ — it *is* radial structure. A scalar
(Object 1) cannot encode it; a radial profile (Object 2) can. The decisive test, on the corpus
spatial metric $\kappa_{\rm Frenet}$ (note 02):

| operation | effect on $\kappa_{\rm Frenet}$ | meaning |
|---|---|---|
| **center shift / radial scale** (Object 1) | **invariant** ($1.186$ at every scale) | scalar $\to$ no $g_{rr}$ response $\to\gamma=0$ (the half) |
| **profile / shape deformation** (Object 2) | **changes** ($1.134\to1.186\to1.219$, spread $0.085$) | radial profile $\to$ *can* source $g_{rr}$ |

$\kappa_{\rm Frenet}=\sqrt{5-3u}/(1+u)^{3/2}$ ($u=\cos^2 2t$) is manifestly **scale-free**, so a
center shift does nothing — *that is exactly why notes 40/41 got $\gamma=0$*. But deforming the
*shape* moves the curvature. **The factor-2 is reachable in principle** — through Object 2, not
Object 1.

## Why we still measured $\gamma=0$ — now precisely located

The corpus mass$\to$distortion formula propagates **only Object 1**: $\Delta r_i$ is a single
scalar field; it shifts shell radii but does *not* carry the profile parameters
$(V_1,R_1,\sigma_1,V_2,R_2,\sigma_2)$. So the gravity-propagation channel sees the 1-dof scalar,
not the 6-dof profile. The profile *defines the particle's mass* (the COTV Schrödinger eigenvalue)
but is **not coupled into gravity propagation**. That is the exact, now-located reason for the
half-deflection — not a generic "the framework is scalar," but a specific missing coupling.

## The Birkhoff guardrail — necessary, not sufficient

Honesty check: even *with* the profile coupled in, the **exterior** metric of a static spherical
source depends only on total mass $M$ (Birkhoff's theorem); the exterior $\gamma=1$ comes from the
$rr$ **field equation** $G_{rr}=8\pi T_{rr}$, not from the source profile alone. The mass integral
$m\propto\int(V_1\sigma_1^3-V_2\sigma_2^3)$ collapses the 6 dof to one number for the exterior. So
Object 2 is the **channel** through which the framework *could* carry $g_{rr}$ — but a field
equation (note 40's specified missing rung) is still required. The profile is **necessary, not
sufficient**.

## Verdict — a constructive sharpening, not an escape

$$\boxed{\;\text{COTV is the deflecting mass. Its per-shell radial PROFILE is the right lever for
}g_{rr}\text{ — but the corpus propagates only its scalar center-shift, and the factor-2 needs an
}rr\text{ field equation coupling the profile in.}\;}$$

This turns notes 40/41's flat negative into a **specific, testable target**:

- **What works:** COTV generates mass (Schrödinger eigenvalues, the framework's real
  mass-mechanism) and deflects via the Newtonian $g_{tt}$ sector.
- **What's missing, now precise:** couple the COTV *profile deformation* (shape/width response to
  a source), not just its *center shift*, into the metric via an $rr$ field equation. The geometry
  *can* carry it ($\kappa_{\rm Frenet}$ is shape-sensitive); the coupling is the open work.

The earlier "scalar, can't get the factor-2" was correct for the *propagated* object but missed
that the *generating* object is a profile — so the gap is not "the framework can only ever be
scalar" but "the profile's radial DOF are not yet in the gravity channel." That is a much more
tractable problem.

## Falsifier / the one constructive path

Derive a coupling in which a source's mass deforms the COTV *profile* of neighboring shells
(changing $\sigma$ or the $V_1/V_2$ balance, not just $R$), and feed that into an $rr$ field
equation that produces $g_{rr}=1/(1-2\Phi)$ from the *same* $m$. If the resulting deflection is the
factor-2 ($\gamma\to1$), the framework reaches GR through COTV; if the profile response cannot be
built from framework objects without hand-inserting $g_{rr}$, the scalar standing of notes 40/41
holds and the tensor gap is irreducible. Either way the question is now sharp.
