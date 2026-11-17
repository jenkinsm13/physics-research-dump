# 35a — The Chronogravitational Potential and Field Equation

*Sibling of note 35 (the time=gravity spine): one generator $K$ at rate $1/\varphi$,
eigenvalues $\pm1$; null rays $T=e^{-\theta}$ (time, decaying), $G=e^{+\theta}$ (gravity,
growing); $T\cdot G=1=L_y$; net force $\mathcal F=G-T=2\sinh\theta$; $\beta=\tanh\theta$.
We ask whether that single force descends from **one scalar potential** whose two opposite
gradients are the time and gravity rays. All boxed numbers confirmed in
`verify/verify_chronogravity-potential.py` (exit 0). $\varphi=1.6180339887$,
$1/\varphi=0.6180339887$, $\ln\varphi=0.4812118251$.*

---

## 1. The potential whose gradient is the chronogravitational force

Note 35 isolated the net pull as the *odd*, flow channel $\mathcal F(\theta)=G-T=2\sinh\theta$,
zero only at the now. A conservative force comes from a potential by $\mathcal F=-dU/d\theta$.
The unique (up to constant) primitive is the **even, standing-mode** channel:

$$\boxed{\;U(\theta)=-2\cosh\theta,\qquad -\frac{dU}{d\theta}=2\sinh\theta=G-T=\mathcal F(\theta).\;}$$

Verified exact to machine precision over $\theta\in[-3,3]$ (max residual $8.9\times10^{-16}$).
This is the cleanest possible statement of the spine: $U\propto\cosh$ is the **$G_{\rm sym}$
(symmetric/standing) channel**, its gradient $\propto\sinh$ is the **$G_{\rm flow}$ (gravity)
channel**. Precisely, $U=-2\,G_{\rm sym}^{\rm bare}$ on the bare null amplitudes ($G_{\rm sym}^{\rm bare}=\cosh\theta$,
$G_{\rm flow}^{\rm bare}=\sinh\theta$): the *potential is the standing mode, the force its
gradient* — the same $G_{\rm sym}^2-G_{\rm flow}^2=\mathrm{osc}^2$ split of note 10, now read
as potential-vs-force. The force points **away** from the now ($\mathcal F>0$ for $\theta>0$):
$U$ is a hill, not a well — we develop the sign in §3.

## 2. The two null rays are the $\pm$-gradient eigendirections

The force $\mathcal F=G-T$ is the *difference* of the two rays; the potential $-2\cosh\theta=-(G+T)$
is their *sum*. The rays themselves are singled out by the gradient operator that generates
the force. Acting with $d/d\theta$ on the bare null amplitudes,

$$\boxed{\;\frac{d}{d\theta}\,G(\theta)=+1\cdot G(\theta),\qquad
\frac{d}{d\theta}\,T(\theta)=-1\cdot T(\theta),\;}$$

verified numerically to $<10^{-6}$. The gravity ray $e^{+\theta}$ is the $+1$ eigenfunction of
the gradient; the time ray $e^{-\theta}$ is the $-1$ eigenfunction. These eigenvalues are
**identical to the spectrum of the generator $K$** that note 35 is built on — $K$'s eigenvalues
$\{+1,-1\}$ match the gradient's $\{+1,-1\}$ to machine precision. So "the two opposite gradients
of one potential" is literally true and exact: the time ray and the gravity ray are the two
opposite-sign gradient eigendirections, and the single force $\mathcal F=-U'$ is the imbalance
between them. The diagonalization needs no dressing — it is a property of $e^{\pm\theta}$ alone.

## 3. The hard number: $U''(0)=-2$, and an honest read against the now-Hessian

The curvature of the potential at the now is the single hardest number here:

$$\boxed{\;U''(0)=-2\cosh 0=-2\quad(\text{exact; numeric }-2.0000000).\;}$$

**$U''(0)<0$ means the now is a *maximum* of $U$ — an unstable hilltop.** The force
$-U'=2\sinh\theta$ points away from $\theta=0$ in both directions, so along any worldline
running off the now ($\theta=k/\varphi$ increasing forward, §5) the imbalance *grows*
toward the horizon: the present is the watershed, and every worldline leaves it for
ever-deeper gravity (growing $G$). This is the correct sign — the spine's "imbalance grows
as $2\sinh\theta$, saturating at the horizon."

