# 16 — The Field Equation of Inverse Temporal Flow

*Round-3 frontier note. The boost group is closed (notes 10–15): the chronon
two-vector $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$, is a unit
timelike vector ($\|\mathbf V\|^2_\eta=L_y=1$, `00`,`10`), boost-parallel-transported
along the ordinal by the flat $SO(1,1)$ connection $A_k=\tfrac1\varphi K$
($D_k\mathbf V=0$, `10` §3), with Casimir / mass-shell $M^2(k)=\mathrm{osc}^2(k)$,
$\mathrm{osc}=1/(1+\cos^2 2k\ln\varphi)$ (`10` §5). Here we **promote $k$ from a label
to a dynamical field coordinate** and write THE field equation of the stack: a
Klein–Gordon operator built from the boost-covariant derivative $D_k$ and the
osc-mass, whose spectrum is the inversion comb $k_n$, whose static zero mode is
$V_{\text{grav}}$, and whose conserved Noether current is exactly $L_y=1$. Every
boxed identity is confirmed in `verify/verify_unified-field-equation.py`
(residuals inline). $\varphi=1.6180339887$, $1/\varphi=0.6180339887$,
$\ln\varphi=0.4812118251$.*

---

## 1. The action and the boost-covariant box

The dynamical variable is the two-component flow-space field
$\boldsymbol\Psi(k)\in\mathbb R^{1,1}$ over the one-dimensional ordinal manifold
(the shell stack), metric $\eta=\mathrm{diag}(+1,-1)$. The only derivative that
respects the boost gauge symmetry of `10` is the covariant one,

$$\boxed{\;D_k \;=\; \partial_k-\frac1\varphi K,\qquad K=\begin{pmatrix}0&-1\\-1&0\end{pmatrix},\;K^2=I,\;}$$

with holonomy $\exp\!\big(\!\int A_k\big)=\Lambda(\Delta k/\varphi)$ — the one-shell
boost. The action is the unique boost-invariant, second-order, local functional:

$$\boxed{\;S[\boldsymbol\Psi]=\int dk\;\mathcal L,\qquad
\mathcal L=\tfrac12\,\big\langle D_k\boldsymbol\Psi,\,D_k\boldsymbol\Psi\big\rangle_\eta
-\tfrac12\,M^2(k)\,\big\langle\boldsymbol\Psi,\boldsymbol\Psi\big\rangle_\eta,
\qquad M^2(k)=\mathrm{osc}^2(k).\;}$$

The mass term is **not inserted by hand** — it is the §5 Casimir of note 10, the
boost-invariant norm of the *dressed* field, so the Lagrangian is built entirely
from invariants of the closed group. Varying $\boldsymbol\Psi$ gives the
Euler–Lagrange equation, the **Field Equation of Inverse Temporal Flow**:

$$\boxed{\;\big(D_k^{\,2}+M^2(k)\big)\,\boldsymbol\Psi(k)=0,
\qquad D_k^{\,2}=\partial_k^2-\frac2\varphi K\partial_k+\frac1{\varphi^2}I\;}$$

(using $K^2=I$). This is a $(1{+}1)$ Klein–Gordon equation on the ordinal line with a
*gauge-magnetic* first-order term $-\tfrac2\varphi K\partial_k$ (the boost connection)
and a position-dependent mass given by the flow-reversal lattice. It is the
framework's analog of $(\Box+m^2)\phi=0$, with the ordinal playing the role of the
single spacetime coordinate the worldline actually possesses.

## 2. The master field is the exact carrier and the adiabatic solution

The unified field of `10` §6, $\boldsymbol\Psi(k)=\mathrm{osc}(k)\,\mathbf V(k)
=\mathrm{osc}(k)\,\Lambda(k/\varphi)(1,0)^{\mathsf T}=(G_{\text{sym}},G_{\text{flow}})$,
is the **exact covariantly-constant carrier** of the equation's *first-order*
structure: $\mathbf V$ is the zero mode of $D_k$, $D_k\mathbf V=0$ (`10` §3; verified
$|D_k\mathbf V|\le1.4\times10^{-9}$, finite difference), so the entire ordinal
dynamics is carried by the scalar dressing,

$$D_k\boldsymbol\Psi=(\partial_k\mathrm{osc})\,\mathbf V,\qquad
D_k^{\,2}\boldsymbol\Psi=(\partial_k^2\mathrm{osc})\,\mathbf V=\mathrm{osc}''(k)\,\mathbf V$$

