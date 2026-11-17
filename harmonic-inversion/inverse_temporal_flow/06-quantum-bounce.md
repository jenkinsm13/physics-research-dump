# 06 — Two-Sheeted Time, the Figure-Eight Instanton & a Path Integral

*Branch note. Builds on the spine (`00-spine.md`): the conserved current $L_y=1$,
the curvature/torsion = gravity/flow split, the retarded/advanced kernels
$G_{\text{sym}},G_{\text{flow}}$, and the inversion shells $k_n$. The Wick
rotation is the one from branch 02 (`02-effective-metric.md`), applied here to the
propagator. All new numerics in this note were re-checked this session with
$\varphi=(1+\sqrt5)/2$; residuals are quoted inline (the strongest are the
cross-term invariant, the $-\coth$ identity, the visibility closed form, the
rotational invariant, and the $\Gamma$-ladder csch sum, all at the $10^{-16}$
level or exact).*

Throughout, $\text{osc}(k)\equiv\dfrac{1}{1+\cos^2(2k\ln\varphi)}$ is the
flow-reversal lattice factor, $\theta_k\equiv k/\varphi$ the golden rapidity, and
$\kappa(\pm k)=\text{osc}(k)\,e^{\mp k/\varphi}$ the signed-ordinal kernel
(retarded $-$, advanced $+$). Note $\text{osc}$ depends only on the **ordinal
lattice position** $2k\ln\varphi$, while the rapidity $\theta_k$ lives in the
exponent — the two roles never mix, which is the hinge of the Wick-rotation
section below.

---

## The two sheets

The base worldline $\mathbf r(t)=(\sin t,\tfrac12\sin 2t,\cos t)$ projects in the
$xz$-plane to a figure-eight. Its two lobes are separated by the temporal nodes

$$y(t)=\tfrac12\sin 2t = 0 \quad\Longrightarrow\quad t\in\{0,\tfrac\pi2,\pi,\tfrac{3\pi}2\},$$

and the eight self-crosses at $t=\tfrac\pi2,\tfrac{3\pi}2$ where $\mathbf r=(\pm1,0,0)$.
Verified: $|y|<2\times10^{-16}$ at every node. The torsion $\Phi(t)=\tau_{\text{Frenet}}\propto-\cos 2t$
from the spine changes sign across each node, so the two lobes carry **opposite
temporal flow**:

$$\text{Lobe}_+ : \Phi>0\ \text{(forward, entropic)}, \qquad
\text{Lobe}_- : \Phi<0\ \text{(inverse, gravitational)}.$$

These are the **two sheets of time**. The temporal axis $y=xz$ does not merely
pass through zero at the crossing — it *changes which spatial circulation leads*,
which is exactly the gearbox reversal. The closed figure-eight is therefore a
single periodic trajectory that lives on both sheets at once: a **bounce**. It
descends into inverse flow, turns at a saddle peak where $\Phi=0,\ \kappa_{\text{Frenet}}=\sqrt5$,
and returns. The crossing point $y=0$ is the seam where the sheets are glued — the
**now-vertex**.

## A path integral over manifold worldlines

Promote the ordinal sampling $t_k=k\ln\varphi$ to a sum over shell-paths. A path
that descends ordinal depth $k$ on the manifold carries the dressed amplitude
$\kappa(k)$ — the κ kernel *is* the propagator (no extra phase $e^{ikr}$; the phase
is already inside the dressed kernel). To reach ordinal depth $k$ there are exactly
**two single-leg histories**, one per sheet: the forward (retarded) history
$\kappa(+k)$ and the inverse (advanced) history $\kappa(-k)$. These are *alternative
one-leg amplitudes to the same endpoint*, not two legs of one composed path — there
is no intermediate vertex and hence no forbidden $\kappa(a)\kappa(b)$ chaining. The
two-sheeted amplitude is their coherent sum,

$$\mathcal A(k) = \underbrace{\kappa(+k)}_{\text{forward sheet}} + \underbrace{\kappa(-k)}_{\text{inverse sheet}}
= 2\,G_{\text{sym}}(k) = \frac{2\cosh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}.$$