Now the honest comparison the audit demands. Note 14's now-Hessian carries the **dressed**
amplitude curvature $G_{\rm sym}''(0)\big|_k=2\ln^2\varphi+\tfrac1{2\varphi^2}=+0.654113$ —
a **minimum**. These have **opposite sign**, and they *must*: by definition $U=-2\,G_{\rm sym}^{\rm bare}$,
so $U$'s maximum is the amplitude's minimum, flipped by the factor $-2$. The two are the
**same $\cosh$ backbone, sign-reversed by the defining relation** — not an independent
agreement, and *we do not equate the two curvatures*. Two further honesty notes: (i) note 14
differentiates in the shell label $k$, while $U$ is in rapidity $\theta=k/\varphi$, so the
two also differ by the dressing and by $d\theta/dk=1/\varphi$. The clean **stripped**
comparison, both in $\theta$, is the rapidity part of $G_{\rm sym}''$, namely
$\mathrm{osc}(0)\cdot\cosh''(0)=\tfrac12$ (the $+\tfrac12$ of note 14's curvature triple
$(\tfrac12,-1,-\tfrac89)$), against $U''(0)=-2$; their ratio $-4$ is just the $-2$
normalization times the sign and carries no deeper meaning. The genuine content is the
**sign opposition**, which is exactly what "potential vs amplitude" predicts.

## 4. $V_{\rm grav}$ is the discretized *gradient* of $U$, not $U$ itself

Note 16 §5 derived the static gravity potential as the field equation's zero-mode Green's
function, $V_{\rm grav}(n)=\sum_{m<n}\sinh\!\big((n{-}m)/\varphi\big)\big/\big(1+\cos^2(2(n{-}m)\ln\varphi)\big)\,\rho_m$.
Its kernel is $\propto\sinh$, not $\cosh$ — so $V_{\rm grav}$ is **not** the shell-discretized
$U$. It is the osc-dressed, source-convolved **gradient** of $U$:

$$\boxed{\;\frac{\sinh\!\big(d/\varphi\big)}{1+\cos^2\!\big(2d\ln\varphi\big)}
=\mathrm{osc}(d)\cdot\Big(\!-\tfrac12 U'(d/\varphi)\Big),\qquad d=n-m,\;}$$

verified exact ($0.0$ residual over $d=1,2,3,5,8,13$), since $-\tfrac12U'(x)=\sinh x$. The
static gravitational potential of the field theory is the chronon-density convolution of the
**force-field** $-\tfrac12U'$ dressed by the flow-reversal lattice $\mathrm{osc}$ — exactly
the advanced-dominated *growing* $\sinh$ combination of note 16. (Sanity: $|\sinh(3/\varphi)-\cosh(3/\varphi)|=0.157\neq0$,
so $\sinh\neq\cosh$ and the distinction is real.) The shell-discretized object of note 16 is
the gradient of the rapidity potential of this note, convolved with sources — the two notes lock.

## 5. Equation of motion and the boost rate

A test chronon's worldline is $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$.
Its time component obeys

$$\boxed{\;\frac{dV_0}{dk}=\frac1\varphi\sinh\theta=\frac1{2\varphi}\,\mathcal F(\theta),\;}$$

verified to $6.5\times10^{-10}$. The $k$-gradient of the time component is the chronogravitational
force divided by $2\varphi$ — the potential's gradient drives the worldline. **Honest framing of
the boost rate:** the $1/\varphi$ here is the boost *connection* of note 10 (the input that
$\theta=k/\varphi$), not something $U$ derives; the flow is uniform-boost at $1/\varphi$ per shell
*by construction*, and what $U$ supplies is that its gradient reproduces the net force $2\sinh\theta$
exactly along that flow. So the EOM is consistent with — does not independently re-derive — the
$1/\varphi$ rate, with the exact bridge $dV_0/dk=(1/\varphi)\sinh\theta$.

## 6. The apex value and the LIGO bracket

The potential at one shell down is $U(1/\varphi)=-2\cosh(1/\varphi)=-2.39428$ (below the
apex $U(0)=-2$, since $U$ is a hill — §1, §3), and $-U=G+T=2\cosh\theta$
is the *sum* of the two rays — the total chronogravitational "mass" $G+T$, of which the force
$\mathcal F=G-T$ is the imbalance. So the boost velocity reads off the potential channel cleanly:

$$\beta(\theta)=\frac{\mathcal F}{-U}=\frac{G-T}{G+T}=\tanh\theta,\qquad
\beta(1/\varphi)=\frac{2\sinh(1/\varphi)}{2\cosh(1/\varphi)}=0.5498,$$

verified $=\tanh(1/\varphi)$ to $10^{-13}$. **Comparison, even-handed:** this $0.5498$ is the
note-15 first-shell flow fraction $f(1)$, compared against the **corpus LIGO re-analysis**
ringdown timing ratio $t_1/t_2=0.548$ — a $0.32\%$ deviation (matching note 15's own figure;
$40\times$ closer than the naïve $1/\varphi=0.618$, which sits $12.8\%$ off and misreads $\beta$
as a rapidity). This is a sub-percent bracket, **not** an exact hit, and three honesty caveats
fix exactly what it does and does not claim:

1. **The value is parameter-free but the shell is discrete.** $\beta(1/\varphi)=\tanh(1/\varphi)$
   carries *no continuous* tunable constant — it is fixed once $1/\varphi$ is the boost connection
   (note 10). But the match selects the integer shell $n=1$: $\beta(n/\varphi)=\tanh(n/\varphi)$
   gives $0$ at $n=0$, $0.5498$ at $n=1$, $0.844$ at $n=2$, so only $n=1$ lands near $0.548$. That
   discrete selection is **not** arbitrary fitting — note 15 §6 anchors $n=1$ structurally as the
   *fundamental echo leg* / first-shell boost velocity of the ringdown ladder — but it is a discrete
   integer choice and must be disclosed, not hidden behind "not a free parameter."

2. **The target is the corpus's own re-analysis, not a published LIGO observable.** The $0.548$ is
   the corpus LIGO paper's phase-transition timing ratio $t_1/t_2$ (note 15 §6), a framework
   re-reading of the strain — not an independently established LIGO number. The agreement is
   internal-corpus-to-corpus at the headline level; we do not claim to have reproduced a value the
   LIGO collaboration reports.

3. **The residual is sub-percent, comparable to the corpus's absorber-incompleteness corrections —
   not identified with note 13's specific budget.** Note 13 derives a $0.3\%$ correction to the
   *static gravity exponent* $\nu$ ($\nu_{\rm eff}=1.00297$, Newton to three parts in a thousand),
   a different observable from a ringdown timing ratio. The honest statement is that $0.32\%$ is the
   same *order* as the framework's known absorber-completeness corrections, not that it *is* note
   13's number; no $\sim1\%$ budget is asserted in note 13, and we do not borrow one here.

## Extension — the potential–force invariant $U^2-\mathcal F^2=4\,L_y$

The reciprocal law of the spine (note 35) is stated on the rays: $T\cdot G=1=L_y$, identically.
Notes 35 §"imbalance" and §"reciprocal" give the force as the difference $\mathcal F=G-T$ and the
potential magnitude as the sum $-U=G+T$. These two combinations are not independent — they are
constrained by the *same* unit invariant, now written purely in the potential and the force:

$$\boxed{\;U(\theta)^2-\mathcal F(\theta)^2=(G{+}T)^2-(G{-}T)^2=4\,G\,T=4\,L_y=4\quad\text{(exact, all }\theta).\;}$$

Verified to machine precision ($\max|U^2-\mathcal F^2-4|=1.1\times10^{-13}$ over $\theta\in[-3,3]$).
This is the *potential–force form* of the reciprocal law: it says the chronon worldline moves on a
fixed **hyperbola** in the $(\mathcal F,-U)$ plane,

$$(-U)^2-\mathcal F^2=4,\qquad -U=2\cosh\theta\ (\text{semi-major axis }2),\ \ \mathcal F=2\sinh\theta,$$

i.e. the potential-sum and force-difference are the $\cosh$/$\sinh$ legs of one rapidity rotation,
their squared difference pinned at $4=4L_y$. Three locks follow, each already implicit in the corpus
and now made one identity:

- **Lock to §1–§2.** $U=-2G_{\rm sym}^{\rm bare}=-2\cosh\theta$ and $\mathcal F=-U'=2G_{\rm flow}^{\rm bare}=2\sinh\theta$
  obey $U^2-\mathcal F^2=4(\cosh^2-\sinh^2)=4$ — the *bare* (osc-stripped) reading of the spine's
  $M^2=G_{\rm sym}^2-G_{\rm flow}^2=\mathrm{osc}^2$: on the undressed (bare) null amplitudes the
  osc dressing is stripped, so the invariant collapses to the pure unit $1$ (times the normalization $4$).
  The potential is the standing leg, the force the flow leg, of *one* invariant hyperbola.

- **Lock to the boost.** Dividing the two legs returns §6 with no new input:
  $\beta=\mathcal F/(-U)=\tanh\theta$ is the *slope* on the invariant hyperbola, and the invariant
  $U^2-\mathcal F^2=4$ is exactly the statement $1-\beta^2=4/U^2=1/\cosh^2\theta=\operatorname{sech}^2\theta$
  — the Lorentz $\gamma$-factor in disguise: $-U=2\cosh\theta=2\gamma$, $\mathcal F=2\sinh\theta=2\beta\gamma$.
  The potential magnitude *is* twice the boost $\gamma$-factor; the force *is* twice $\beta\gamma$.

- **No new claim, no inner product needed.** This is a purely algebraic identity among the bare null
  amplitudes — it makes **no** energy or stability assertion, so the non-Hermitian-operator caveat
  of the corpus is not engaged. It is the reciprocal law $L_y=1$ re-expressed in the variables this
  note introduced, and nothing more.

A clean falsifier rides along: if a measured $(\mathcal F,-U)$ pair ever left the hyperbola
$U^2-\mathcal F^2=4$ — equivalently if $1-\beta^2\neq\operatorname{sech}^2\theta$ at any shell — the
single-potential/single-force structure (and with it $T\cdot G=1$) would break.

## Verdict

The single chronogravitational force $\mathcal F=2\sinh\theta$ **does** descend from one scalar
potential, $U(\theta)=-2\cosh\theta=-2\,G_{\rm sym}^{\rm bare}$, whose two opposite gradient
eigendirections are exactly the time ray ($-1$) and gravity ray ($+1$) — the same $\pm1$ spectrum
as the generator $K$. The hard number is $U''(0)=-2$ (exact): the now is an unstable *maximum* of
$U$, sign-opposite to the note-14 dressed-amplitude *minimum* $+0.654113$ by the defining factor
$-2$ (reported as opposition, not equated). $V_{\rm grav}$ (note 16 §5) is the osc-dressed,
source-convolved **gradient** $-\tfrac12U'$, not $U$ — verified exact. The EOM gives
$dV_0/dk=(1/\varphi)\sinh\theta=\mathcal F/2\varphi$, consistent with (not re-deriving) the
$1/\varphi$ boost connection. The redshift ratio $\beta(1/\varphi)=\tanh(1/\varphi)=0.5498$ sits
$0.32\%$ off the **corpus LIGO re-analysis** ratio $0.548$ — a sub-percent bracket, not a forced
fit; parameter-free in value, but selecting the structurally-motivated discrete shell $n=1$ (§6),
and compared corpus-to-corpus rather than against an independently established LIGO observable.

**Falsifier:** if the static gravity zero-mode of note 16 were found to be $\propto\cosh$ (i.e.
$V_{\rm grav}$ *were* the discretized $U$ rather than its $\sinh$ gradient), or if a localized
now-probe showed the present to be a potential *minimum* ($U''(0)>0$, a stable well rather than
the unstable hilltop $U''(0)=-2$), the single-potential structure $\mathcal F=-U'$ with
$U=-2\cosh\theta$ is falsified.
