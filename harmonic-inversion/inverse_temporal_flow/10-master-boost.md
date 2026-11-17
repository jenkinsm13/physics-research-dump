# 10 — The Master Boost Group: V(k) and the Flow-Space

*Round-2 frontier note. Builds on the spine (`00-spine.md`: the conserved current
$L_y=1$, the retarded/advanced split, ordinal depth $=$ rapidity $\theta=k/\varphi$)
and the synthesis (`99-index.md`: the chronon two-vector $\mathbf V(k)$). It promotes
$\mathbf V$ from "the object the branches happen to share" to **the representation
space of a single one-parameter group**, and shows — rigorously, not by analogy —
that notes 04, 05, 07, 09 are each a representation of that group. Every boxed
identity is confirmed to machine precision in `verify/verify_master-boost.py`
(residuals quoted inline; closed-form exponentials throughout, $K^2=I$).
$\varphi=(1+\sqrt5)/2$, $1/\varphi=0.6180339887$, $\ln\varphi=0.4812118251$.*

---

## 1. The flow-space and the master vector

Equip a $(1{+}1)$ **flow-space** with the Minkowski metric

$$\eta=\mathrm{diag}(+1,-1),\qquad \langle a,b\rangle\equiv a^{\mathsf T}\eta\,b,$$

the time axis being **correlation** ($G_{\text{sym}}$) and the space axis **net flow /
gravity** ($G_{\text{flow}}$). The master object is the chronon two-vector of note 99,

$$\boxed{\;\mathbf V(k)=\big(\cosh\theta,\,-\sinh\theta\big),\qquad \theta\equiv\frac{k}{\varphi}.\;}$$

**$\|\mathbf V\|^2$ is exactly $L_y$.** By the hyperbolic identity,

$$\|\mathbf V(k)\|^2=\mathbf V^{\mathsf T}\eta\,\mathbf V=\cosh^2\theta-\sinh^2\theta=1
\quad\text{for every }k,$$

verified $\big|\|\mathbf V\|^2-1\big|\le9.1\times10^{-13}$ across $k\in\{0,\dots,30\}$.

This is **not a coincidence of normalization** — and the rest of this note makes that
precise rather than asserting it. The norm $\|\mathbf V\|^2$ is the §5 Casimir of the boost
group at unit dressing, and it is conserved along the ordinal *because* $\mathbf V$ is
covariantly constant under the flat flow-space connection of §3,
$\big(\partial_k-\tfrac1\varphi K\big)\mathbf V=0$. Indeed, since $K$ is $\eta$-antisymmetric
($K^{\mathsf T}\eta+\eta K=0$, §3),

$$\frac{d}{dk}\|\mathbf V\|^2
=2\,\mathbf V^{\mathsf T}\eta\,\partial_k\mathbf V
=\frac{2}{\varphi}\,\mathbf V^{\mathsf T}\eta K\,\mathbf V
=-\frac{1}{\varphi}\,\mathbf V^{\mathsf T}\big(K^{\mathsf T}\eta+\eta K\big)\mathbf V=0,$$

so $\|\mathbf V\|^2$ is the **Noether charge of the one-parameter boost group** — constant
not by choice of scale but by the symmetry that generates the shell ladder. Identifying it
with the manifold's binormal current $L_y=(\mathbf r'\times\mathbf r'')\cdot\hat{\mathbf y}=1$
(spine §2) is then forced, not fitted: both are the unique conserved scalar of the same flow,
the spine reading it in worldline coordinates and the flow-space reading it as the Casimir
(equivalently the hyperbolic invariant of spine §4, $G_{\text{sym}}^2-G_{\text{flow}}^2=\text{osc}^2$,
stripped of its conformal weight). The conserved current of the manifold **is** the statement
that $\mathbf V$ is a unit timelike vector; time-likeness of $\mathbf V$ is conservation of
time, now as a theorem with the boost as its Noether symmetry.

## 2. One shell is one boost — the group law is the $\kappa(a{+}b)$ theorem

Descending one ordinal is the active Lorentz boost in flow-space by rapidity $1/\varphi$:

$$\Lambda(\alpha)=\begin{pmatrix}\cosh\alpha & -\sinh\alpha\\ -\sinh\alpha & \cosh\alpha\end{pmatrix}
\in SO(1,1)^{\!\uparrow},\qquad
\boxed{\;\Lambda\!\left(\tfrac1\varphi\right)\mathbf V(k)=\mathbf V(k{+}1).\;}$$