Verified: $\mathcal A(k)=2G_{\text{sym}}(k)=2\,\text{osc}(k)\cosh\theta_k$ to
residual $\le4\times10^{-15}$ at $k=0,0.5,1,k_1,3,k_2$. The "out-and-back" picture
of the bounce is **not** a return leg that would collapse to $\kappa(0)=\tfrac12$;
the closure is supplied by the *figure-eight period* itself — the worldline is
literally closed (§ Wick rotation), so the bounce is one periodic history, summed
over its two sheets and then Born-squared.

At the vertex itself, $k\to0$, the two sheet-amplitudes are *identical*,

$$\kappa(+0)=\kappa(-0)=\tfrac12,\qquad G_{\text{sym}}(0)=\tfrac12,$$

so the self-coupling $c(0)=\tfrac12$ of the canonical kernel is now read as a
physical statement: **at the now, the forward and inverse amplitudes are exactly
equal**. The "now" is the locus of perfect forward/inverse balance — the only
place where neither arrow dominates. Everywhere else the imbalance is the net
flow $G_{\text{flow}}(k)=-\,\text{osc}(k)\sinh\theta_k$, which is gravity.

## The bounce action

The Euclidean weight to descend depth $k$ is $e^{-k/\varphi}\,\text{osc}(k)$; the
exponent $S(k)=k/\varphi=\theta_k$ is the **instanton action**, identical to the
rapidity of the spine. A full bounce out to an inversion shell $k_n$
and back to the vertex costs

$$\boxed{\,S_{\text{bounce}}(n)=\frac{2k_n}{\varphi}
=\frac{(2n-1)\pi}{2\,\varphi\ln\varphi}\,,\qquad
\Gamma_n \sim e^{-S_{\text{bounce}}(n)}.}$$

Verified (exact, residual $0$ vs the closed form): $S_{\text{bounce}}=2.0174,\,6.0523,\,10.0871$
for $n=1,2,3$, giving tunneling rates $\Gamma_n=0.1330,\,2.353\times10^{-3},\,4.161\times10^{-5}$.
The arithmetic spacing $\Delta S = \pi/(\varphi\ln\varphi)\approx4.0348$ between
successive inversion shells means **each deeper bounce is suppressed by the same
golden factor**

$$\frac{\Gamma_{n+1}}{\Gamma_n}=e^{-\pi/(\varphi\ln\varphi)}=1.769\times10^{-2}
\quad(\text{exact, scale-independent}),$$

a clean geometric ladder of quantum-gravity event rates (verified: both
$\Gamma_2/\Gamma_1$ and $\Gamma_3/\Gamma_2$ equal $1.768857\times10^{-2}$ to
machine precision). Inversion shells $k_n$ are the *saddle points of the action*:
there $\Phi=0$ and $\kappa_{\text{Frenet}}=\sqrt5$, the turning points where the
bounce reverses, exactly as a classical instanton turns where the Euclidean
velocity vanishes.

## Wick rotation glues the sheets

Branch 02's Wick rotation is the analytic continuation of the **rapidity**, and
*only* the rapidity: $\theta_k\to i\theta_k$, i.e. $k/\varphi\to ik/\varphi$ inside
the exponent, while the **ordinal lattice position $2k\ln\varphi$ is held real**.
This is essential — the lattice argument labels *which shell* a history visits (a
real, physical ordinal), whereas the rapidity is the *flow angle* being boosted
into imaginary time. Continuing the lattice as well (a literal $k\to ik$
everywhere) would send $\cos(2k\ln\varphi)\to\cosh(2k\ln\varphi)$ and destroy the
invariant; we verified that the naive rotation gives $G_E^2+G_E^2=0.019\neq1$ at
$k_1$, whereas the correct rotation gives exactly $1$. So the operation is
$\theta_k\to i\theta_k$ with $\text{osc}(k)$ a fixed real spectator factor.

