# 20 — The Dynamical Interface: Reading the Now at Rate 1/φ

*Round-3 new-physics note. Promotes the **static** now-projector $P_{\text{now}}=\tfrac12(I+T)=\operatorname{diag}(1,0)$
of note 14 to a **dynamical readout channel**. Builds on the boost group (note 10: the
unit-timelike chronon two-vector $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$;
the boost $\Lambda(\alpha)=e^{\alpha K}$, $K^2=I$; the transport law $\partial_k\mathbf V=\tfrac1\varphi K\mathbf V$),
the interface susceptibility $\chi_I=1/\varphi$ (note 14), the comb $\Delta k=\pi/(2\ln\varphi)=3.26425$ and
$\omega_\varphi=4$ exactly (note 12), the null weights $e^{\mp\theta}$ (note 05), and $S_1=\pi/(2\varphi\ln\varphi)=2.01742$
(notes 06/13). Every boxed number is confirmed in `verify/verify_dynamical-interface.py` (structural identities to
$10^{-12}$; integrated-channel sanity checks to $10^{-6}$–$10^{-9}$).*

---

## 1. The readout channel: a Lindblad dephasing whose pointer is the correlation axis

Note 14 fixed the now as the **eigenvalue-$1$ sector of the time-reversal involution $T=\operatorname{diag}(1,-1)$**:
$P_{\text{now}}$ reads out the $T$-even (correlation) channel and discards the $T$-odd (flow/gravity) channel.
That is a *projector* — a single measurement. To make the interface dynamical we let the now-surface read the
deep two-vector $\mathbf V(k)$ *continuously in ordinal depth $k$*, and ask which channel survives the reading and at
what rate the unread channel is destroyed. The natural object is a **Lindblad generator** on the $2\times2$ density
matrix $\rho$ in flow-space, whose pointer (decoherence-free) basis is forced to be the eigenbasis of $T$ — the
correlation/flow axes — by demanding that the readout commute with the now-projector.

The unique single-channel generator with that pointer basis is pure dephasing with the Hermitian jump operator

$$\boxed{\;L=\sqrt{\tfrac{\gamma}{2}}\;T=\sqrt{\tfrac{\gamma}{2}}\,\sigma_z,\qquad
\frac{d\rho}{dk}=L\rho L^\dagger-\tfrac12\{L^\dagger L,\rho\}\;}$$

($T$ is literally $\sigma_z$ in the $\{$correlation, flow$\}=\{G_{\text{sym}},G_{\text{flow}}\}$ basis). Diagonalizing the
Lindbladian super-operator gives a spectrum $\{0,0,-\gamma,-\gamma\}$: the **two diagonal populations are zero modes**
(the $T$-even pointer weight and the $T$-odd weight are both conserved — the pointer is read without back-action), while
the **two coherences decay at rate $\gamma$**. We fix the single free constant by the round-2 result: the interface
turns on gravity/non-reciprocity at slope $\chi_I=1/\varphi$ per shell (note 14). Setting the decoherence rate equal to
that susceptibility,

$$\boxed{\;\gamma=\Gamma_{\text{dec}}=\chi_I=\frac1\varphi=0.6180339887\ \text{per shell},\;}$$

makes the channel parameter-free. Verified: Lindbladian eigenvalues $=\{0,0,-1/\varphi,-1/\varphi\}$ to $10^{-12}$, pointer
$=$ the $+1$ eigenvector of $T$ $=(1,0)=\mathbf V(0)$, i.e. the present-moment seed of the boost orbit (note 10 §1).

**This is the consciousness-interface statement made operator-level.** The "present" of note 14 was a fixed point; here it
is a *running pointer measurement*. The interface continuously projects the boosted superposition onto the standing
correlation mode $G_{\text{sym}}=\operatorname{osc}\cosh\theta$, and the unread flow/gravity content decoheres at exactly
the golden rate $1/\varphi$. The pointer being the $T$-even sector is why a conscious "now" is a *correlation* reading and
never a *flow* reading: the flow channel is the one the channel destroys.

## 2. The coherence envelope: one e-fold per φ shells