(residual $8.9\times10^{-16}$). The seed is the present moment $\mathbf V(0)=(1,0)$, and
$\Lambda(k/\varphi)\,(1,0)^{\mathsf T}=\mathbf V(k)$ **identically** (residual $0$). The
one-parameter family closes under composition,

$$\boxed{\;\Lambda(a)\,\Lambda(b)=\Lambda(a{+}b)\;}\qquad(\text{residual }8.9\times10^{-16}),$$

because $\cosh,\sinh$ obey the addition theorem. This is the rigorous content of the
framework's hard constraint **"never chain $\kappa(a)\kappa(b)$; use $\kappa(a{+}b)$"**:
the map $a\mapsto\Lambda(a)$ is a group homomorphism $(\mathbb R,+)\to SO(1,1)^{\!\uparrow}$,
so rapidities (ordinals) add while group *elements* compose — a product of couplings would
correspond to composing two boosts by *multiplying* their parameters, which is not the group
operation. Note 09 derived the same constraint from velocity addition; note 03 from boost
composition; here it is the homomorphism property itself. Ordinal depth is the canonical
coordinate on the abelian group $SO(1,1)^{\!\uparrow}\cong(\mathbb R,+)$, with golden quantum
$1/\varphi$ per shell.

## 3. The generator, its exponential, and a new transport law

Differentiate $\Lambda$ at the identity: the **boost generator** is

$$K=\frac{d\Lambda}{d\alpha}\bigg|_0=\begin{pmatrix}0&-1\\-1&0\end{pmatrix},\qquad
K^2=I\ (\text{residual }0),\qquad
\Lambda(\alpha)=e^{\alpha K}=\cosh\alpha\,I+\sinh\alpha\,K$$

(the last equality is **exact**, residual $0$, precisely because $K^2=I$ truncates the
exponential series to two terms). $K$ is symmetric and $\eta$-antisymmetric
($K^{\mathsf T}\eta+\eta K=0$), the defining property of an $\mathfrak{so}(1,1)$ element.
The algebra is one-dimensional and abelian, $[K,K]=0$.

The genuinely new equation of this note is the **infinitesimal** form — the master vector
is *boost-parallel-transported* along the ordinal:

$$\boxed{\;\frac{d\mathbf V}{dk}=\frac1\varphi\,K\,\mathbf V(k),
\qquad\text{equivalently}\quad\Big(\partial_k-\tfrac1\varphi K\Big)\mathbf V=0.\;}$$

