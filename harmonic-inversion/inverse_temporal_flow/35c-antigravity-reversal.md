# 35c — Anti-Gravity as Reversed Eigenvalue, and What the Reciprocal Law Permits

*Building on the note-35 spine: one generator $\partial_k\mathbf V=\frac1\varphi K\mathbf V$,
$K^2=I$, eigenvalues exactly $\pm1$; the two null rays $T(\theta)=e^{-\theta}$ (time, eigenvalue
$-1$, decaying) and $G(\theta)=e^{+\theta}$ (gravity, eigenvalue $+1$, growing); the reciprocal
law $T\cdot G=1=L_y$; net force $\mathcal F=G-T=2\sinh\theta$; boost $\beta=\tanh\theta$. The
question — is anti-gravity literally running $K$ the other way? — is open thread 35(c). All
numbers below confirmed in `verify/verify_antigravity-reversal.py` (exit 0). This is the most
speculation-prone thread; I separate what the **algebra forces** from what is **interpretation**.*

---

## 1. What the algebra forces: the sign of the force is the sign of $\theta$

The net chronogravitational force is the imbalance between the two eigenrays,
$$\mathcal F(\theta)=G(\theta)-T(\theta)=e^{+\theta}-e^{-\theta}=2\sinh\theta.$$
$\sinh$ is **odd and strictly monotone**, so two facts are forced with no interpretive freedom:
$$\operatorname{sign}\mathcal F(\theta)=\operatorname{sign}\theta,\qquad
\mathcal F(\theta)=0 \iff \theta=0.$$
For $\theta>0$ the gravity ray dominates ($G>T$): **attraction**. For $\theta<0$ the time ray
dominates ($T>G$): $\mathcal F<0$, **repulsion** — structurally, *anti-gravity is the $\theta<0$
branch, where the $-1$ ($T$, time) eigendirection out-weighs the $+1$ ($G$, gravity)
eigendirection in the net imbalance $\mathcal F=G-T$.* The spectrum of $K$ stays $\pm1$ on both
branches — nothing is "reversed" in $K$ itself; what reverses is **which eigendirection wins**.
The hard number: there is exactly **one** place the force changes sign, $\theta=0$,
the now — the time-reversal fixed point of note 14. (Verified: on a $2\times10^5$-point grid over
$[-6,6]$ the only zero of $2\sinh\theta$ is at the origin.) Anti-gravity is not forbidden by the
spine; it is simply *the other side of the now.*

The mirror is exact. One shell into the time side, $\theta=-1/\varphi$:
$$\mathcal F(-1/\varphi)=2\sinh(-1/\varphi)=-1.31627=-\mathcal F(+1/\varphi),\qquad
\beta(-1/\varphi)=\tanh(-1/\varphi)=-0.5498.$$
The repulsion one golden shell into the time-dominant side has **exactly the magnitude** of the
attraction one golden shell into the gravity-dominant side — and $|\beta|=0.5498$ is the very
ratio that reproduced the note-15 LIGO ringdown, now carrying a minus sign. Repulsion is not a
weak afterthought; it is attraction's reflection.

## 2. Is $\theta<0$ physical, or the time-reverse of $\theta>0$? (CPT-like)

The reflection $\theta\to-\theta$ acts on the null rays by **swapping them exactly**:
$$T(-\theta)=e^{+\theta}=G(\theta),\qquad G(-\theta)=e^{-\theta}=T(\theta),\qquad
\mathcal F\to-\mathcal F,\quad \beta\to-\beta.$$
(Verified to $10^{-12}$ for all tested $\theta$.) So the anti-gravity branch is **not a new
substance or exotic material**: it is the gravity branch with the roles of the time and gravity
rays interchanged — the configuration reflected through the now-surface, the $T$-fixed point.
This is the framework's CPT-like statement: the advanced (growing $e^{+\theta}$) and retarded
(decaying $e^{-\theta}$) branches are mirror images across $\theta=0$, and *repulsion is the
retarded/time ray dominating exactly where attraction had the advanced/gravity ray dominating.*
"Running the eigenvalue the other way" is literally reflecting across the now.

## 3. What the reciprocal law actually forbids: shielding, not repulsion