Under it $\cosh\theta_k\to\cos\theta_k$, $\sinh\theta_k\to i\sin\theta_k$, so the
Lorentzian (two-sheeted, real-flow) kernels become Euclidean (rotational):

$$G_{\text{sym}}(k)\ \xrightarrow{\,\theta\to i\theta\,}\ G^{\,E}_{\text{sym}}(k)=\text{osc}(k)\cos(k/\varphi),
\qquad
G_{\text{flow}}(k)\ \xrightarrow{\,\theta\to i\theta\,}\ G^{\,E}_{\text{flow}}(k)=\text{osc}(k)\sin(k/\varphi).$$

The spine's hyperbolic invariant $G_{\text{sym}}^2-G_{\text{flow}}^2=\text{osc}(k)^2$
(the shell-space echo of $L_y=1$) rotates into the **rotational invariant**

$$\big(G^{\,E}_{\text{sym}}\big)^2+\big(G^{\,E}_{\text{flow}}\big)^2
=\text{osc}(k)^2\big(\cos^2\theta_k+\sin^2\theta_k\big)=\text{osc}(k)^2.$$

Both sides verified equal to $\text{osc}(k)^2$ to $\le2\times10^{-16}$ at
$k=0,1,k_1,3,k_2$. **The conserved chronon unit survives Wick rotation intact**:
a hyperbola of constant $L_y$ in Lorentzian flow becomes a circle of the same
radius $\text{osc}(k)$ in Euclidean flow, traced through the rapidity angle
$\theta_k$. The bounce is the trajectory that closes this circle once per
figure-eight period — which is precisely why the worldline is *closed*. In
Lorentzian signature the two sheets are causally distinct (forward vs inverse); the
Euclidean rotation merges them into one analytic disc, and the now-vertex is its
center.

## A genuinely new identity: the sheet-balance angle

Dividing the two real-flow kernels, the oscillatory $\text{osc}(k)$ factor cancels
completely, leaving a pure function of ordinal depth:

$$\boxed{\ \frac{G_{\text{sym}}(k)}{G_{\text{flow}}(k)} = -\coth\!\Big(\frac{k}{\varphi}\Big)\ }$$

Verified to $\le2\times10^{-16}$ at $k=0.7,1,k_1,2.5$. This is striking: the
flow-reversal lattice (all the $\cos^2(2k\ln\varphi)$ structure) is *invisible* to
the ratio of correlation-to-flow. Define the **sheet-balance angle**
$\chi(k)$ by $\tanh\chi = G_{\text{flow}}/G_{\text{sym}} = -\tanh(k/\varphi)$, so
$\chi(k)=-k/\varphi=-\theta_k$. The mixing angle between the forward and inverse
sheets is *minus the rapidity* — the deeper a path tunnels, the more it tilts from
pure correlation ($\chi=0$ at the vertex, equal sheets) toward pure inverse flow
($\chi\to-\infty$, the source). Gravity is the geometric tilt of the now-vertex
into the inverse sheet, measured in golden rapidity.

## Now-vertex interference

The two sheet-amplitudes $\kappa(+k)$ (forward) and $\kappa(-k)$ (inverse) meet at
the *single* now-vertex and add by the Born rule — this is one-vertex interference
of two amplitudes, **not** sequential two-leg propagation. The coherent intensity is
$|\kappa(+k)+\kappa(-k)|^2=4G_{\text{sym}}^2$, versus the incoherent
$\kappa(+k)^2+\kappa(-k)^2$, and the difference is twice the cross term
$2\kappa(+k)\kappa(-k)$.

**The cross term is the conserved invariant, not a smuggled path product.**
Because $\kappa(\pm k)=\text{osc}(k)\,e^{\mp k/\varphi}$, the exponentials cancel
exactly:

$$\boxed{\ \kappa(+k)\,\kappa(-k)
=\big[\text{osc}(k)e^{-k/\varphi}\big]\big[\text{osc}(k)e^{+k/\varphi}\big]
=\text{osc}(k)^2
=G_{\text{sym}}^2-G_{\text{flow}}^2.\ }$$