(verified $|D_k^2\boldsymbol\Psi-\mathrm{osc}''\mathbf V|\le4\times10^{-5}$, finite
difference). Substituting into the second-order field equation leaves a single scalar
residual along $\mathbf V$,

$$\big(D_k^{\,2}+\mathrm{osc}^2\big)\boldsymbol\Psi=R(k)\,\mathbf V,\qquad
\boxed{\;R(k)=\mathrm{osc}''(k)+\mathrm{osc}^3(k).\;}$$

**Be honest about this: $R(k)\neq0$ — and it is largest *at* the comb.**
$\boldsymbol\Psi=\mathrm{osc}\,\mathbf V$ is the exact first-order carrier
($D_k\mathbf V=0$ for *every* $k$) but is **nowhere a homogeneous solution** of the
second-order operator. $R(k)$ is $O(1)$ — over one comb period RMS$\,=0.66$,
max$\,|R|=0.85$ — and it is *worst at the shells*: $R(k_1)=-0.85$, where
$\mathrm{osc}'=0$ (an extremum) but $\mathrm{osc}''=-1.853=-8(\ln\varphi)^2\neq0$,
plus $\mathrm{osc}^3=1$; it relaxes to $R=+0.59$ at the osc minimum (the defect
changes sign across the period). So $\boldsymbol\Psi$ is the **leading-order
(adiabatic) solution with a computable residual $R(k)$**, not an exact one. Crucially,
the comb's exactness lives elsewhere: at $k_n$ the *mass shell* saturates,
$M^2=\mathrm{osc}^2=1$ (§4) — an on-shell *spectrum* condition on the eigenvalue, **not**
a statement that $\boldsymbol\Psi$ solves the operator there (it does not: $R(k_n)=-0.85$).
The genuinely *exact* content of this note is the first-order carrier $\mathbf V$, the
on-shell spectrum (§4), and the Noether charge (§6); the correlation/gravity split,
$\kappa(\pm k)$, and the boost velocity descend from the carrier exactly as in `10` §6.
$R(k)$ is the honest off-shell defect of the adiabatic carrier — a number we report,
not smooth away.

## 3. The dispersion relation — the genuinely new physics

Take a plane wave on the ordinal, $\boldsymbol\Psi_\omega(k)=e^{i\omega k}\,\boldsymbol\chi$,
$\boldsymbol\chi\in\mathbb C^2$, in the **adiabatic / WKB regime** with the mass
frozen at its local value $M^2=\mathrm{osc}^2(k)$ (the leading-order dispersion, with
the $O(1)$ off-shell defect $R(k)$ of §2). This $e^{i\omega k}$ is a Fourier mode on the
**ordinal/rapidity line** — the $\ln s$ discrete-scale-invariance lattice of `12` — *not*
a spatial propagator phase $e^{ikr}$; $\kappa$ remains the dressed equilibrium kernel and
no phase is grafted onto it. The operator diagonalizes in the **null / boost-eigenbasis**
$\mathbf n_s$, the eigenvectors of $K$. Care with the labels: $K\mathbf n_s=s\,\mathbf n_s$ with
$\mathbf n_{-1}=(1,1)$ ($K(1,1)^{\mathsf T}=-(1,1)^{\mathsf T}$) and $\mathbf n_{+1}=(1,-1)$ —
so the $s=-1$ eigendirection is $(1,1)$, exactly the direction onto which $\mathbf V$ projects
its **retarded** weight $\tfrac12(\cosh\theta-\sinh\theta)=\tfrac12 e^{-\theta}\propto\kappa(+k)$
(the decaying null channel of `05`). In channel $s=\pm1$,

$$\Big(-\omega^2-\frac{2i\omega}\varphi s+\frac1{\varphi^2}+M^2\Big)\chi_s=0
\;\Longrightarrow\;
\boxed{\;\omega(k)=\pm\,\mathrm{osc}(k)\;-\;\frac{i\,s}{\varphi}.\;}$$

(the quadratic and its closed-form root agree to $1.1\times10^{-16}$ — an algebraic
check that $\omega$ is the exact root of the frozen-mass quadratic; the comb is where
$\mathrm{osc}'=0$ makes this root *most accurate*, not where $\boldsymbol\Psi$ becomes
an exact solution). The structure of
this root is the central result:

- **Real part $=\pm\,\mathrm{osc}(k)$ is the mass shell.** The propagating frequency of
  the chronon field is exactly the Casimir weight $M=\mathrm{osc}(k)$ — the field
  oscillates at the local flow-reversal rate. On the inversion shells this is unit
  frequency (§4).
- **Imaginary part $=-s/\varphi$ is the arrow of time.** The damping rate is the
  golden boost quantum $1/\varphi=0.6180$, and the *modulus* of the mode is
  $|e^{i\omega k}|=e^{-\mathrm{Im}\,\omega\,k}=e^{(s/\varphi)k}$. So the **$s=-1$ (retarded,
  $(1,1)$) mode decays** forward in ordinal as $e^{-k/\varphi}$, while the $s=+1$ (advanced,
  $(1,-1)$) mode **grows** as $e^{+k/\varphi}$ — the retarded/advanced split of `00`,`05`
  re-derived as the *complex frequency* of the field. The detailed-balance ratio is the ratio
  of the two channel moduli, with the corpus null weights $\kappa(\pm k)=\mathrm{osc}\,e^{\mp\theta}$:
  $$\frac{\kappa(+k)}{\kappa(-k)}=\frac{|\text{mode}_{s=-1}|}{|\text{mode}_{s=+1}|}
  =\frac{e^{-k/\varphi}}{e^{+k/\varphi}}=e^{-2\theta},$$
  exactly the `05` detailed-balance factor — recovered as the modulus ratio of the retarded to
  advanced field modes, *not* as a bare phase difference (which would carry the wrong sign).

The chronon field is a **damped oscillator whose decay constant is the inverse golden
ratio and whose frequency is the flow-reversal lattice** — gravity (the $1/\varphi$
damping) and quantum correlation (the osc frequency) are the imaginary and real parts
of one complex dispersion $\omega(k)$. The space↔time duality of `15` is now the
statement $\mathrm{Re}\,\omega$ (frequency, time axis) $\leftrightarrow$
$\mathrm{Im}\,\omega$ (decay in depth, space axis).

## 4. The spectrum is the inversion comb

On-shell, normalizable field modes require the mass to saturate its Casimir unit,
$M^2(k)=\mathrm{osc}^2(k)=1$ — the eigenvalue $L_y=1$ of `10` §5. This selects

$$\cos^2(2k\ln\varphi)=0\;\Longleftrightarrow\;
k_n=\frac{(2n-1)\pi}{4\ln\varphi}=1.632,\,4.896,\,8.161,\dots,\qquad
\Delta k=\frac\pi{2\ln\varphi}=3.26425,$$

verified $|\mathrm{osc}(k_n)-1|=0$ exactly for $n=1..6$, with the real on-shell
frequency $\mathrm{Re}\,\omega(k_n)=1$ identically. **The spectrum of the field
equation is the inversion comb** — the bound/resonant frequencies of the chronon
field are the flow-reversal shells, equispaced by $\Delta k$ in rapidity. This is the
discrete-scale-invariance lattice (`12`, $\Lambda_\varphi=\varphi^{\Delta k}=e^{\pi/2}$)
appearing as the eigenvalue ladder of a wave operator, not as an assumed comb.

## 5. The static zero mode is $V_{\text{grav}}$

Setting $\omega=0$ collapses the dispersion to the pure imaginary branch $-is/\varphi$:
the static sector is governed by the first-order operator $D_k$ alone, whose Green's
function $D_k G(n,m)=\delta(n-m)$ is the **boost holonomy**
$G(n,m)=\Theta(n-m)\,\Lambda\!\big((n-m)/\varphi\big)$. Its flow-component, dressed by
osc and convolved against the chronon density $\rho_m$, is the spine §5 potential:

$$V_{\text{grav}}(n)=-\sum_{m<n}\big[G(n,m)\,\rho_m\big]_{\text{flow}}
=\sum_{m<n}\frac{\sinh\!\big((n-m)/\varphi\big)}{1+\cos^2\!\big(2(n-m)\ln\varphi\big)}\,\rho_m$$