The crucial honest point. One might guess $T\cdot G=1$ *forbids* sustained anti-gravity. It does
not: the reciprocal law holds **identically on the $\theta<0$ side as well** —
$$T(\theta)\,G(\theta)=e^{-\theta}e^{+\theta}=1\quad\text{for all }\theta\ \text{(verified for }
\theta=-5,-2,-1/\varphi,-0.5,-0.1\text{).}$$
What the law forbids is something different and sharper: **gravity shielding at fixed clock rate.**
Because $T=1/G$ rigidly, you cannot lower the gravity amplitude $G$ below unity *without* the time
amplitude $T$ rising by the reciprocal amount. Suppressing gravity,
$$G\to 0\;\Longleftrightarrow\;T=\frac1G\to+\infty\;\Longleftrightarrow\;\theta=\ln G\to-\infty,$$
drives the system to the **anti-horizon limit** $\beta\to-1$ (verified
$\beta(-20)=-1.000000$): the clock runs away unboundedly. Concretely, attenuating $G$ to $0.1$
*forces* $T=10$ ($\theta=\ln0.1=-2.303$); to $10^{-3}$ forces $T=10^3$. There is therefore **no
local anti-gravity device** in the naive sense — no configuration that cancels $G$ while clocks
inside keep ticking at the ambient rate. Repulsion is permitted; *free* repulsion is not. The
price of every unit of $G$ you suppress is an equal unit of time-rate you must accept. This is the
energy-condition analogue the spine has been pointing at: the cost of anti-gravity is paid in
time, one-for-one, by the same conserved $L_y=1$.

## 4. Cosmic acceleration: a structural analog, **not** a literal $\theta<0$ (Q3, handled honestly)

It is tempting — and *wrong* — to say cosmic acceleration is the time ray winning at the horizon,
i.e. $\theta<0$ at cosmological scales. The framework's own bookkeeping forbids this conflation.
Note 21 identifies the scale factor with the boost orbit, $a(N)=a_0\varphi^N$, and the
Planck$\to$Hubble traversal banks a **large positive** cumulative scale-rapidity
$$\Theta_H=N_\star/\varphi=180.39\quad(N_\star=291.88),$$
deep on the **gravity-dominant** side, $\beta\to+1$. The note-35 $\theta$ is the *local* force
direction into a well; note-21's $\Theta$ is the *cumulative* scale-rapidity Planck$\to$Hubble.
They are different coordinates, and $\Theta_H=+180$ is the opposite sign of the naive guess.

The honest mapping: the cosmological analog of the now ($\theta=0$, zero net force) is the
**de Sitter balance $w=-1$** — the equation of state at which the cosmic flow neither decelerates
nor super-accelerates. Acceleration is a small **offset** from that balance, set by the horizon
phase (note 21):
$$\Phi_{\rm res}=-\cos(2N_\star\ln\varphi),\qquad
w_0=-1+\frac{\Phi_{\rm res}}{N_\star},\qquad 1+w_0=\frac{\Phi_{\rm res}}{N_\star}.$$
So the *structural* correspondence is real and coordinate-clean: *local anti-gravity
($\mathcal F<0$, $\theta<0$) and cosmic acceleration are **structural analogs** — both are a small
offset from a reciprocal balance ($\theta=0$ locally, $w=-1$ cosmologically) — but they live in
different rapidity coordinates and are **not the same $\theta$.*** The balance point for the local
force is $\theta=0$; the balance point for cosmology is $w=-1$. Conflating them would contradict
note 21's $\Theta_H=+180$.

**Where I must be blunt: the *sign* of the offset is a phase knob, not a prediction.** The number
quoted in note 21, $\Phi_{\rm res}=+0.894$, $w_0=-0.99693$, $1+w_0=+0.00306$ (quintessence), is the
value at the **integer** shell $N=291$. But the depletion shell is actually $N_\star=291.88$
(note 08), and $\Phi_{\rm res}=-\cos(2N\ln\varphi)$ is the cosine of a *large* argument
($2N\ln\varphi\approx280$ rad), so it is acutely phase-sensitive. Evaluated honestly across the
shell-convention ambiguity (verify §5b):
$$N=291\to 1+w_0=+0.00306\ (\text{quintessence}),\quad
N_\star=291.88\to +0.00088\ (\text{quintessence, but }3.5\times\text{ smaller}),$$
$$N\approx292.15\to 0\ (\text{de Sitter balance}),\qquad N=293\to -0.0025\ (\textbf{phantom}).$$
The cosine zero-crossing sits at $N\approx292.15$ — barely $\Delta N\approx0.3$ beyond the true
depletion shell. So $1+w_0$ runs the **entire** quintessence$\to$de Sitter$\to$phantom range within
$\Delta N\lesssim1.3$ of the quoted shell, and landing on the *quintessence* side requires
truncating $N_\star=291.88$ down to $291$. Note 21's own history confirms the fragility: its
**local-shell** reading gave the opposite sign, phantom $w_0=-1.003$, "fixed" by switching to
horizon anchoring. *Selecting the convention that yields the desired sign is the fudge.* I
therefore retract any side-claim: the framework does **not** robustly predict which side of $w=-1$
the offset falls on, and I drop the earlier "the side DESI has hinted at" remark as unsupported.

