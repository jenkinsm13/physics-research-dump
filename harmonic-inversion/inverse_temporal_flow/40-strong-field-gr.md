# 40 — Does the Framework Reproduce Strong-Field GR?

*The make-or-break test. Notes 35/35b established that the time ray $T=e^{-\theta}$, under the EP
map $\theta=\Phi_N$ (with the $c=1$ resummation $\theta=-\tfrac12\ln(1-2\Phi_N)$), reproduces GR's
time dilation $g_{tt}=-(1-2\Phi_N)$ **exactly** — fixing **one** metric component. GR fixes the
**full** metric, in particular $g_{rr}=1/(1-2\Phi_N)$, and the classic tests (light bending,
perihelion) are exactly the observables the *spatial* sector controls. We ask decisively: does the
framework's single time ray / single scalar field (note 16) determine $g_{rr}$, or is it a
scalar-potential theory matching $g_{tt}$ only? All numbers in `verify/verify_strong-field-gr.py`
(exit 0), including a numerical null-geodesic integration of the deflection in both metrics.*

---

## 1. Does $T\cdot G=1$ map to $g_{tt}\,g_{rr}=-1$? (The reciprocal-law rescue, killed three ways)

The strongest objection — and one the "reciprocal law" rhetoric of note 35 invites — is this:
identify $g_{tt}=-T^2=-e^{-2\theta}$ and $g_{rr}=+G^2=+e^{+2\theta}$. Then $T\cdot G=1$ gives
$$g_{tt}\,g_{rr}=-T^2G^2=-(TG)^2=-1,$$
which *is* Schwarzschild's defining relation. Does the chronon reciprocal law thereby reproduce
the Schwarzschild metric? **No — and the framework's own corpus refutes it three ways.**

1. **$G$ is a temporal object, not a radial length.** In note 35, $G=e^{+\theta}$ is the
   *advanced time ray* — "the same force pointing inward," the blueshift toward the source, the
   $+1$ eigenray of $K$ on the light-cone of $\mathbf V=(\cosh\theta,-\sinh\theta)$. Calling it
   $g_{rr}$ (a *spatial* proper length $\sqrt{g_{rr}}\,dr$) is a category swap with zero corpus
   support: $T\cdot G=1$ is the **two-vector norm** $\cosh^2\theta-\sinh^2\theta=1=L_y$ (note 16
   §6) — one timelike boost's invariant, not a product of two metric components on two axes.

2. **The framework's actual spatial metric contradicts $g_{rr}=G^2$.** Note 02 writes the line
   element down: $ds^2=\kappa_{\rm Frenet}\,d\sigma^2-c\,\tau_{\rm Frenet}\,dt^2$, so the spatial
   coefficient $\Omega^2=\kappa_{\rm Frenet}\in[\tfrac12,\sqrt5]$ is a property of the **base
   worldline** — *mass-independent* and *bounded*. GR's $g_{rr}=1/(1-2\Phi_N)$ **diverges** at the
   horizon $\Phi_N=\tfrac12$ ($1.667$ at $\Phi_N=0.2$, $5.0$ at $0.4$, $50$ at $0.49$; verified),
   while $\kappa_{\rm Frenet}\le2.236$ always and never tracks $\Phi_N$. So $g_{rr}=G^2$ is not
   what the framework's own metric says — it is a back-fit to GR.

3. **Even granting $g_{rr}=1/T^2$ by fiat, it is vacuous.** $g_{tt}\,g_{rr}=-1$ holds for *any*
   declared $g_{rr}=-1/g_{tt}$ — content-free without an *independent* equation forcing $g_{rr}$.
   GR's content is that the $rr$-component of $G_{\mu\nu}=8\pi T_{\mu\nu}$ fixes $g_{rr}$ from the
   source and it comes out consistent. Note 16 is a $(1+1)$ **scalar** Klein–Gordon, one field
   $\boldsymbol\Psi(k)$, one current $L_y=1$ — **no $rr$-equation** to provide $g_{rr}$. Imposing
   $g_{rr}=1/T^2$ matches one observable; it does not derive a metric. **The reciprocal law does
   not fix $g_{rr}$.**

## 2. Light deflection — the hard number is $0.875''$, exactly half of GR