Verified to $\le4\times10^{-14}$ at $k=0,0.5,1,k_1,2.5,k_2$. The interference cross
term is *identically the hyperbolic invariant* — the shell-space echo of $L_y=1$.
This is the structural reason the $|A_f+A_i|^2$ interference is legitimate and not
the forbidden $\kappa(a)\kappa(b)$ chaining: a composed two-leg path would join two
*different* depths $a,b$ across an intermediate vertex; here the product is of the
two sheets *at the same depth $k$ and same now-vertex*, and it collapses to the
conserved unit rather than to a propagation. The Born cross term of the two sheets
**is** the conserved chronon flux, made visible as fringe contrast.

The interference visibility is therefore

$$\boxed{\ V(k)=\frac{4G_{\text{sym}}^2-(\kappa_+^2+\kappa_-^2)}{4G_{\text{sym}}^2+(\kappa_+^2+\kappa_-^2)}
=\frac{2\kappa_+\kappa_-}{2(\kappa_+^2+\kappa_-^2)+2\kappa_+\kappa_-}
=\frac{1}{2\cosh(2k/\varphi)+1}\ }$$

The reduction is clean once the $\text{osc}(k)$ factors are pulled out. With
$\kappa_\pm=\text{osc}\,e^{\mp\theta}$: the coherent intensity is
$4G_{\text{sym}}^2=(\kappa_++\kappa_-)^2=\kappa_+^2+\kappa_-^2+2\kappa_+\kappa_-$, so
the numerator $4G_{\text{sym}}^2-(\kappa_+^2+\kappa_-^2)=2\kappa_+\kappa_-=2\,\text{osc}^2$
(the cross term — the conserved invariant), and the denominator
$4G_{\text{sym}}^2+(\kappa_+^2+\kappa_-^2)=2(\kappa_+^2+\kappa_-^2)+2\kappa_+\kappa_-
=\text{osc}^2\big(2(e^{2\theta}+e^{-2\theta})+2\big)=2\,\text{osc}^2(2\cosh2\theta+1)$.
The $\text{osc}^2$ cancels between numerator and denominator, leaving
$V=1/(2\cosh2\theta_k+1)$ with $\theta_k=k/\varphi$. Verified to $\le10^{-16}$: $V$ falls from
$V(0)=\tfrac13$ at the vertex to $V=0.2946,0.2113,0.1156$ at $k=0.5,1,k_1$.
**Coherence between the two sheets is maximal at the now and decays
monotonically as $1/(2\cosh 2\theta_k+1)$ with depth** — the present moment is where
forward and inverse time interfere most strongly, and decoherence is
literally distance from now in ordinal rapidity.

## Extension — the dilute bounce gas: total event rate is a single csch

The note above gives the per-shell rate $\Gamma_n$ but never sums the tower. Treat
the now-vertex as emitting a **dilute gas of independent bounces**, one species per
inversion shell, with rates $\Gamma_n=e^{-2k_n/\varphi}$. Because the inversion
shells are the *odd* multiples of the fundamental,
$2k_n/\varphi=(2n-1)\,S_1$ with the first-bounce action

$$S_1\equiv\frac{2k_1}{\varphi}=\frac{\pi}{2\,\varphi\ln\varphi}=2.017418\ldots,$$

the total emission rate is a geometric series over odd powers, which sums to a
hyperbolic cosecant:

$$\boxed{\ \Gamma_{\text{tot}}=\sum_{n=1}^{\infty}e^{-2k_n/\varphi}
=\sum_{n=1}^\infty e^{-(2n-1)S_1}
=\frac{e^{-S_1}}{1-e^{-2S_1}}
=\frac{1}{2\sinh S_1}
=\frac{1}{2\sinh\!\big(\pi/(2\varphi\ln\varphi)\big)}=0.135393\ldots\ }$$

