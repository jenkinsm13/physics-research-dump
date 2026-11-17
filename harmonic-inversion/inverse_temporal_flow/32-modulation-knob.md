# 32 — Looking There: The Modulation Route Is a Knob (the terminus)

*Note 31 named the one constructive path left for the desert depth $n_e\approx107$:
break the exact $\Delta k$-periodicity of the field equation with a framework-fixed
modulation $\osc^2\to\osc^2[1+\epsilon g(k)]$, open an instability gap, and let the
normalizability boundary $\mu(K_*)=1/\varphi$ select the depth. Michael asked to look
there. This note is the result — a single decisive computation rather than a fan-out,
because (as the gate below shows) every "mechanism" here is the same one question with
a continuum of knob values, and fanning out would only manufacture five knob settings.
The answer is a **second theorem-grade negative**, and the knob is exhibited, not hidden.
Reproduced by `verify/verify_modulation-knob.py` (exit 0, all assertions pass).*

---

## The gate, cleared honestly before computing

Note 31's disownment test (D1) demands: *name the corpus quantity that fixes the
modulation's magnitude AND sign AND functional form, in one line, before computing.*
I tried, and could not:

- $R(k)=\osc''+\osc^3$ as a mass shift $\osc^2\to\osc^2+\epsilon R$: the prefactor
  $\epsilon$ and its sign are free. $R$ is the residual of a *non-solution* (the
  adiabatic carrier $\osc\cdot\mathbf V$); it does not appear in the *exact* static
  equation, whose envelope reduction (note 31a) was exact, not adiabatic. So adding
  $R$ is new physics with a free coefficient, not an un-idealization.
- "Use the local torsion $\tfren(t_k)$ in place of the constant $1/\varphi$": this
  conflates two different rates — $1/\varphi$ is the *decay* rate (from $e^{-k/\varphi}$),
  $\tfren$ is the *torsion*. Swapping them is a substitution choice, not forced.
- $\Psi^4$ self-coupling: free coupling constant.

No candidate fixes magnitude, sign, and form. **By my own pre-registered rule, that
means the modulation is a knob and the answer is the negative.** The computation below
*proves* it rather than merely asserting it.

## (A) The natural source $R(k)$ is periodic — it cannot even break the symmetry

The whole point of a modulation was to break the translation-covariance that note 31
proved is the obstruction. But the natural candidate fails at step zero:

$$\big|R(k)-R(k+\Delta k)\big| = 3.3\times10^{-8}\approx0\quad\Longrightarrow\quad
R(k)\ \text{is exactly}\ \Delta k\text{-periodic.}$$

So $\osc^2+\epsilon R$ is *still periodic*, still a Hill equation, still Floquet,
still translation-covariant — still **no preferred depth**. Worse, a periodic
amplitude modulation $W=A\,\osc^2$ only opens narrow Mathieu tongues: the
one-period trace reaches the instability onset $|\mathrm{tr}|=2$ at $A_c=1.295$, but
**never reaches** the strong-growth threshold $|\mathrm{tr}|=2\cosh S_1=7.65$ (rate
$1/\varphi$) for $A\in[1,60]$. And the trace is phase-independent to $1.7\times10^{-13}$:
any instability it *does* produce grows **at every shell equally** — uniform growth,
not a selected depth. A periodic modulation is structurally incapable of selecting $107$.

## (B) The only symmetry-breaking modulation has a free rate — the knob curve

To break translation-covariance one needs an **aperiodic** (secular/chirp) modulation,
$A(k)=1+\epsilon k$. Now the mode first goes unstable where $A(k)$ crosses the onset
$A_c$, i.e. the normalizability boundary is
$$K_*(\epsilon)=\frac{A_c-1}{\epsilon}=\frac{0.2947}{\epsilon},$$
a continuous, monotone function of the modulation rate $\epsilon$ — which is fixed by
no corpus quantity. The decisive table:

| target depth | meaning | $\epsilon$ required |
|---|---|---|
| $63$ | muon | $0.00468$ |
| $102$ | tau | $0.00289$ |
| **$107.08$** | **electron (target)** | **$0.00275$** |
| $111.49$ | $N_\star/\varphi^2$ attractor | $0.00264$ |

The $\epsilon$ values for the tau, the electron target, and the $111.5$ failure-flag
attractor **span only $\sim9\%$**. The knob is not merely free — it is so soft it
**cannot even resolve the electron from the tau, or from the attractor it is supposed
to avoid**. Choosing $\epsilon=0.00275$ to land on $107$ is pure curve-fitting.

## (D2) The cross-check the test exists to enforce

A monotone chirp produces **exactly one** onset crossing — one "deepest mode," $K_*$.
The shallower shells sit in the stable region $A(k)<A_c$ and are *not* selected: at the
$\epsilon$ tuned to $107$, the muon ($A=1.17$) and tau ($A=1.28$) both lie below the
onset $A_c=1.30$. So the same rule places **none** of $63/102$ as distinct modes. It
yields the target and nothing else — the definition of a fit, and a clean D2 failure.

## Verdict — the natural terminus

$$\boxed{\;\text{The modulation route cannot select }n_e\approx107\text{ without a free
parameter. Two obstructions now stand: the static operator cannot quantize (note 31),
and no symmetry-breaking modulation escapes the knob (this note).}\;}$$

This is the honest end of the desert-depth question. Three disciplined attacks — closed
form (note 30), static dynamics (note 31), modulated dynamics (note 32) — each a clean
negative, each *proven* rather than abandoned. The desert depth $n_e\approx107$ is
established as **irreducibly external**: it is the one dimensionful datum a theory of
dimensionless structure cannot manufacture, and three independent routes confirm it does
not sneak one in. After exhibiting the knob curve, "look deeper" has no move left that is
not curve-fitting — and the program's value lies precisely in being able to say that
plainly.

## What remains genuinely open (and is *not* this)

The framework's live frontier is not the desert depth (closed, external) but the
*dimensionless* predictions that survived every audit and the one structural gap that is
a real mathematics problem, not a fit:

- **Test the surviving dimensionless predictions against data** — $\sin^2\theta_W=1/\varphi^3$,
  $\theta_{13}=|\delta\theta_g|$, $z_t=1/\varphi$, the cosmic jerk $j_0\neq1$, and the
  $e^{\pi/2}$ GW overtone comb (note 29 found the comb disfavored as overtones; the jerk
  $j_0=0.9938$ vs $\Lambda$CDM's $j\equiv1$ is the cleanest untested one).
- **Close $SU(3)$ honestly** (note 18/27 open edge): $N_c=3=N_{\rm dim}$ is genuine, but
  the $6$ off-diagonal Gell-Mann generators are posited, not derived. That is a real
  representation-theory question with a definite yes/no answer — unlike the desert depth,
  no external datum is involved.