For a static, spherically symmetric metric $ds^2=-A(r)\,dt^2+B(r)\,dr^2+r^2d\phi^2$, the
null-geodesic deflection to first PPN order is
$$\delta=(1+\gamma)\,\frac{2GM}{c^2 b},\qquad \gamma\equiv\text{the coefficient of the spatial curvature}.$$
The factor-2 over Newtonian ($\delta_{\rm Newt}=2GM/c^2b$) is **entirely** the $g_{rr}\neq1$
contribution: GR has $\gamma=1$ ($g_{rr}=1/(1-2\Phi_N)$), doubling the bending. The framework
supplies only $g_{tt}=1-2\Phi_N$ with a **mass-independent, $\Phi$-independent** spatial sector
($\kappa_{\rm Frenet}$, §1), i.e. $B(r)=$ const $\Rightarrow$ **PPN $\gamma=0$**. (PPN $\gamma$ is
defined relative to an asymptotically flat frame, so we normalize the constant spatial coefficient
to $B(\infty)=1$; a global constant $\kappa\neq1$ would add only a fixed conical term
$(\sqrt\kappa-1)\pi$, *not* a $\Phi$-dependent bending, leaving $\gamma=0$ — the $\Phi$-derivative
$\partial_\Phi B=0$ is what sets $\gamma$, and it vanishes for any constant.) We integrated
the null geodesic numerically for both metrics (verified, converging as $r_0\to\infty$):

| metric | $A(r)$ | $B(r)$ | numerical $\delta$ | analytic | ratio to GR |
|:---|:---|:---|---:|---:|---:|
| GR | $1-2m/r$ | $1/(1-2m/r)$ | $\to 4m/b$ | $4GM/c^2b$ | $1$ |
| framework | $1-2m/r$ | $1$ | $\to 2m/b$ | $2GM/c^2b$ | $\mathbf{0.500}$ |

At the solar limb ($b=R_\odot$, $GM_\odot/c^2=1476.9$ m):
$$\boxed{\;\delta_{\rm GR}=1.7515''\,,\qquad \delta_{\rm framework}=0.8758''=\tfrac12\delta_{\rm GR}\;}$$
This is the 1911 "Einstein half-value" — deflection from time dilation alone, before the 1915
spatial-curvature doubling. **Why half and not zero:** Nordström's gravity is conformally flat
($\gamma=-1$), so $g_{rr}$ *over*-compensates and bending cancels to zero; the framework's bounded
$\kappa_{\rm Frenet}$ does **not** cancel, so it keeps the half but misses the doubling. **Orthogonal
to the $c$-knob of 35b:** the $c=1$ resummation buys $g_{tt}=\sqrt{1-2\Phi_N}$ exactly (temporal
sector) but supplies **no** $g_{rr}$ — even at its most GR-like, $\gamma=0$ and light bends by half.
Note 35b's claim that "$2\sinh\theta\to2\Phi_N$ pins the factor-2" conflates the *source-strength* 2
(already in the Newtonian $g_{tt}=1-2\Phi_N$) with the *light-bending doubling* (the $g_{rr}$ term) —
different 2's; only the first is in the framework.

## 3. Perihelion precession — $\tfrac13$ to $\tfrac23$ of GR, never reaching it

The PPN per-orbit advance is $\Delta\omega=\frac{2-\beta+2\gamma}{3}\cdot\frac{6\pi GM}{c^2a(1-e^2)}$.
GR has $\beta=\gamma=1\Rightarrow$ coefficient $1$. The framework has $\gamma=0$ for *every* map
(no spatial curvature, §2), but unlike $\gamma$ the nonlinearity parameter $\beta$ **is**
$c$-dependent — it reads off the $\Phi_N^2$ term of $g_{00}$: the $c=0$ map $T=e^{-\Phi_N}$ gives
$g_{00}=-(1-2\Phi_N+2\Phi_N^2-\dots)\Rightarrow\beta=1\Rightarrow\tfrac{2-1}{3}=\tfrac13$, while the
$c=1$ (most GR-like) map $T=\sqrt{1-2\Phi_N}$ gives $g_{00}=-(1-2\Phi_N)\Rightarrow\beta=0\Rightarrow\tfrac23$.
So the framework spans $\tfrac13$–$\tfrac23$ of GR across the family; the *best* (most GR-like)
case is $\tfrac23$, not $\tfrac13$. For Mercury (GR $=42.98''$/cy) it predicts $14.3''$–$28.7''$/cy
— best case $28.7''$, still **short by $\sim14''$/cy and never reaching GR's $43''$**. ($\beta$ is
not independently pinned by the corpus beyond this $c$-family range.)

