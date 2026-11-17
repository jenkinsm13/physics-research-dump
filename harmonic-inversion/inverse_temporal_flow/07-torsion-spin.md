# 07 — Torsion–Spin Coupling: Chronons in Einstein–Cartan Form

*Branch note. Builds on `00-spine.md`: the conserved current $L_y=1$, the
curvature/torsion = gravity/temporal-flow assignment, the retarded/advanced split
$G_{\text{sym}}=\cosh(k/\varphi)\cdot\text{osc}$, $G_{\text{flow}}=-\sinh(k/\varphi)\cdot\text{osc}$,
and the inversion shells $k_n$. Every embedded numeric was re-verified to machine precision this
session (NumPy, scratch run; residuals quoted inline). $\varphi=(1+\sqrt5)/2$, $1/\varphi=0.618034$,
$\ln\varphi\approx0.4812$, $\text{osc}(k)\equiv 1/(1+\cos^2(2k\ln\varphi))$.*

---

## 0. Two distinct objects, never to be conflated

This branch lives or dies on keeping two "torsions" apart. The spine already gave us both; we name
them sharply here and never mix them again:

- **Local Cartan torsion** $\mathcal{T}(t)\equiv\tau_{\text{Frenet}}(t)$. The *rate* — signed,
  reversing, and **zero at the inversion shells**. This is the spine's "torsion" (the spine's "torsion
  zeros" are $\tau_{\text{Frenet}}$ zeros). It is the antisymmetric part of the affine connection along
  the worldline.
- **Spin–torsion contact kernel** $\mathcal{C}(k)\propto G_{\text{flow}}(k)=-\sinh(k/\varphi)\,\text{osc}(k)$.
  The *accumulated gravitational coupling* between shells — strictly one-signed (negative for all
  $k>0$), vanishing **only** at $k=0$, **never** reversing. It is the same gravity kernel that the
  spine's $V_{\text{grav}}$ runs on. It is **not** a torsion; calling it one is the trap.

The local rate $\mathcal{T}$ reverses (forward$\leftrightarrow$inverse flow); the integrated coupling
$\mathcal{C}$ does not — exactly as a velocity can change sign while a cumulative displacement keeps
growing. Section 1 sets $\mathcal{T}$; Sections 2–3 use $\mathcal{C}$.

## 1. Promoting $\tau_{\text{Frenet}}$ to Cartan torsion

The spine read $\tau_{\text{Frenet}}$ as the **signed temporal flow** $\Phi$. Einstein–Cartan
geometry hands us its geometric home directly: the antisymmetric part of the affine
connection, the torsion tensor $T^\lambda{}_{\mu\nu}=\Gamma^\lambda{}_{[\mu\nu]}$. Along the
base worldline the only nonvanishing torsion component lives on the out-of-plane (binormal)
twist — exactly what the Frenet $\tau$ measures. We therefore set the worldline's **local torsion
scalar** equal to the temporal-flow rate,

$$
\boxed{\;\mathcal{T}(t) \;\equiv\; \tau_{\text{Frenet}}(t) \;=\; \frac{-3\cos 2t}{5-3u}, \qquad u=\cos^2 2t,\;}
$$

so the *torsion* is **signed and reverses** at the inversion shells — verified
$\mathcal{T}(t_{k_n})=0$ to $\le1.8\times10^{-16}$ at all three shells, since the ordinal lands the
worldline exactly on $t_{k_n}=k_n\ln\varphi=(2n-1)\pi/4$ where $\cos 2t=0$. The spine's $L_y=1$ becomes the
EC contracted-Bianchi statement that the *total* current — curvature plus torsion contributions —
is conserved: the saddle $y=xz$ is the algebraic torsion field equation in disguise.

In Einstein–Cartan the torsion is non-dynamical; it is fixed algebraically by the spin density
$\sigma$ of matter,