**Honest comparison to established cosmology.** What survives is *magnitude and structure*, not
sign: $|1+w_0|\lesssim1/N_\star=3.4\times10^{-3}$ — a definite, geometry-locked, *small* deviation
from $\Lambda$CDM's $w\equiv-1$, an order of magnitude below current DESI sensitivity. The
framework cleanly recovers the $\Lambda$CDM limit ($w=-1$, $\theta=0$) as the balance and bounds
the departure to sub-percent; it does **not** earn a claim about the direction of that departure.
That is the honest reading: a structural analog with a geometry-fixed amplitude bound, and a side
that is convention-dependent — *consistent only as a structural analog.*

## Extension — the shielding cost is an exact $\sinh$ functional, and its derivative is the force

§3 said the price of suppressing gravity is "paid in time, one-for-one." That phrasing is correct
but qualitative; the algebra makes it an exact functional, anchored entirely to the identity core
($T\cdot G=1$, $\mathcal F=2\sinh\theta$) — no cosmology, no phase, no knob.

Define the **shielding cost** $\mathcal C(\theta)$ as the work done moving along the boost against
the net force, i.e. the antiderivative of the scalar force $\mathcal F$,
$$\mathcal C(\theta)\equiv\int_0^\theta\mathcal F(\theta')\,d\theta'
=\int_0^\theta 2\sinh\theta'\,d\theta'=2(\cosh\theta-1)=G+T-2.$$
*Caveat, per the framework's standing constraint that the generator $D_k$ is non-Hermitian:*
$\mathcal C$ is the **classical line-integral of the real scalar net force** $\mathcal F(\theta)$
along the 1D rapidity line — a c-number potential, exactly as $\mathcal F$ itself is the c-number
imbalance $G-T$. It makes **no** claim about a norm, energy spectrum, or mode stability of the
non-Hermitian operator, so the "specify the space & inner product" caveat does not bind here; this
is force-times-displacement on a real axis, nothing more. Three things fall out immediately, all
identities:

1. **The cost is even: $\mathcal C(-\theta)=\mathcal C(\theta)$.** Repulsion and attraction one
   golden shell out cost *exactly the same*, $\mathcal C(\pm1/\varphi)=2(\cosh(1/\varphi)-1)=0.39428$.
   This is the potential-level statement of the §2 mirror: the now is not just the force-zero, it is
   the unique *minimum* of the potential $\mathcal C$ ($\mathcal C(0)=0$, $\mathcal C''(0)=2\cosh0=2>0$),
   and the two branches are degenerate in cost — there is no preference, *in this real scalar
   potential*, for the gravity side over the time side. The arrow of time (note 05) must therefore
   come from the entropy gradient (the branch-detailed-balance $\kappa(+k)/\kappa(-k)=e^{-2\theta}$),
   *not* from a cost asymmetry: this potential is blind to the sign of $\theta$.

2. **Its gradient *is* the force, and its curvature is the conserved unit plus the cost.** By
   construction $\mathcal C'(\theta)=\mathcal F(\theta)=2\sinh\theta$, and
   $$\mathcal C''(\theta)=2\cosh\theta=G+T=\mathcal C(\theta)+2.$$
   So the cost obeys the autonomous ODE $\mathcal C''=\mathcal C+2$ — the force-potential is its own
   curvature shifted by exactly $2$, the doubled $L_y=1$. The reciprocal law is hiding inside the
   second derivative: $\tfrac14[(\mathcal C'')^2-(\mathcal C')^2]=\tfrac14[(G+T)^2-(G-T)^2]=GT=1$,
   recovering $T\cdot G=1$ as the **discriminant** of the cost functional. (This is the note-10
   $G_{\rm sym}^2-G_{\rm flow}^2=1$ invariant read on the cost's own derivatives.)

3. **The shielding cost diverges exactly as the inverse of the suppression.** To attenuate gravity
   to $G=\epsilon<1$ requires $\theta=\ln\epsilon$, and then
   $$\mathcal C=G+T-2=\epsilon+\frac1\epsilon-2\;\xrightarrow{\ \epsilon\to0\ }\;\frac1\epsilon-2
   \sim\frac1G.$$
   The cost to shield gravity by a factor $G$ grows as $1/G$ — the *same* reciprocal that forbids a
   free device, now quantified: halving $G$ roughly doubles the cost; driving $G\to0$ (the
   anti-horizon, $\beta\to-1$) costs unboundedly, $\mathcal C\sim1/G\to\infty$. The "one-for-one"
   of §3 is sharpened: it is *one-for-one in the rays* ($T=1/G$) but *inverse-law in the cost*
   ($\mathcal C\sim1/G$). Anti-gravity is permitted; its price scales as the reciprocal of how much
   gravity you cancel.

All four numbers ($\mathcal C(\pm1/\varphi)=0.39428$; $\mathcal C''(0)=2$; the discriminant $=1$;
$\mathcal C\to1/G$) are added to the verify script (§6) and confirmed to machine precision.

## Verdict

**The identity core is solid and machine-precise.** The one-force law **permits** repulsion
structurally: anti-gravity is the $\theta<0$ branch where the time ray ($-1$ eigendirection)
dominates the gravity ray ($+1$ eigendirection) in the net force. The spectrum of $K$ stays
$\pm1$ on *both* branches — nothing exotic is switched on; what reverses is only *which
eigendirection wins the imbalance* $\mathcal F=G-T$. It is the exact CPT-like reflection of
attraction across the now ($\theta\to-\theta$ swaps the rays), with mirror magnitude
$|\mathcal F(\pm1/\varphi)|=1.31627$, $|\beta|=0.5498$. The reciprocal law $T\cdot G=1$ does **not**
forbid this side — it holds identically for $\theta<0$ — but it **forbids gravity shielding**: you
cannot suppress $G$ without an equal, ultimately unbounded, speed-up of the clock $T=1/G$. These
are algebraic identities, verified to machine precision.

**The cosmology link is weaker and I grade it down accordingly.** Cosmic acceleration is a
*structural analog* of the $\theta<0$ branch (a small offset from the $w=-1$ balance, not a literal
$\theta<0$ — the horizon scale-rapidity is the large *positive* $\Theta_H=+180.39$). The framework
locks the *amplitude* of the offset to $|1+w_0|\le1/N_\star=3.4\times10^{-3}$, but the **sign** of
that offset is a phase knob (§4): it flips quintessence$\leftrightarrow$phantom within $\Delta N\lesssim1$
of the quoted shell, so no side-claim is earned. No working anti-gravity device is claimed; what is
claimed is the structure the algebra permits (identity-level, solid), the price it sets (the
reciprocal shielding cost, identity-level, solid), and — at most — a structural cosmological analog
with a bounded but sign-ambiguous offset.

**Falsifier (the strong one, on the identity core):** a material that attenuates the gravitational
coupling ($G<1$, locally weaker gravity) while clocks inside it run at the ambient rate
($T\approx1$) would violate $T\cdot G=1$ and kill the reciprocal law. This is the clean, sign-free
falsifier the thread actually owns.

**On cosmology, I will *not* offer a directional falsifier**, because the framework does not
robustly predict the direction (§4): with the depletion shell $N_\star=291.88$ sitting only
$\Delta N\approx0.3$ from the cosine zero-crossing, both quintessence and phantom are reachable by
a sub-shell convention change, so a measured $w_0<-1$ would *not* cleanly falsify the thread — it
would merely select the phantom convention. What the framework genuinely risks is the **amplitude
bound**: a firmly measured $|1+w_0|>1/N_\star=3.4\times10^{-3}$ (a deviation from $\Lambda$CDM
*larger* than the geometry-locked envelope, on either side) would break the horizon-anchored
construction of notes 08 and 21, and with it this thread's structural-analog claim.