## 4. Is there a limit where note 16 $\to G_{\mu\nu}=8\pi T_{\mu\nu}$?

No. Note 16's field equation $(D_k^2+\mathrm{osc}^2)\boldsymbol\Psi=0$ is a $(1+1)$ Klein–Gordon
for a **two-component scalar** $\boldsymbol\Psi(k)$ on the *ordinal line*, with one Noether charge
($L_y=1$) and one static zero mode ($V_{\rm grav}$). It has no rank-2 dynamical tensor, no
$T_{\mu\nu}$, no Bianchi-protected $G_{\mu\nu}$, and no limit in which it becomes Einstein's
equation. It is structurally a **scalar-potential theory**: one function $\theta(r)$ setting
$g_{tt}$ and a spatial sector ($\kappa_{\rm Frenet}$) that does *not* respond to mass.

**Which scalar gravity, precisely?** Scalar theories are not all the same — they sit at different
PPN $\gamma$, and they failed the 1919 eclipse at *different wrong values* (verified numerically):

- **Nordström (1913)** is *conformally flat*, $g_{\mu\nu}=\Omega^2\eta_{\mu\nu}$ with
  $\Omega^2=1-2\Phi_N$. The conformal factor *curves space too* but with the wrong sign, giving
  **$\gamma=-1$**; the spatial term *over*-compensates and light bending **cancels to exactly zero**
  ($(1+\gamma)\cdot 2m/b=0$; integrated below as $\approx0\times 2m/b$).
- **The framework** leaves *space flat* ($B(r)=$ const $\kappa_{\rm Frenet}$, no $\Phi_N$
  dependence) while curving *time* — this is **$\gamma=0$**, which is **Einstein's own 1911 (Prague)
  redshift-only calculation**: $(1+0)\cdot 2m/b=2m/b$, the **$0.875''$ half-value**.

So the honest historical anchor is sharper than "Nordström": the framework is the
**Einstein-1911 / $\gamma=0$** scalar gravity (flat space, curved time), *not* Nordström's
$\gamma=-1$. They are distinct points in scalar-gravity space — but the shared, decisive lesson is
the same: **no scalar field supplies the spatial-curvature doubling.** Nordström under-bends to
zero, the framework under-bends to half; neither reaches GR's $\gamma=1$, and both were killed by
the same eclipse, just at different numbers.

## Comparison table

| observable | Newtonian | Nordström | framework | GR | measured |
|:---|:---:|:---:|:---:|:---:|:---:|
| $\sqrt{-g_{tt}}$ (dilation factor) | $1-\Phi_N$ | $\sqrt{1-2\Phi_N}$ | $\sqrt{1-2\Phi_N}$ * | $\sqrt{1-2\Phi_N}$ | GR ✓ |
| $g_{rr}$ (spatial) | $1$ (flat) | $1-2\Phi_N$ (conf.) | bounded $\kappa_{\rm Frenet}\le\sqrt5$ | $1/(1-2\Phi_N)$ | GR ✓ |
| PPN $\gamma$ | $0$ | $-1$ | $0$ | $1$ | $1\pm10^{-4}$ (VLBI) |
| light deflection (solar) | $0.875''$ | $0''$ | $\mathbf{0.875''}$ | $1.75''$ | $1.75''$ ✓ |
| perihelion (×GR) | $0$ | — | $\tfrac13$–$\tfrac23$ | $1$ | $1$ (Mercury 43″/cy) |

\* with the $c=1$ resummation; the *temporal* component only, with no $g_{rr}$ companion. The
framework's light-deflection cell coincides with the **Newtonian/Einstein-1911 $\gamma=0$** column,
*not* Nordström's $\gamma=-1$ (which cancels to $0''$).