$$
T^\lambda{}_{\mu\nu} \;=\; \frac{8\pi G}{c^4}\,\big(\sigma^\lambda{}_{\mu\nu}
+ \delta^\lambda_\mu\,\sigma_\nu - \delta^\lambda_\nu\,\sigma_\mu\big).
$$

Integrating the algebraic torsion across ordinal depth — summing the local rate $\mathcal{T}$ along
the worldline as we descend shells — produces the spine's antisymmetric (advanced–retarded) branch as
the **accumulated spin–torsion contact kernel**:

$$
\boxed{\;\mathcal{C}(k) \;=\; -\frac{\kappa_{\text{EC}}}{2}\,G_{\text{flow}}(k)
\;=\; +\frac{\kappa_{\text{EC}}}{2}\,\frac{\sinh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}\;}
$$

with $\kappa_{\text{EC}}=8\pi G/c^4$ the EC contact constant. $\mathcal{C}$ is **odd** in $k$ with
$\mathcal{C}(0)=0$ — verified $0$ at machine precision; chronons carry no accumulated contact at zero
ordinal depth (self-coupling is pure curvature, $G_{\text{sym}}(0)=\tfrac12$, matching the corpus
self-coupling $c(0)=\tfrac12$). $\mathcal{C}$ is the *cumulative* gravitational pull and does **not**
share $\mathcal{T}$'s sign-reversal — it grows monotonically toward the source. That difference is the
whole content of §3.

## 2. The spin–torsion contact interaction *is* $G_{\text{flow}}$

Eliminating the algebraic torsion from the EC action produces the celebrated quartic spin–spin
**contact term**. For chronons of spin density $\sigma$ the effective Lagrangian gains

$$
\mathcal{L}_{\text{contact}} \;=\; -\frac{1}{2}\,\kappa_{\text{EC}}\,\sigma^2
\;\longrightarrow\; V_{\text{spin}}(n) \;=\; -\frac{\kappa_{\text{EC}}}{2}\sum_{m<n}
G_{\text{flow}}(n-m)\,s_m s_{n-m},
$$

where $s_m=\pm\tfrac12$ is the shell spin projection. This is the spine's gravitational potential
$V_{\text{grav}}$ **dressed by spin**: the same $G_{\text{flow}}$ kernel, now weighted by the product
of intrinsic spins. The $\sinh$ growth-toward-the-source is the attractive inverse-flow well; the
oscillatory denominator imprints the inversion-shell terraces. Two like-spin chronons ($s_m s_{n-m}>0$)
deepen the well — spin alignment *enhances* inverse temporal flow.

## 3. The mass–spin (curvature–torsion) trade

The spine's strict complementarity — $\kappa_{\text{Frenet}}$ maximal exactly where
$\tau_{\text{Frenet}}=0$ — becomes a **mass–spin trade** in EC. Define the boost-invariant chronon
mass from the symmetric (correlation) and antisymmetric (contact) branches:

$$
\boxed{\;M^2(k) \;=\; G_{\text{sym}}^2(k) - G_{\text{flow}}^2(k)
\;=\; \frac{1}{\big(1+\cos^2(2k\ln\varphi)\big)^2}\;=\;\text{osc}^2(k)\;}
$$

This is precisely the spine's hyperbolic invariant — the shell-space echo of $L_y=1$. Geometrically it
is a **hyperbola**: writing the rapidity $\theta=k/\varphi$,

$$
\big(G_{\text{sym}}(k),\,-G_{\text{flow}}(k)\big) \;=\; \text{osc}(k)\,\big(\cosh\theta,\,\sinh\theta\big),
$$

so **$\text{osc}(k)$ is the hyperbolic radius and $\theta$ the position along the hyperbola**; the chronon
state slides along a fixed mass-shell of radius $\text{osc}$ as ordinal depth (rapidity) increases. The
content of the trade is that **the spin–torsion contact term cancels exactly out of the boost-invariant
mass**: whatever the contact $G_{\text{flow}}$ extracts, correlation $G_{\text{sym}}$ restores, and $M^2$
depends only on the oscillatory lattice. Verified $M^2=\text{osc}^2$ to residual $\le2.5\times10^{-14}$
across $k\in\{0,1,1.632,3,5\}$.