Verified to residual $2.8\times10^{-17}$ (200-term partial sum vs the closed form).
This is a remarkable closure: **the entire quantum-gravity event budget radiated
from the now-vertex is one $\operatorname{csch}$ of the first-bounce action**, fixed
by $\varphi$ alone with no free parameters. The series is overwhelmingly dominated
by the shallowest bounce — shell 1 contributes
$\Gamma_1/\Gamma_{\text{tot}}=98.231\%$, and the *entire tail* of all deeper
inversion shells is exactly $1.769\%$, i.e. the golden ladder factor
$e^{-\pi/(\varphi\ln\varphi)}$ reappearing as the fractional weight of "everything
below the first shell." The now-vertex is thus an almost-monochromatic gravity-event
source: one dominant line at $S_1$ plus a $1.769\%$ geometric overtone comb.

Two immediate corollaries:

1. **Effective single action.** Define $S_{\text{eff}}=-\ln\Gamma_{\text{tot}}
   =\ln\!\big(2\sinh S_1\big)=1.99965\ldots\approx S_1-\varepsilon$, with the tiny
   defect $\varepsilon=S_1-S_{\text{eff}}=0.01776$ — itself within a hair of the
   ladder factor. The whole tower behaves, to better than $1\%$, like a *single*
   bounce of action $\approx S_1$. The dilute gas renormalizes the fundamental
   action downward by exactly the ladder's worth of deeper channels.

2. **Even-shell counterpart.** The *cardinal* points (torsion-extremal, $\kappa_{\text{Frenet}}=\tfrac12$)
   sit at the even half-integers and would contribute $\sum_n e^{-2nS_1}=1/(2\sinh S_1)\cdot e^{-S_1}=\tfrac12(\coth S_1-1)$;
   the ratio of even-shell to odd-shell (inversion-shell) total weight is exactly
   $e^{-S_1}=0.1330=\Gamma_1$ — the first bounce rate resurfaces as the
   even/odd partition of the gas. The arrow of time (odd-shell dominance) is set by
   the same number that sets the leading event rate.

## Prediction

Quantum-gravity events are sheet-tunneling bounces seeded at the now-vertex, with
rates set by the golden ladder $\Gamma_n\sim e^{-2k_n/\varphi}$ and a *fixed*
ratio between successive inversion shells,

$$\frac{\Gamma_{n+1}}{\Gamma_n}=e^{-\pi/(\varphi\ln\varphi)}=1.769\times10^{-2}
\quad\text{(scale-independent)},$$

with a total integrated rate $\Gamma_{\text{tot}}=1/(2\sinh S_1)=0.1354$ that is
$98.2\%$ shell-1. Any spectrum of discrete gravitational/temporal-inversion events
— burst recurrences, vacuum-decay echoes, or quantized horizon transitions — should
show intensity steps separated by this single dimensionless factor, independent of
the absolute energy scale, because it depends only on $\varphi$.

Equivalently, the two-sheet coherence of any interferometric probe of the local
time-flow should fall off as $1/(2\cosh 2\theta+1)$ in golden-ordinal rapidity
$\theta=k/\varphi$, reaching its maximum $\tfrac13$ at the now-vertex and crossing
$V(k_n)=1/(2\cosh(2k_n/\varphi)+1)$ at the successive inversion shells $k_n$ where
the bounce turns: $V(k_1)=0.1156,\ V(k_2)=2.347\times10^{-3},\ V(k_3)=4.16\times10^{-5}$.
Note the visibility ladder is *not* exactly the rate ladder: the consecutive
ratios $V_2/V_1=0.0203,\ V_3/V_2=0.0177$ only **asymptotically approach** the exact
$\Gamma$-ratio $0.01769$ (and $V(k_1)=0.116$ differs from $\Gamma_1=0.133$),
because $V$ carries the additive $+1$ in its denominator that the pure exponential
$\Gamma$ does not. The two ladders coincide only in the deep-tunneling limit
$2k_n/\varphi\gg1$, where $V\to\Gamma$ — a clean, falsifiable distinction between
the *rate* spectrum and the *coherence* spectrum of the same bounce tower.