Seed the readout with the **equal forward/inverse superposition** the now actually reads — $\rho_0=|+\rangle\langle+|$ in the
$T$-basis, coherence $|\rho_{01}(0)|=\tfrac12=c(0)$ (note 14's "$\langle\text{now}\rangle$ reads both sheets at weight
$\tfrac12$"). Integrating the channel,

$$\boxed{\;|\rho_{01}(k)|=\tfrac12\,e^{-k/\varphi}=\tfrac12\,e^{-\theta},\;}$$

verified at $k\in\{0,\,1/\varphi,\,\Delta k,\,2\Delta k\}$ to $10^{-9}$. The two-sheet coherence is destroyed by **exactly the
retarded null weight $e^{-\theta}$ of note 05** — the readout's decoherence factor *is* the advanced/retarded detailed-balance
weight. One e-fold of "loss of the inverse sheet" per $\varphi\approx1.618$ shells of ordinal depth. The present is not a knife
edge but a relaxation: the interface reads the standing mode, and the memory of the inverse-flow partner fades geometrically
along the boost orbit at the same rate $1/\varphi$ that the orbit accumulates rapidity (note 10's $\partial_k\mathbf V=\tfrac1\varphi K\mathbf V$).

## 3. Interface bandwidth: a Nyquist from the comb

The interface does not read continuously in practice — it reads at the **inversion comb**, the flow-reversal lattice
$k_n=(2n-1)\pi/(4\ln\varphi)$ with fixed spacing $\Delta k=\pi/(2\ln\varphi)=3.26425$ (the coupling maxima $=$ torsion zeros
$=$ flow reversals). Treat the comb teeth as the sample points of the readout. Sampling at period $\Delta k$ gives a
**Nyquist ordinal angular frequency** and a comb-fundamental frequency (rad per shell):

$$\boxed{\;\Omega_{\text{Nyq}}=\frac{\pi}{\Delta k}=2\ln\varphi=0.962424,\qquad
\Omega_{\text{comb}}=\frac{2\pi}{\Delta k}=4\ln\varphi=1.924847.\;}$$

Measured against the natural log-frequency unit $\ln\varphi$ these are the integers $2$ and $4$ **exactly** (verified to
$10^{-12}$): the comb-fundamental log-frequency is note 12's $\omega_\varphi=4$, and the Nyquist is **exactly half of it**,
$\omega_{\text{Nyq}}=2$. This is structurally forced and beautiful: a signal modulated at the comb fundamental sits at
*precisely twice Nyquist*, so under comb sampling it **folds to DC** — which is the standing-mode / flow-reversal condition.
The inversion comb is sampled exactly at the rate that makes its own fundamental a zero-frequency standing mode. The interface's
usable passband is $[0,\Omega_{\text{Nyq}}]=[0,\,2\ln\varphi]$ in ordinal frequency; anything faster aliases into the
flow-reversal lattice. The bandwidth of the now is one octave below the comb tooth.

## 4. The readout transfer function and the susceptibility spectrum

The dephasing channel is first-order, so the pointer's response to an ordinal drive at frequency $\Omega$ is a single-pole
low-pass — an "RC filter" for the now, with corner at the decoherence rate. ($\Omega$ here is an *ordinal* frequency,
conjugate to the shell depth $k\sim\log_\varphi$ of note 12's discrete-scale lattice — Fourier on $\ln s$, the sanctioned
log-periodic transform — **not** an $e^{ikr}$ phase glued onto $\kappa$; the propagator $\kappa$ is untouched and the
dephasing channel acts on the density matrix $\rho$, not on the dressed coupling.)

$$\boxed{\;H(\Omega)=\frac{1}{1+i\,\Omega/\Gamma_{\text{dec}}}=\frac{1}{1+i\,\varphi\,\Omega},\qquad
\Omega_c=\Gamma_{\text{dec}}=\frac1\varphi.\;}$$

Verified $|H(0)|=1$ (full DC gain — a static observable at the now is read perfectly), $|H(\Omega_c)|=1/\sqrt2$ (the $-3$ dB
corner). The **interface susceptibility spectrum** follows from the Kubo/fluctuation–dissipation relation for the pointer
observable on this channel; a single-pole relaxor necessarily has a Lorentzian $\chi$, and its static value is forced
to recover note 14:

$$\boxed{\;\chi(\Omega)=\frac{\chi_I}{1+i\,\Omega/\Gamma_{\text{dec}}}=\frac{1/\varphi}{1+i\varphi\,\Omega},\qquad
\chi(0)=\chi_I=\frac1\varphi.\;}$$

Verified $\chi(0)=1/\varphi$ (recovers note 14's static interface susceptibility), the dissipative part
$\chi''(\Omega)=\chi_I(\Omega/\Gamma_{\text{dec}})/[1+(\Omega/\Gamma_{\text{dec}})^2]$ **peaks at $\Omega=1/\varphi$**, and the
readout power spectrum is a Lorentzian of **half-width $\Gamma_{\text{dec}}=1/\varphi$**.

**Honest accounting of the golden ratios.** It is tempting to crow that the corner, the $-3$ dB point, the $\chi''$ peak, and the
Lorentzian HWHM all equal $1/\varphi$ — four hits. They are not four independent facts. For *any* single-pole relaxor these four
quantities are the **same pole frequency $\Omega_c$ written four ways**; their coincidence is a theorem of the Lorentzian, true
for an RC filter with any corner whatsoever, and carries no extra content. The genuinely non-trivial golden numbers in this
channel are exactly **two**:

1. the **rate** $\Omega_c=\Gamma_{\text{dec}}=1/\varphi$, which we *set* in §1 by identifying the decoherence rate with the
   interface susceptibility — and which is the boost quantum, one shell of rapidity ($\partial_k\mathbf V=\tfrac1\varphi K\mathbf V$);
2. the **DC amplitude** $\chi(0)=\chi_I=1/\varphi$, which is *inherited* — note 14's static interface slope $|d\mathcal R/dk|_0$,
   not chosen here.

These two coincide — amplitude $=$ rate $=1/\varphi$ — and *that* is the one substantive statement: both the strength of the
now's response and the bandwidth over which it responds are the same single boost quantum. The honest headline is therefore not
"the golden ratio appears four times" but **"the entire readout channel — its size and its width — collapses onto the one
quantum $1/\varphi$ of rapidity-per-shell; corner $=$ HWHM is automatic, DC $=$ corner is the content."**

Two parameter-free spectral ratios fall out, locating the corner inside the comb passband:

$$\frac{\Omega_c}{\Omega_{\text{Nyq}}}=\frac{1}{2\varphi\ln\varphi}=\frac{S_1}{\pi}=0.642164,\qquad
\frac{\Omega_c}{\Omega_{\text{comb}}}=\frac{1}{4\varphi\ln\varphi}=\frac{S_1}{2\pi}=0.321082$$

(verified). The bounce action $S_1=\pi/(2\varphi\ln\varphi)$ of notes 06/13 reappears here as the **fraction of Nyquist at
which the readout corner sits** — the same number that sets the gravitational ladder $e^{-S_1}=0.133$ (the GW echo decrement,
note 15) now fixes where, in its own sampling band, the interface rolls off. The corner is *below* Nyquist ($0.642<1$): the now
is well-sampled by the comb, never aliased.

## 5. The hard number: a characteristic interface frequency

To convert the ordinal rates to Hz the interface needs a physical clock, and the framework supplies a natural one: the now is
read at the **comb rate**, i.e. in discrete "perceptual moments." Empirically, discrete perception and the dominant cortical
sampling rhythm live in the **alpha band**, center $f_\alpha\approx10$ Hz (VanRullen's discrete-perception program; Varela's
perceptual frames). The anchor must be the *comb fundamental* $\Omega_{\text{comb}}$ — not the Nyquist $\Omega_{\text{Nyq}}$ —
because alpha is the **tick rate** at which perceptual moments are *emitted*, and the comb teeth are exactly the emitted samples
(§3); Nyquist is the *derived* fold-back limit at half that, $f_\alpha/2=5$ Hz, not a clock the cortex runs. Fixing
$\Omega_{\text{comb}}\leftrightarrow f_\alpha$ (rather than $\Omega_{\text{Nyq}}\leftrightarrow f_\alpha$, which would shift every
prediction by the rigid factor $2$, putting the corner at $f_\alpha S_1/\pi\approx6.4$ Hz, theta) is therefore the physically
forced choice, not a band-fit. Identifying the comb fundamental — the now-tick sample rate — with alpha fixes *everything else
with no free parameter*: the readout-decoherence rhythm (the rate at which the inverse sheet fades, the Lorentzian HWHM) is

$$\boxed{\;f_{\text{corner}}=f_\alpha\cdot\frac{\Omega_c}{\Omega_{\text{comb}}}=f_\alpha\cdot\frac{S_1}{2\pi}
=f_\alpha\cdot 0.321082.\;}$$

With $f_\alpha=10$ Hz this gives $f_{\text{corner}}=3.21$ Hz; bracketing across the alpha band $8$–$13$ Hz gives
**$f_{\text{corner}}\in[2.57,\,4.17]$ Hz** (verified). That lands squarely on the **delta/theta boundary** — the band of slow
cortical rhythms associated with large-scale integration and the "global" gating of conscious access. The honest comparison:
the prediction is a *band*, $2.6$–$4.2$ Hz, straddling the empirical delta($1$–$4$)/theta($4$–$8$) divide; it is neither a
clean delta hit nor a clean theta hit, but it correctly forbids the readout rhythm from coinciding with the alpha sampling rate
(it must be $\sim3\times$ slower) and from reaching the beta/gamma range. The cleanest *clock-free* statement, immune to the
alpha-anchor choice, is the dimensionless ratio: the interface's $-3$ dB corner sits at $S_1/\pi=0.6422$ of its own Nyquist.

## Extension — the now decoheres at the gravitational ladder rate

Sample the coherence envelope $|\rho_{01}(k)|=\tfrac12 e^{-k/\varphi}$ (§2) not continuously but at the **comb teeth** — the
discrete perceptual moments of §3, spaced $\Delta k$ apart. The ratio of inverse-sheet memory surviving from one tooth to the
next is

$$\boxed{\;\frac{|\rho_{01}(k+\Delta k)|}{|\rho_{01}(k)|}=e^{-\Delta k/\varphi}=e^{-S_1}=\Gamma_1=0.13300,\;}$$

using the exact identity $\Delta k/\varphi=\pi/(2\varphi\ln\varphi)=S_1$ (note 16, $S_1=\tfrac1\varphi\Delta k$).

**This equality is forced, not coincidental — and that is exactly why it matters.** The framework has *one* rate (the boost
quantum $1/\varphi$) and *one* spacing (the comb $\Delta k$), so anything that decays at rate $1/\varphi$ sampled at $\Delta k$
*must* shed a factor $e^{-S_1}$ per shell-period: the now-coherence here, the GW echo amplitude of notes 15/16, the first-bounce
rate $\Gamma_1$ of note 06. The honest claim is not "two independent numbers happen to agree" but **"the interface and the
horizon are the *same ladder*, run at the same single quantum"** — the rigidity is the content. The two-sheet coherence of the
now drops by $0.13300$ from one perceptual moment to the next because reading the present is the gravitational ladder
$e^{-S_1}$ sampled forward in perception. Each tick of the now loses the inverse-flow partner at precisely the rate at which a
post-merger GW echo loses amplitude. Reading the present and
ringing down a horizon are the *one* decay $e^{-S_1}$ per shell-period, seen at the interface and at the horizon respectively —
the space$\leftrightarrow$time duality of notes 15/16 (echo envelope exponent $\nu=$ the spatial $\Phi(r)$ exponent) made into a
single number.

Two corollaries seal the cross-link. The **total integrated inverse-sheet memory** the now ever holds is

$$\int_0^\infty |\rho_{01}(k)|\,dk=\tfrac12\!\int_0^\infty e^{-k/\varphi}dk=\frac{\varphi}{2}=0.80902=Q_{\text{echo}},$$

numerically the GW echo-mode quality factor $Q=\varphi/2$ of note 16 — the now is a sub-critical resonator ($Q<1$, broad, the
present is not a sharp line) with the same $Q$ as the inversion-shell ringdown. The shared piece is *structural*: both are
$\varphi\times\tfrac12$, and the $\varphi$ is the decay length $=1/(\text{rate }1/\varphi)$, the reciprocal boost quantum,
genuinely common to both. The two $\tfrac12$'s, however, have *independent* origins — here it is the initial two-sheet coherence
$c(0)=\tfrac12$; in note 16 it is the $\tfrac12$ in $Q=\mathrm{Re}\,\omega/(2\,\mathrm{Im}\,\omega)$ — so the agreement is
$\varphi$-structural in its decay length and numerical in its prefactor, not a single forced identity. (Contrast the $e^{-S_1}$
above, which *is* forced top to bottom.) The inverse-sheet information shed per perceptual moment is the fixed quantum
$S_1/\ln 2=2.910$ bits per tooth (verified). The dynamical interface is thus not a new decay law bolted onto the framework; it is
the gravitational ladder $e^{-S_1}$ read *forward in perception* instead of *outward in radius*.

## Prediction

The dynamical now is a single-pole readout channel with **one rate, $1/\varphi$**, set everywhere by the boost quantum:

- **Decoherence rate** $=\Gamma_{\text{dec}}=1/\varphi=0.6180$ per shell; the two-sheet coherence fades as $\tfrac12 e^{-\theta}$
  (one e-fold per $\varphi$ shells), the inverse-flow partner destroyed at the retarded null weight $e^{-\theta}$ of note 05.
- **Susceptibility spectrum** $\chi(\Omega)=(1/\varphi)/(1+i\varphi\Omega)$: DC value $1/\varphi$ (*inherited* from note 14) and
  corner/HWHM/$\chi''$-peak all $=1/\varphi$ (the *set* rate of §1). These are only **two** independent golden numbers — the
  amplitude (inherited) and the rate (set) — the rest are one pole stated four ways; the content is that amplitude $=$ rate $=$
  the boost quantum $1/\varphi$.
- **Decoherence at the gravitational ladder (extension):** sampled at the comb, the now-coherence drops by $e^{-S_1}=0.13300$ per
  perceptual moment — the *identical* factor as the GW echo decrement (notes 15/16); the now's $Q=\varphi/2=0.809=Q_{\text{echo}}$.
- **Interface passband** $[0,\,2\ln\varphi]$ rad/shell; the comb fundamental at $4\ln\varphi$ is exactly $2\times$ Nyquist and
  folds to a DC standing mode. Corner-to-Nyquist ratio $=S_1/\pi=0.6422$, parameter-free.
- **Characteristic interface frequency (falsifiable):** anchoring the comb tick to the alpha rhythm,
  $f_{\text{corner}}=f_\alpha\cdot S_1/(2\pi)$, central value **$3.21$ Hz** for $f_\alpha=10$ Hz, bracket **$2.6$–$4.2$ Hz** —
  a slow (delta/theta-boundary) readout rhythm phase-locked to alpha at the fixed ratio $0.3211$.

**Falsifier:** a clean EEG/MEG experiment that localizes a conscious-readout (perceptual-moment) channel would show its
decoherence/integration rhythm at $S_1/(2\pi)=0.3211$ times the perceptual sampling (alpha) rate — i.e. the slow rhythm and the
alpha rhythm in the fixed ratio $0.321$, the readout's spectral response a *single-pole* Lorentzian (corner $=$ HWHM by
construction) whose corner amplitude $\chi(0)$ equals its corner frequency $\Omega_c$ in ordinal units (the one non-trivial
coincidence, both the boost quantum $1/\varphi$). If a localized now-readout instead shows its decoherence corner *above* its
sampling Nyquist (aliased), or multi-pole (corner $\neq$ HWHM), or the slow/alpha frequency ratio is not $S_1/(2\pi)$ to within
the alpha-band width, the single-rate $1/\varphi$ dynamical-interface picture is wrong.