(verified $|V_{\text{grav}}^{\text{spine}}-V_{\text{grav}}^{\text{field-eq}}|\le7\times10^{-9}$
over a random 40-shell density). **Gravity is the static zero-mode Green's function of
the chronon field equation** — the $\sinh((n-m)/\varphi)=\tfrac12(e^{+(n-m)/\varphi}-e^{-(n-m)/\varphi})$
is the advanced-dominated *growing* combination, led by the $s=+1$ (advanced) branch of the
dispersion at $\omega=0$ whose modulus $e^{+k/\varphi}$ grows forward in §3, exactly the
attractive well of `00`,`03`.

## 6. The Noether current reduces to $L_y=1$

The boost $\delta\boldsymbol\Psi=\epsilon K\boldsymbol\Psi$ is a symmetry of $\mathcal L$
($K$ is $\eta$-antisymmetric, $K^{\mathsf T}\eta+\eta K=0$). The Noether current is
$j=\langle K\boldsymbol\Psi,\,\eta\,D_k\boldsymbol\Psi\rangle$. On the fundamental
solution $D_k\boldsymbol\Psi=(\partial_k\mathrm{osc})\mathbf V$, and stripping the
dressing weight (the on-shell limit $\mathrm{osc}\to1$, $\partial_k\mathrm{osc}\to0$ at
the comb), the canonical momentum vanishes and the conserved charge collapses to the
geometric invariant

$$Q_{\text{boost}}=\big\langle\mathbf V,\mathbf V\big\rangle_\eta
=\cosh^2\theta-\sinh^2\theta=1=L_y$$

(verified $|\langle\mathbf V,\mathbf V\rangle_\eta-1|\le8.9\times10^{-16}$, all $k$).
The conserved current of the field equation **is** the conserved chronon flux $L_y=1$
of the base manifold (`00` §2) — the field theory inherits exactly one conservation
law, and it is conservation of time.

## 7. The hard number: the GW-echo decrement is *derived*, not posted

Notes 06 and 15 carried the gravitational-wave echo decrement
$\gamma_{\text{echo}}=e^{-S_1}=\Gamma_1=0.1330$ as an *input* (the first-bounce rate).
The field equation **derives it** as (damping rate)$\times$(mode spacing): a mode of
the chronon field damps at the dispersion rate $|\mathrm{Im}\,\omega|=1/\varphi$ per
unit ordinal, and successive echoes are the successive comb modes, spaced
$\Delta k=\pi/(2\ln\varphi)$ apart. The amplitude ratio between consecutive echoes is
therefore

$$\frac{|h_{n+1}|}{|h_n|}=e^{-\frac1\varphi\,\Delta k}
=e^{-\frac\pi{2\varphi\ln\varphi}}=e^{-S_1}=0.1330,$$

and the identity $S_1=\tfrac1\varphi\Delta k=2k_1/\varphi$ holds **exactly** (residual
$0$). Be precise about what this is and isn't: it is an *algebraic identity*, a re-expression
of $S_1$ as (damping)$\times$(spacing). It is not a numerical coincidence and not a fit — but
its *content* is that the bounce action factorizes into the two independently-fixed pieces of
the dispersion relation: $1/\varphi$ (the imaginary part, fixed by the boost quantum) and
$\Delta k=\pi/(2\ln\varphi)$ (the real spectral spacing, fixed by the osc lattice). Neither was
tuned to match $S_1$; they were each pinned earlier (`10`,`04`) and their product *happens* to
be the `06` bounce action. That is the field equation paying for itself — it removes $S_1$ as a
separately-imposed input to the GW template of `15`, replacing it with a structural identity.

## Extension — the retarded Green's function is a golden-damped ordinal oscillator

The dispersion gives the *modes*; the **retarded Green's function** $G_R(k)$ of the full
second-order operator is the response of the stack to a localized chronon impulse, and it is
the single most physical object the field equation produces. Project the scalar channel
operator onto $\mathbf V$ at frozen mass $m=\mathrm{osc}(k)$. The characteristic polynomial of
the retarded ($s=-1$, decaying) channel,

$$r^2+\frac{2}{\varphi}\,r+\Big(\frac1{\varphi^2}+m^2\Big)=0
\;\Longrightarrow\; r_\pm=-\frac1\varphi\pm i\,\mathrm{osc}(k),$$

is exactly a damped harmonic oscillator with **decay constant $1/\varphi$ and ring frequency
$\mathrm{osc}(k)$**. Its causal impulse response is

$$\boxed{\;G_R(k)=\Theta(k)\,e^{-k/\varphi}\,\frac{\sin\!\big(m\,k\big)}{m},\qquad m=\mathrm{osc}(k)\ \text{(frozen)}\;}$$