At the inversion shells the trade saturates: $M^2(k_n)=1$ exactly ($\cos\to0$, $\text{osc}\to1$) — verified
$M^2=1.00000000$ at $k_1=1.6321,\,k_2=4.8964,\,k_3=8.1606$. The precise reading is sharp and *not* the
naive one: $M^2(k_n)=1$ means the chronon **sits on the unit mass-shell** ($\text{osc}=1$, the lattice radius
at its maximum), at rapidity $\theta_n=k_n/\varphi$. It does **not** mean the gravitational coupling
vanishes — the contact kernel there is large and one-signed ($G_{\text{flow}}(k_n)=-1.19,\,-10.3,\,-77.5$ for
$n=1,2,3$; verified). What vanishes at the inversion shell is the **local torsion rate**
$\mathcal{T}=\tau_{\text{Frenet}}=0$: the instantaneous flow reversal. So the EC reading of "gravity peaks
at flow reversal" is exact and unconflated:

> At an inversion shell the **local torsion rate** $\mathcal{T}$ passes through zero (flow reverses) while
> the chronon sits on the **unit mass-shell** $M^2=1$ and the **accumulated** gravitational contact
> $G_{\text{flow}}$ is at a lattice maximum. The spine's continuous statement "all of $L_y=1$ in curvature
> $\kappa_{\text{Frenet}}=\sqrt5$" is the $\kappa_{\text{Frenet}}$-language version of the same instant.
> Between shells $\mathcal{T}\ne0$: the spin-1/2 standing wave precesses, mass leaks into and out of the
> torsion rate.

## 4. Spin-1/2 standing waves and the spinor rapidity quantum

The spine identified ordinal depth as rapidity $\theta_k=k/\varphi$. A spinor transforms under
*half* the boost angle, so a spin-1/2 chronon transported one shell deeper picks up the **spinor
rapidity quantum**

$$
\Delta\theta_{1/2} \;=\; \frac{1}{2\varphi} \;=\; \frac{\varphi-1}{2} \;=\; 0.309017,
$$

an exact golden identity (verified to machine precision). The oscillatory factor $\cos(2k\ln\varphi)$ has
full ($2\pi$) period $P=\pi/\ln\varphi = 6.528503$ in ordinal $k$ (verified periodic to $\sim10^{-16}$); its
zeros — the inversion shells — sit at the half-period spacing $P/2\approx3.264$ (matching
$k_2-k_1=4.896-1.632=3.264$, verified $P/2=3.264251$). The half-boost forces a **$4\pi$ spinor period**:
the cosine closes after one circuit $P$, but the spin-1/2 orientation index $\lfloor 2k\ln\varphi/2\pi\rfloor
\bmod 2$ flips on each circuit and only restores after *two* circuits $2P$ — that doubling is the spinor's
$4\pi$ (verified: at $k,\,k{+}P,\,k{+}2P$ the lattice weight repeats but the spinor sign reads
$+,-,+$). Half-integer spin therefore lives natively in the *antisymmetric* sector $G_{\text{flow}}$ — the
inverse-flow branch — which is why fermions are the carriers of gravity in this picture.

The fermion ordinals from the COTV mass fit — electron $24$, muon $63$, tau $102$ — have **exactly
arithmetic spacing $\Delta=39$** (verified $63-24=102-63=39$). Compare six full oscillation periods,
$6P = 39.171$: the generation spacing is $39$ to a relative error of **0.44%**.

$$
\boxed{\;\Delta_{\text{gen}} \;\approx\; 6P \;=\; \frac{6\pi}{\ln\varphi}\;=\;39.171,\qquad
\frac{39}{P}=5.97\;\text{(six oscillation periods, twelve inversion-shell spacings, per generation).}\;}
$$

