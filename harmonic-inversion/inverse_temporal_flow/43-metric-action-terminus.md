# 43 — The Gravity Terminus: No Metric Action to Vary

*Note 42 sharpened the gravity gap into a target — couple the COTV profile-deformation into an
$rr$ field equation so $g_{rr}$ responds to mass with $\gamma=1$ (the factor-2). This note takes
the fork the target poses: the only honest positive is **deriving** that field equation from note
16's Lagrangian; a static source map $a(\Phi)$ tuned to $1+2\Phi$ is the forbidden "hand-insert
$g_{rr}$." The gate fails — and for a clean structural reason that **terminates the gravity sector**
exactly as note 39 terminated color. Verified in `verify/verify_metric-action.py` (4/4, exit 0).*

---

## The fork, and the gate

Note 42 located the gap precisely: the framework propagates mass as a *scalar center-shift*
(Object 1, $\gamma=0$, the half), while the *profile deformation* (Object 2) — which the
shape-sensitive $\kappa_{\rm Frenet}$ can carry — is not in the gravity channel. The factor-2 needs
that profile coupled in via an $rr$ field equation $G_{rr}=8\pi T_{rr}$. Two ways forward:

(a) **derive** the $rr$ field equation from note 16's action; or
(b) **terminate** the sector with the missing object named.

The gate, pre-registered before computing: *name the relation in note 16 that forces $g_{rr}$'s
$\Phi$-coefficient to be exactly 2 ($\gamma=1$).* If a coupling must be **chosen** to land on 2,
$\gamma$ is a knob → the half → the negative. And the verdict is read from the **deflection
integrator** (note 40), never a curvature proxy. (One trap closed first: the "saddle $y=xz$" that
seemed a fresh lever *is* the amplitude $a$ — $y=a\cdot\tfrac12\sin2t=a\cdot xz$ — i.e. the same
shape knob that already saturated. Renaming it does not make it a new object; third instance of the
worldline→matrix→saddle "is it different?" move, provably the same.)

## The structural failure: there is no $g_{rr}$ in the action

Note 16's action is
$$S[\boldsymbol\Psi]=\int dk\;\Big[\tfrac12\langle D_k\boldsymbol\Psi,D_k\boldsymbol\Psi\rangle_\eta-\tfrac12\,\osc^2(k)\,\langle\boldsymbol\Psi,\boldsymbol\Psi\rangle_\eta\Big],\qquad D_k=\partial_k-\tfrac1\varphi K.$$

Inventory what it can be varied against:
- **one coordinate** — the ordinal $k$;
- a **2-component** flow-space field $\boldsymbol\Psi$;
- $\eta=\mathrm{diag}(+1,-1)$ — the **internal** flow-space metric (time-ray vs gravity-ray), *fixed*, $2\times2$.

There is **no $g_{rr}(r)$** in $S$: no radial coordinate, no spacetime metric tensor. So
$\delta S/\delta g_{rr}$ is **undefined**. The Euler–Lagrange variation $\delta S/\delta\boldsymbol\Psi$
gives the field equation $(D_k^2+\osc^2)\boldsymbol\Psi=0$ — a *matter* equation on a *fixed
background*. The object $G_{rr}=8\pi T_{rr}$ requires a **metric action** $S[g_{\mu\nu}]$ that note
16 simply does not have.

## The rank/dimension deficit

| | action | field | rank | dim | varies to |
|---|---|---|---|---|---|
| **GR** | $S[g_{\mu\nu}]=\int\sqrt{-g}\,R$ | $g_{\mu\nu}$ | 2 | 4D | $G_{\mu\nu}=8\pi T_{\mu\nu}$ |
| **note 16** | $S[\boldsymbol\Psi]$ | $\boldsymbol\Psi$ | 1 | 1D | $(D_k^2+\osc^2)\boldsymbol\Psi=0$ (scalar) |

To produce $G_{rr}$ one must **promote** the fixed background to a dynamical rank-2 $g_{\mu\nu}$ over
a spacetime with a radial coordinate. That is *adding GR*, not deriving it from note 16. The deficit
is structural — a difference of rank (1 vs 2) and dimension (1D vs 4D) — not a missing term that
could be supplied by a cleverer source coupling.

## The non-foolable read, and why the "2" is out of reach

Feeding $g_{rr}=1+2\gamma\Phi$ into note 40's null-geodesic deflection integrator (not a curvature
proxy):
$$\gamma=1:\ 1.7515''\ (\text{GR}),\qquad \gamma=0:\ 0.8758''\ (\text{framework, the half}).$$
The framework supplies $\gamma=0$. And the coefficient $2$ that defines $\gamma=1$ is a **rank-2
fact**: it is the trace-reversal $G_{\mu\nu}=R_{\mu\nu}-\tfrac12 g_{\mu\nu}R$, Bianchi-protected
($\nabla_\mu G^{\mu\nu}=0$), that makes $g_{rr}$'s mass-response *equal* $g_{tt}$'s. A scalar field
equation, a COTV map $a(\Phi)$, or any shape knob has no rank-2 / trace-reversal structure — so even
a *derived* $a(\Phi)$ could not fix the coefficient to 2; it would be a free knob. The "2" lives in
the tensor structure the framework lacks.

## Verdict — gravity terminates, object named

$$\boxed{\;\text{Note 16 has no metric action to vary; the }rr\text{ field equation cannot be derived
from it. The missing object is a rank-2 dynamical metric action }S[g_{\mu\nu}]\text{ — which is GR.}\;}$$

The framework is, structurally and provably, a **$\gamma=0$ scalar-time theory**: it reproduces
gravitational time dilation ($g_{tt}$) and bends light by exactly half the GR value, and it **cannot
be made into a tensor theory of spacetime** without adding GR's metric action as new input. Note
42's target is unreachable from within the framework — supplying the $rr$ field equation means
adding $S[g_{\mu\nu}]$ by hand.

This is the gravity sector's terminus, identical in shape to color's (note 39): a clean, *located*
negative with the missing object specified exactly. The thread does not loop further — the next
question about gravity would be "adopt GR's metric action as an external input and ask how the
framework's $V_{\rm grav}$ sits inside it," which is a different (and much larger) program, not a
refinement of this one.

## What stands

The honest gravity ledger across notes 35–43:
- **Derived / correct:** time = gravity as one boost generator (35); gravitational time dilation,
  weak-field EP (35b); the static potential and its golden exponent (03/13); $\gamma=0$.
- **Located negatives, all proven:** not a tensor theory — half-deflection, no $G_{\mu\nu}$ (40);
  the shell matrix is source-free / at most 2+1D holographic (41); COTV is the mass and its profile
  is the right lever but only the scalar center-shift propagates (42); and **no metric action exists
  to vary into the $rr$ field equation (43)** — the structural reason the factor-2 is unreachable.

Gravity in this framework is a scalar theory of time, exact where it is scalar, and terminated —
honestly and precisely — where spacetime would have to become a rank-2 dynamical field.