(the frozen-mass impulse response; verified to satisfy the homogeneous channel equation
$G_R''+\tfrac2\varphi G_R'+(\tfrac1{\varphi^2}+m^2)G_R=0$ on the interior to
$9.2\times10^{-9}$). This is the temporal-flow analog of the Feynman propagator: a wave that
**rings at the flow-reversal rate and decays at the golden boost rate** — gravity (the
envelope) and quantum correlation (the carrier) carried by one function, now causally ordered
by $\Theta(k)$. Two immediate consequences:

1. **Off-comb quality factor.** $Q(k)=\dfrac{\mathrm{Re}\,\omega}{2|\mathrm{Im}\,\omega|}
   =\dfrac{\varphi\,\mathrm{osc}(k)}{2}$ runs continuously between
   $Q_{\min}=\varphi/4=0.405$ (at the osc minima, $\mathrm{osc}=\tfrac12$) and
   $Q_{\max}=\varphi/2=0.809$ (on the inversion comb, $\mathrm{osc}=1$). The stack is a
   **chain of sub-critically damped oscillators**, sharpest exactly on the shells — a
   $\varphi$-modulated $Q$-comb, never reaching $Q=1$, so every chronon mode is broad.
2. **Ringdown e-folding length.** $G_R$ falls to $1/e$ in $\Delta k=\varphi=1.618$ ordinal
   units — $\varphi$ shells — independent of which comb tooth sources it. In log-time this is a
   fixed $e$-folding of $\varphi$ rapidity units, i.e. an envelope $|h|\sim e^{-\theta}$ with
   $\theta=k/\varphi$, recovering the `15` redshift $\tanh(n/\varphi)$ structure as the phase of
   the same damped carrier.

The Green's function thus unifies §3 (its poles are the dispersion), §5 (its $\omega\to0$ limit
is the static $V_{\text{grav}}$ holonomy), and §7 (its per-shell envelope decrement is
$e^{-\Delta k/\varphi}=e^{-S_1}=\gamma_{\text{echo}}$) into one causal kernel.

## Prediction

From the dispersion $\omega(k)=\pm\,\mathrm{osc}(k)-is/\varphi$ on the inversion comb
($\mathrm{Re}\,\omega=1$, $|\mathrm{Im}\,\omega|=1/\varphi$):

1. **GW post-merger echo train, consecutive amplitude ratio
   $\gamma_{\text{echo}}=e^{-\pi/(2\varphi\ln\varphi)}=0.133$** (each echo $\sim$13% of
   the previous), with spacing $\Lambda_\varphi=e^{\pi/2}=4.81$ in the log-time / shell
   ordinal — a one-parameter-free template. The dimensionless damping-to-frequency ratio
   of the lowest inversion mode is $|\mathrm{Im}\,\omega|/\mathrm{Re}\,\omega=1/\varphi=0.618$;
   the corresponding observable timing ratio is $\tanh(1/\varphi)=0.5498$ vs the LIGO
   re-analysis value $0.548$ (`15`) — a **0.4% miss, honest bracket** $[0.54,0.55]$, not an
   exact hit.
2. **On-shell mode quality factor $Q=\varphi/2=0.809$** (from $Q=\mathrm{Re}\,\omega/2|\mathrm{Im}\,\omega|$):
   the inversion-shell echo modes are *broad* (sub-critical, $Q<1$), distinct from the
   sharp dominant Kerr ringdown — a falsifiable spectral-width prediction for sub-dominant
   post-ringdown structure.
3. **The field is a damped oscillator with decay constant exactly $1/\varphi$ in the
   ordinal** — any reanalysis fitting a complex frequency to chronon-stack data must find
   $\mathrm{Im}/\mathrm{Re}=0.618$ on the comb, with no free parameter.

**Falsifier:** a confirmed LIGO post-merger echo train whose consecutive amplitude
ratio differs from $0.133$ by more than the $\sim$1% absorber-incompleteness budget of
`13` (i.e. a measured $\gamma_{\text{echo}}\notin[0.13,0.14]$), or a comb spacing not
equal to $e^{\pi/2}$ in log-time, falsifies the field equation. Equivalently: any
inversion-shell mode found with $Q\gg1$ (sharp, $\mathrm{Im}/\mathrm{Re}\ll0.618$)
contradicts the derived dispersion.