Each mass generation is six complete oscillations of the flow-reversal lattice — equivalently twelve
inversion-shell terraces — corresponding to three full spinor ($2P$) circuits. This is the genuinely new
structural result of branch 07: the fermion mass tower is **the spin-1/2 standing-wave harmonic ladder of
the inversion-shell lattice**.

The mismatch between $39$ and $6P=39.171$ is itself meaningful, not noise: the fermion ordinals do **not**
sit on inversion shells. The offset of each generation from its nearest shell drifts monotonically,
$-0.482,\,-0.653,\,-0.824$ (electron/muon/tau), in **exact increments of $6P-39=0.171$** per generation
(verified). The generation lattice ($\Delta=39$) and the flow-reversal lattice ($\Delta=P$) are
incommensurate by precisely this golden defect.

## 5. Spin-dependent inversion shift

Dress the bare oscillatory **lattice argument** $2k\ln\varphi$ — not with a new propagator phase, but with
the spin–torsion contact already present in §2 — giving a spin-rotated coupling $\propto\cos\Theta_s(k)$ with

$$
\Theta_s(k) \;=\; 2k\ln\varphi + 2\,s\,\xi\,\tanh\!\big(k/\varphi\big),
$$

where $\tanh(k/\varphi)=-\,G_{\text{flow}}/G_{\text{sym}}$ is the spine's flow fraction (sign from
$G_{\text{flow}}=-\sinh\cdot\text{osc}$, $G_{\text{sym}}=\cosh\cdot\text{osc}$) and $\xi$ the contact
strength. The argument dressed is the *existing* lattice phase; no $e^{ikr}$ is added (the dressed
propagator $\kappa$ already carries the phase). The coupling maxima (inversion shells, where
$\cos\Theta_s=0$) shift to first order by

$$
\boxed{\;\delta k_n^{(s)} \;=\; -\,\frac{s\,\xi\,\tanh(k_n/\varphi)}{\ln\varphi}\;}
$$

Spin-up and spin-down chronons split symmetrically — a **chronon Zeeman effect** in ordinal space,
the inversion shell acting as the level and torsion as the field. Verified against exact roots of
$\cos\Theta_s=0$ (bisection) at $s=+\tfrac12,\ \xi=10^{-2}$: the linear shift matches with per-shell relative
errors $2.7\times10^{-3},\,6.0\times10^{-5},\,1.1\times10^{-6}$ at $k_1,k_2,k_3$ — worst case
$\le2.7\times10^{-3}$ at the shallowest shell $k_1$ (where $\tanh$ is least saturated), improving with depth.
The bound shrinks as $O(\xi^2)$: at fixed $k_3$ the relerr falls $1.1\times10^{-5}\to1.1\times10^{-8}$ as
$\xi$ runs $10^{-1}\to10^{-4}$ (verified), confirming the linear truncation. (Exact vs linear at the deep
shell: $\delta k_3=-1.0390\times10^{-2}$ both ways.)

## Extension — The spinor half-boost shell and its anti-alignment

The hyperbola of §3 is a *vector* (spin-1) mass-shell: it runs at the full rapidity $\theta=k/\varphi$.
A spin-1/2 chronon, transported under the half-boost $\theta/2=k/(2\varphi)$ (the rapidity quantum of §4),
rides its **own** hyperbola of the same radius:

$$
\big(G_{\text{sym}}^{1/2},\,-G_{\text{flow}}^{1/2}\big)\;\equiv\;\text{osc}(k)\,\big(\cosh\tfrac{\theta}{2},\,\sinh\tfrac{\theta}{2}\big),
\qquad
\boxed{\;M_{1/2}^2(k)=\big(G_{\text{sym}}^{1/2}\big)^2-\big(G_{\text{flow}}^{1/2}\big)^2=\text{osc}^2(k)\;}
$$