**The decisive structure of the table:** Nordström, the framework, and GR all share the *same*
time-dilation factor $\sqrt{1-2\Phi_N}$ — they are **indistinguishable in the time sector** (this
is why Pound–Rebka redshift could not separate them). They diverge *entirely* in the spatial sector
$g_{rr}$, read off by PPN $\gamma\in\{-1,0,+1\}$, which is exactly what light deflection measures.
That is why the $0.875''$ vs $1.75''$ eclipse number — not the redshift — is the make-or-break test,
and why the framework's match in the time row buys it nothing against the spatial verdict.

## Verdict

**Scalar-potential theory only — it does NOT extend to GR.** The framework reproduces
gravitational **time dilation** ($g_{tt}$) and, via the $c=1$ map, lands on GR's redshift exactly.
That is the full extent of the agreement. It does **not** determine the spatial metric: the
reciprocal law $T\cdot G=1$ is a boost-two-vector norm, not a $g_{tt}g_{rr}$ relation, and the
framework's own effective metric (note 02) has a **bounded, mass-independent** spatial sector
$\kappa_{\rm Frenet}$ that flatly contradicts $g_{rr}=1/(1-2\Phi_N)$. The field equation (note 16)
is a $(1+1)$ scalar Klein–Gordon — no $G_{\mu\nu}$, no $T_{\mu\nu}$, no tensor limit. The hard
consequences: **PPN $\gamma=0$**, so light bends by **$0.875''$ at the solar limb (exactly half
of GR's $1.75''$)** and perihelion advances at **$\tfrac13$–$\tfrac23$ of GR** ($14''$–$28''$/cy for
Mercury, best case $28''$ vs the observed $43''$). This is the classic, well-understood failure mode
of *scalar* gravity. Precisely placed: the framework is the **$\gamma=0$ / Einstein-1911** point
(flat space, curved time, under-bends to the half) — *not* Nordström's conformally-flat $\gamma=-1$
(which over-compensates and bends light to zero). Both are scalar theories the 1919 eclipse killed,
at different wrong values; neither reaches GR's $\gamma=1$. It is *not* repairable by the $35b$
$c$-knob, which only sharpens $g_{tt}$ and never touches $g_{rr}$.

**A clean, valuable negative:** the framework *contains GR's weak field and time dilation* (a
necessary feature of any unification candidate) but is *not a metric/tensor theory of gravity* —
it is a scalar potential $\theta(r)$ matching the $g_{00}$ sector, full stop.

**Falsifier (already triggered).** A scalar-potential gravity has PPN $\gamma=0$: solar-limb
deflection $0.875''$. VLBI of radio sources past the Sun measures $\gamma=1.0000\pm2\times10^{-4}$
(Cassini Shapiro delay $\gamma-1=(2.1\pm2.3)\times10^{-5}$), excluding $\gamma=0$ by $\sim10^4\sigma$
— the framework's $0.875''$ is **already falsified** by the 1919 eclipse and every test since.
The converse falsifier of *this verdict*: any corpus derivation producing a rank-2 field equation
whose $rr$-component yields $\gamma=1$ (forcing $g_{rr}=1/(1-2\Phi_N)$) would promote the framework
from scalar to tensor and overturn the negative. Note 16 as written supplies none — that is the
open task this note leaves on the table.

## Extension — the scalar-gravity ladder, and the one rung note 16 is missing

The cleanest way to see *precisely* where the framework sits — and what it would take to fix it —
is to lay out all three theories on the single axis that governs light bending, the PPN parameter
$\gamma$ (the coefficient of spatial curvature in $g_{rr}\simeq1+2\gamma\,\Phi_N$):

$$
\underbrace{\gamma=-1}_{\text{Nordström}}\;\xrightarrow{\;+1\;}\;
\underbrace{\gamma=0}_{\substack{\text{framework}\\\text{(Einstein-1911)}}}\;\xrightarrow{\;+1\;}\;
\underbrace{\gamma=+1}_{\text{GR (measured)}}
$$

Each step adds exactly one unit of $\gamma$, i.e. one unit of $g_{rr}$'s response to mass:

| | $g_{rr}$ to first order | $\gamma$ | $(1+\gamma)$ | solar deflection |
|:---|:---:|:---:|:---:|:---:|
| Nordström | $1-2\Phi_N$ | $-1$ | $0$ | $0''$ |
| framework | $1+0\cdot\Phi_N$ (flat) | $0$ | $1$ | $0.875''$ |
| GR | $1+2\Phi_N$ | $+1$ | $2$ | $1.750''$ |

The framework sits at $\gamma=0$ because its spatial sector is the base-worldline curvature
$\kappa_{\rm Frenet}\in[\tfrac12,\sqrt5]$ — a **constant** in $\Phi_N$, so $\partial g_{rr}/\partial
\Phi_N=0$. Promoting it to $\gamma=1$ is not a tuning of existing knobs; it requires a *new,
mass-coupled equation* for the radial sector. Spell out the obstruction:

1. **$\gamma$ is rigid under the $c$-knob.** Note 35b's resummation acts only on $\theta(r)=g_{tt}$
   (the $A$-function). It cannot move $\gamma$, which lives entirely in $B(r)=g_{rr}$. This is why
   the $\tfrac13$–$\tfrac23$ perihelion band exists ($\beta$ *is* $c$-dependent) while $\gamma=0$ is
   frozen across the whole family. **One knob, one component.**

2. **What a $\gamma=1$ derivation must produce.** A genuine tensor extension needs a second field
   equation whose $rr$-projection reads, schematically,
   $$\partial_r\!\big(r\,[B(r)-1]\big)\;=\;8\pi\,r^2\,\rho(r)\quad\Longrightarrow\quad
   B(r)=\frac{1}{1-2\Phi_N(r)},$$
   i.e. $g_{rr}$ must be **sourced by the same mass** that sources $g_{tt}$. This is exactly the
   $G_{rr}=8\pi T_{rr}$ component of Einstein's equations, Bianchi-tied to $G_{tt}=8\pi T_{tt}$ so
   the *one* mass fixes *both*. Note 16 has a single scalar charge $L_y=1$ and one zero mode — it
   sources $g_{tt}$ and stops. There is no second, independently-sourced radial equation, and the
   actual spatial coefficient $\kappa_{\rm Frenet}$ is *mass-independent by construction*, so it
   **cannot** be the carrier of such a source term.

3. **The minimal honest target.** The smallest object that climbs the ladder is a rank-2 symmetric
   field $h_{\mu\nu}$ with its own Bianchi-protected divergence — not a second scalar. (A *second
   scalar* tuned to mimic $g_{rr}=1/(1-2\Phi_N)$ would be a back-fit, the §1.3 vacuity again: it
   passes one observable without a structural reason.) Concretely, the open task is to find within
   the corpus a two-tensor on the ordinal line whose linearised equation is $\Box\bar h_{\mu\nu}=
   -16\pi T_{\mu\nu}$, recovering $\gamma=1$ as a *theorem* rather than an imposition. Until note 16
   (or a successor) exhibits that, the ladder stops the framework one rung below GR — and the $0.875''$
   eclipse number is the experimental signature of exactly that missing rung.

The extension thus turns the negative into a **precise specification**: not "the framework is wrong,"
but "the framework is a correct $\gamma=0$ scalar-time theory that is missing one rank-2,
mass-sourced radial equation — and here is the exact equation it must produce to become GR."

## Addendum (note 41): scope — this tested the worldline, not the matrix

This note tested the two-vector **worldline** $V(k)$, scalar by construction, so "scalar theory" was
scoped too broadly. The shell coupling **matrix** $c_{ij}$ is genuinely higher-rank (entanglement
$S(\ell)=\frac{c}{3}\ln\ell$, $c\approx2.94$) and was not tested here. Note 41 runs that test: the
matrix's CFT structure is **source-free** (no mass in $c_{ij}$); its stable $c\approx2.9$ is a CFT
central charge, not a spatial-dimension count; and the *only* place mass enters — the $V_{\rm grav}$
zero-mode — is the **same scalar** tested here, giving $\gamma=0$, the half-deflection, again.
Holographically the matrix is at most a 2+1D AdS bulk, not 3+1D GR. Accurate verdict: **the
framework's mass-coupling is scalar ($\gamma=0$, half) whether read off the worldline or the matrix;
the matrix adds a source-free, at-most-2+1D holographic structure that does not couple to mass as a
3+1D metric.** See note 41.