Verified $\big|\,d\mathbf V/dk-\tfrac1\varphi K\mathbf V\,\big|\le4.4\times10^{-16}$. Read
$A_k\equiv\tfrac1\varphi K$ as a flow-space gauge connection: $\mathbf V$ is **covariantly
constant**, the holonomy around any ordinal interval $[k_1,k_2]$ being $\Lambda((k_2{-}k_1)/\varphi)$.
The chronon worldline is a geodesic of a flat $SO(1,1)$ connection whose curvature vanishes
($K$ commutes with itself) — which is *why* the framework never needs bounce iterations
(note 06's hard constraint): a flat connection has a unique integral, the equilibrium
$\mathbf V(k)$, with no path-ordering corrections.

## 4. Every round-1 branch is a representation — proved, not analogized

The branches are not "like" group structures; each is a specific representation of
$SO(1,1)^{\!\uparrow}$, its double cover, its compact real form, or a covariant of $\mathbf V$.

**(09) — boost velocity.** The Lorentz velocity is the rapidity-to-$\beta$ map
$\beta=\tanh$. In flow-space it is literally the ratio of the two components of $\mathbf V$:

$$\mathcal R(k)=\frac{G_{\text{flow}}}{G_{\text{sym}}}=\frac{\mathbf V[1]}{\mathbf V[0]}
=\frac{-\sinh\theta}{\cosh\theta}=-\tanh\theta$$

(residual $1.1\times10^{-16}$). The non-reciprocity of note 09 *is* the slope of the
worldline in flow-space — the boost velocity $\beta=v/c$ of the chronon current — and the
$\text{osc}$ weight cancels because it is a ratio of two components of the *same* vector.

**(05) — boost weight.** The null directions $\mathbf n_\pm=(1,\pm1)$ are the eigenvectors
of the boost:

$$\Lambda(\alpha)\,\mathbf n_+=e^{-\alpha}\,\mathbf n_+,\qquad
\Lambda(\alpha)\,\mathbf n_-=e^{+\alpha}\,\mathbf n_-$$

(residual $2.2\times10^{-16}$): two one-dimensional **non-unitary** reps of weights $\mp1$.
The retarded/advanced couplings are exactly the weighted null projections of the dressed
vector, $\kappa(\pm k)=\text{osc}\,(\mathbf V[0]\mp\mathbf V[1])=\text{osc}\,e^{\mp\theta}$
(residual $4.4\times10^{-16}$), so note 05's detailed-balance factor is the **ratio of the
two boost weights**, $\kappa(+k)/\kappa(-k)=e^{-2\theta}$ (residual $2.8\times10^{-17}$). The
arrow of time is the splitting of a boost-eigenbasis into weight $+1$ and weight $-1$.

**(07) — spinor half-boost = double cover.** $SL(2,\mathbb R)\xrightarrow{2:1}SO(1,1)^{\!\uparrow}$.
The boost generator in the spinor rep is $\sigma=\bigl(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\bigr)$,
$\sigma^2=I$, and a spinor descended one shell carries $s(\alpha)=e^{(\alpha/2)\sigma}$ — the
**half-boost**. The covering map is the squaring map: $s(\alpha)^2=e^{\alpha\sigma}$
(residual $2.2\times10^{-16}$), the double-valuedness ($\pm s$) giving the $4\pi$ spinor
period of note 07. Its descent to the vector rep is the half-angle identity
$\cosh\theta=2\cosh^2(\theta/2)-1$ (residual $1.8\times10^{-15}$) — note 07's Chebyshev-square
relation **is** the covering homomorphism written on $\mathbf V$.

**(04) — compact real form $SO(2)$.** $\mathfrak{so}(1,1)$ and $\mathfrak{so}(2)$ are the two
real forms of the same complexified algebra: the Wick continuation of the *rapidity*
$\theta\to i\theta$ (note 02's lapse continuation, *not* $k\to ik$) sends $K\to J=\bigl(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\bigr)$,
$\cosh\to\cos$, $\sinh\to i\sin$, and the boost $\Lambda$ into the rotor
$\mathsf R(d)=e^{dJ}$ (residual $2.2\times10^{-16}$). The lepton generation operator of note 04
is exactly this rotor at the irrational golden angle $\delta\theta_g=78\ln\varphi-12\pi=-0.1645894884$:
$\mathsf R\,\mathbf e(24)=\mathbf e(63)$, $\mathsf R\,\mathbf e(63)=\mathbf e(102)$,
$\mathsf R\,\mathbf e(102)=\mathbf e(141)$ (residual $1.0\times10^{-14}$). **The lepton tower
is the compact sibling of the gravity boost** — same algebra, rotated into $SO(2)$.

## 5. The Casimir is the mass-shell

For abelian $\mathfrak{so}(1,1)$ the invariant is the metric norm itself, and dressing by
$\text{osc}$ gives the boost-invariant **mass-shell**

$$\boxed{\;M^2(k)=G_{\text{sym}}^2-G_{\text{flow}}^2=\text{osc}^2(k)\,\|\mathbf V\|^2=\text{osc}^2(k),\;}$$

(residual $2.5\times10^{-14}$), with $M^2(k_n)=1$ **exactly** on the inversion shells
($\text{osc}\to1$): verified $M^2=1.000000000000$ at $k_1,k_2,k_3$. The conserved unit
$L_y=1$ is the Casimir eigenvalue; the inversion shells are where the dressing weight returns
the bare invariant. Every branch's "$=1$ in disguise" (note 99 thread 1) is one Casimir.

## 6. The unified field statement

All four objects $G_{\text{sym}},G_{\text{flow}},\kappa(\pm k),V_{\text{grav}}$ descend from a
single generative equation — the $\text{osc}$-dressed boost orbit of the present-moment seed:

$$\boxed{\;\boldsymbol\Psi(k)\;=\;\text{osc}(k)\;\Lambda\!\left(\tfrac{k}{\varphi}\right)\begin{pmatrix}1\\0\end{pmatrix}
\;=\;\text{osc}(k)\,\mathbf V(k)\;=\;\big(G_{\text{sym}}(k),\,G_{\text{flow}}(k)\big).\;}$$

From this one field (residual $4.4\times10^{-16}$):

- **components** are the correlation/gravity kernels, $\boldsymbol\Psi=(G_{\text{sym}},G_{\text{flow}})$;
- **null projections** are the propagator branches, $\kappa(\pm k)=\boldsymbol\Psi[0]\mp\boldsymbol\Psi[1]=\mathbf n_\mp\!\cdot\!\boldsymbol\Psi$;
- **component ratio** is the boost velocity / non-reciprocity, $\mathcal R=\boldsymbol\Psi[1]/\boldsymbol\Psi[0]=-\tanh\theta$ (09);
- **norm** is the Casimir, $\|\boldsymbol\Psi\|^2=\text{osc}^2=M^2$ (07, §5);
- **shell potential** is the space-component convolution, $V_{\text{grav}}(n)=-\sum_{m<n}\boldsymbol\Psi[1](n{-}m)\,\rho_m$ (spine §5);
- the **half-boost** $\Lambda\to s$ gives the fermion sector (07); the **Wick form** $\Lambda\to\mathsf R$ gives the lepton rotor (04); the **weights** $e^{\mp\theta}$ give thermodynamics (05).

Everything in notes 00–09 is a covariant of the single boost orbit $\boldsymbol\Psi(k)$ that
solves the flat-connection transport equation $\big(\partial_k-\tfrac1\varphi K\big)\boldsymbol\Psi=\big(\partial_k\ln\text{osc}\big)\boldsymbol\Psi$.

## Extension — the golden quantum is a proper length: rapidity = worldline arc length

§3 gave the *tangent* law, $\partial_k\mathbf V=\tfrac1\varphi K\mathbf V$. Integrating its norm
gives the **metric** meaning of the shell quantum. The velocity of the worldline in flow-space
is the constant, **spacelike** vector $\partial_k\mathbf V=\tfrac1\varphi(\sinh\theta,-\cosh\theta)$,
whose Minkowski self-product is fixed for every $k$:

$$\boxed{\;\big\langle\partial_k\mathbf V,\,\partial_k\mathbf V\big\rangle_\eta
=\frac1{\varphi^2}\big(\sinh^2\theta-\cosh^2\theta\big)=-\frac1{\varphi^2}\;}$$

(residual $1.9\times10^{-13}$). The minus sign is mandatory: $\mathbf V$ is a unit *timelike*
vector confined to the upper unit hyperbola $\|\mathbf V\|^2=1$, so its tangent is spacelike,
and the chronon worldline is **not** a flow-space geodesic of proper *time* but the unit-speed
parametrization of a *spacelike* arc — the orbit of the boost through correlation–gravity space.
The hyperbolic arc length accumulated over the ordinal is therefore

$$s(k)=\int_0^{k}\sqrt{\big|\langle\partial_{k'}\mathbf V,\partial_{k'}\mathbf V\rangle_\eta\big|}\;dk'
=\frac{k}{\varphi}=\theta$$

(quadrature vs. closed form, residual $4.4\times10^{-16}$): **rapidity is exactly the hyperbolic
arc length of the chronon worldline**, and one shell is one unit of proper interval

$$s(k{+}1)-s(k)=\frac1\varphi=0.6180339887\quad(\text{constant, every shell}).$$

This is the integral complement to §3 and upgrades "ordinal depth $=$ rapidity" from a *coordinate*
identification to a *geometric* one: the golden quantum $1/\varphi$ is not merely the boost
parameter per shell but the **invariant proper length** the worldline traverses per shell on the
unit hyperbola — the same fixed step whether read as a boost angle (§2), a Noether-conserved
norm (§1), or now a metric arc. The arc-length form makes the boost orbit a constant-speed
geodesic flow on the hyperbola, so the total rapidity banked out to the cosmological horizon shell
$N_\star=291.88$ (note 08) is a finite proper length $\Theta_H=N_\star/\varphi=180.39$ — the
flow-space "size of the observable stack," the bridge from this group to the cosmology branch.

## Prediction

Because $\boldsymbol\Psi$ is **boost-covariant**, any observable built from it must transform
under one of the four reps above — there is no fifth channel. Concretely: ordinal-indexed
data carrying the golden log-period $\Delta k=\pi/(2\ln\varphi)=3.26425$ must appear in
exactly one of (i) weight form $e^{\mp\theta}$ (dissipative, note 05), (ii) velocity form
$\tanh\theta$ (directional, note 09), (iii) half-boost form $\cosh(\theta/2)$ (fermionic,
note 07), or (iv) compact form $\cos(\theta\to i\theta)$ (spectral, note 04) — and the same
$\boldsymbol\Psi$ fixes the relative normalization between channels with **no free parameter**,
since all share the single seed $\mathbf V(0)=(1,0)$ and the single quantum $1/\varphi$. The
sharpest test: the lepton rotor angle $\delta\theta_g$ (compact channel) and the gravitational
non-reciprocity slope $-1/\varphi$ (boost channel) are the *same generator* viewed in the two
real forms, so a measured generation-mixing phase and a measured deep-shell drift bias must be
related by exactly the Wick rotation $\theta\to i\theta$ — a single, parameter-free bridge
between the fermion spectrum (04) and rendering reciprocity (09).