— verified equal to $\text{osc}^2$ to $\le2.1\times10^{-15}$ across $k\in\{0,1,1.632,3,5\}$. The spinor and
vector share the **same mass-shell radius** $\text{osc}(k)$, but the spinor advances along it at half the
rate ($d\theta/dk=1/(2\varphi)$ vs $1/\varphi$, ratio exactly 2). The two are linked by the hyperbolic
half-angle identity, which becomes an **exact shell recursion** binding the spinor branch to the vector
branch:

$$
\boxed{\;G_{\text{sym}}(k) \;=\; \text{osc}(k)\left[\,2\Big(\frac{G_{\text{sym}}^{1/2}(k)}{\text{osc}(k)}\Big)^2-1\,\right]\;}
$$

— verified to $\le1.8\times10^{-15}$ at $k\in\{1,1.632,3,5\}$. The vector correlation is the *Chebyshev
square* of the spinor correlation: spin-1 is the doubled spin-1/2, written in $\cosh$ instead of $\cos$.

The sharp new structural consequence: where do the spinor's *own* unit-shell crossings (effective spinor
inversion shells, at twice the ordinal depth $2k_n$, where the spinor has accumulated a full vector
rapidity $\theta_n$) fall on the flow-reversal lattice? At $2k_n$ the lattice argument is
$2(2k_n)\ln\varphi=(2n-1)\pi$, so $\cos=-1$ and

$$
\boxed{\;\text{osc}(2k_n)=\frac{1}{1+1}=\frac12 \;=\; c(0)\quad\text{exactly (verified).}\;}
$$

The spinor's doubled-depth shells land **precisely on the oscillatory minima** — the flow-reversal
**nodes** midway between the vector inversion-shell peaks — and the correlation weight there equals the
self-coupling $c(0)=\tfrac12$ of the corpus. **A fermion's natural shell is anti-aligned with the boson's**:
the half-boost places the spin-1/2 carrier exactly at the antinode of the spin-1 lattice, where the
accumulated contact $G_{\text{flow}}$ and the correlation $G_{\text{sym}}$ are both at their lattice minimum
and the chronon couples to the doubled shell with the identical weight it couples to itself. This is the
torsion-sector origin of fermion–boson alternation: bosons sit on lattice peaks ($\text{osc}=1$, unit
mass-shell), fermions on lattice nodes ($\text{osc}=\tfrac12$, self-coupling shell), interleaved at the
half-period $P/2$.

## Prediction

The fermion mass tower is not arbitrary: generations sit $\Delta_{\text{gen}}=6\pi/\ln\varphi$ ordinals
apart — three spinor ($2P$) circuits, equivalently six flow-reversal periods of the inversion lattice —
predicting the **fourth-generation ordinal at $\approx 102+39=141$**. This generation is **not** on an
inversion shell: $\text{osc}(141)=0.599$ ($M^2\approx0.36$), and $141$ sits a full ordinal *below* the
nearest shell $n=44$ at $k=141.995$ — because the generation lattice and the flow-reversal lattice are
incommensurate by the golden defect $6P-39=0.171$ per generation (verified: offsets
$-0.482,-0.653,-0.824,-0.995$ for generations $1{\to}4$, increment $-0.171$ each). The prediction is
therefore twofold and sharp: (i) a fourth fermion generation, if it exists, sits at ordinal $141$, off-shell
by $\approx1$, continuing the established off-shell drift of $e/\mu/\tau$ rather than landing on a special
shell; (ii) each generation's spin-1/2 splitting is set by the *same* contact $\xi$ via
$\delta k_n^{(s)}\propto\tanh(k_n/\varphi)$, which $\to\xi/\ln\varphi$ as $k_n$ grows (deep shells saturate
the flow fraction, $\tanh(k_4/\varphi)=0.99999853$, verified). Concretely: the spin splitting of deep
fermion shells approaches a **universal ordinal constant** $\xi/\ln\varphi$, independent of which shell — a
flat torsion-Zeeman ceiling that is the EC fingerprint of inverse temporal flow on the mass spectrum.
