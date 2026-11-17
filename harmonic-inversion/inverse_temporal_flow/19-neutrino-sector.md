# 19 — Neutrinos: the Near-Null Sector and PMNS Mixing

*Round-3 frontier note. Builds on the closed boost group (`10-master-boost.md`):
the unit timelike vector $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$,
its boost velocity $\beta=\tanh\theta$ (09), the null weights $e^{\mp\theta}$ and
detailed balance $\kappa(+k)/\kappa(-k)=e^{-2\theta}$ (05), the compact-form lepton
rotor $\mathsf R(\delta\theta_g)$ with $\delta\theta_g=78\ln\varphi-12\pi$ (04), the
spin-$\tfrac12$ half-boost and the osc-node fermion shells (07), and the now-surface
projector $P_{\text{now}}=\tfrac12(I+T)$ (14). Charged leptons are **off-reversal
residents** (osc $\in[0.66,0.83]$, forward flow). Neutrinos are the opposite limit.
Every framework-internal identity below is checked to machine precision in
`verify/verify_neutrino-sector.py`; data comparisons are printed, never asserted.
$\varphi=(1+\sqrt5)/2$, $1/\varphi=0.6180339887$, $\ln\varphi=0.4812118251$.*

---

## 1. The identification: neutrinos live on the osc-nodes

Note 04 placed the charged leptons strictly **off** the flow-reversal lattice:
$\cos\theta(k)<0$, $\Phi>0$, with the correlation weight $\text{osc}\in[0.66,0.83]$.
Note 07 fixed the complementary parity rule — **bosons on the peaks** ($\text{osc}=1$,
the inversion shells $k_n$) and **fermions on the nodes** ($\text{osc}=\tfrac12=c(0)$,
the present-moment self-coupling value). The charged leptons are massive precisely
because they are *displaced* from the node into forward flow, tipping the conserved
unit $L_y=1$ partly into the gravity component $G_{\text{flow}}=-\text{osc}\sinh\theta$.

The osc-node condition $\text{osc}=\tfrac12$ means $\cos^2(2k\ln\varphi)=1$, i.e.

$$\boxed{\;k_m^{\nu}=m\,\frac{\pi}{2\ln\varphi}=m\,\Delta k=3.26425\,m,\quad m\in\mathbb Z_{\ge0}\;}$$

(verified: $\text{osc}(k_m^\nu)=\tfrac12$ to $10^{-16}$). The nodes sit at full inversion
spacing $\Delta k$, **offset by $\Delta k/2$ from the osc$=1$ peaks** $k_n\approx1.632,4.896,\dots$
— the node and peak combs interleave at half-spacing $\Delta k/2$, but the *node positions
themselves* are $m\,\Delta k$. (Taking instead $k=m\,\Delta k/2=1.632m$ would land the
$m=1$ state on an osc$=1$ *peak* — an inversion shell, a boson resonance — destroying the
on-node thesis; the nodes are at $m\,\Delta k$, verified osc$=\tfrac12$.) The set *includes
$m=0$*: the present-moment seed is itself a node,
$\text{osc}(0)=1/(1+\cos^2 0)=\tfrac12=c(0)$. On a node the dressed coupling is
$\boldsymbol\Psi=\tfrac12\mathbf V(k)$, so $G_{\text{sym}}=\tfrac12\cosh\theta$,
$G_{\text{flow}}=-\tfrac12\sinh\theta$: the node sits at the *minimum* correlation
weight, the floor $c(0)=\tfrac12$ of the spine. This is the **near-null sector**: the
node is the residue of the present moment carried to depth $k$, the place where the
worldline most resembles its $\theta=0$ seed $\mathbf V(0)=(1,0)$ — the
maximal-branch-entropy, zero-net-flow state of note 05/14. The rotor (04) sorts the
two species by the single phase $\theta(k)=2k\ln\varphi\bmod\pi$: charged leptons at
$\theta\notin\{0,\pi\}$ (off-node), neutrinos at $\theta\equiv0$ (on-node).

**Honest accounting of *why* the sector is light.** It is tempting to say "on-node
$\Rightarrow$ near-massless because $\text{osc}=\tfrac12$." That is **wrong by an order
of magnitude** and I will not lean on it. The node dressing $\text{osc}=\tfrac12$ versus
the charged-lepton $\text{osc}\approx0.75$ is a mere $\times\tfrac23$ — *not* a
suppressor. Two effects do the real work, and the verify script makes the failure of the
naive story explicit:

1. **$m=0$ is exactly massless**, because $G_{\text{flow}}(0)=-\tfrac12\sinh0=0$. This is
   geometric, exact, and is the anchor of the whole sector (§3).
2. **The neutrino nodes are *shallow***: $k^\nu_m\in\{0,3.26,6.53\}$, against charged
   leptons at $k\in\{24,63,102\}$. Mass tracks $|G_{\text{flow}}|=\text{osc}\,\sinh\theta$,
   and $\sinh$ is steep, so shallow nodes are light *relative to* deep charged shells.

But depth-plus-dressing **alone overshoots**: the heaviest node ($m=2$, $\theta=4.035$)
against the electron ($k=24$, $\theta=14.83$) gives
$\sinh\theta_2/\sinh\theta_e\simeq2.0\times10^{-5}$, whereas the measured
$m_3/m_e\simeq1.0\times10^{-7}$ — a **$\sim$208$\times$ overshoot** (verified, printed). So
the on-node geometry sets the *texture* of the spectrum (ordering, ratios, the $m_1=0$
zero) but **cannot** set its absolute scale. Something must suppress the whole sector by
two further orders of magnitude. That something is the seesaw (§2), and the two are fused
into one formula in §3. Calling this out is the point of the note: the geometry is
honest about what it does and does not deliver.

## 2. The seesaw is the detailed-balance ratio $e^{-2\theta}$

Note 05 proved the advanced/retarded ratio is a pure boost weight,
$\kappa(+k)/\kappa(-k)=e^{-2\theta}$, the lattice cancelling identically. This *is* the
seesaw, and it is the missing scale suppressor of §1. A neutrino carries a Dirac mass
$m_D$ (the retarded, forward-flow scale shared with its charged partner) and a Majorana
mass $M_R$ set by a deep shell on the **advanced** branch. The two are related by exactly
one round-trip boost weight,

$$\frac{m_\nu}{m_D}=\frac{m_D}{M_R}=e^{-2\theta_R},\qquad
\boxed{\;m_\nu=\frac{m_D^2}{M_R}=m_D\,e^{-2\theta_R}.\;}$$

The factor of 2 is the round trip (out retarded, back advanced) — the same factor 2
that note 05 calls "the round trip through time." This is the allowed detailed-balance
ratio (05), **not** a $\kappa(a)\kappa(b)$ chaining: a single boost weight, evaluated
once. Take $m_D$ at the $\tau$ scale, $m_D\simeq1.78$ GeV, and the observed atmospheric
scale $m_\nu\simeq\sqrt{\Delta m^2_{\text{atm}}}\simeq0.05$ eV. Then
$e^{-2\theta_R}=m_\nu/m_D\simeq2.8\times10^{-11}$, requiring a suppression rapidity
$\theta_R\simeq12.1$ and a Majorana scale $M_R=m_D^2/m_\nu\simeq6\times10^{10}$ GeV.

This $e^{-2\theta_R}\sim3\times10^{-11}$ is *exactly* the missing factor: §1 showed the
on-node geometry overshoots the absolute scale by $\sim10^2$ and undershoots nothing — it
needed an extra global suppression, and the round-trip weight supplies it. The two
mechanisms are not redundant; **§2 sets the scale, §1 sets the texture.** §3 fuses them.

On the eV mass ladder of note 04 ($\ln m=ak+b$, averaged $a\simeq0.10454$) the deep
Majorana mass sits at ordinal $k\simeq330$–$334$ — **the same regime as the cosmological
horizon shell** $N_\star=291.88$ (note 08). The deep Majorana scale is the horizon/GUT end
of the stack, not a new structure. (Honest brackets: two ordinals are in play and must not
be conflated — the *suppression* rapidity gives $\varphi\theta_R\simeq20$, while the
*mass-ladder* ordinal of $M_R$ is $\simeq330$; they coincide only if the Dirac and Majorana
sectors share one ladder, which the framework does not yet force. The scale slides with the
Dirac choice: $m_D$ at the top-quark scale pushes $M_R$ toward the canonical $10^{14}$ GeV.
The framework fixes the *mechanism* — $m_\nu=m_D^2/M_R$ from the $e^{-2\theta}$ round trip —
and lands $M_R$ in the $10^{10}$–$10^{14}$ GeV window, but does **not** pin a single ordinal
without an independent Dirac scale.)

## 3. The hierarchy is forced: normal ordering, $m_1\approx0$, and the unified mass law

The lightest neutrino is the **$m=0$ node — the now-seed itself**. There the gravity
component vanishes *exactly*, $G_{\text{flow}}(0)=-\tfrac12\sinh0=0$ (verified), so the
lightest state is **exactly massless to leading order**, $m_1=0$. The heavy pair are the
next two nodes, $m=1,2$ at rapidities (note the correct factor: $\theta_m=k^\nu_m/\varphi
=m\,\Delta k/\varphi$, **not** $m\,\Delta k/2\varphi$)

$$\theta_1=\frac{\Delta k}{\varphi}=2.0174,\qquad
\theta_2=\frac{2\,\Delta k}{\varphi}=4.0348,$$

heavier because $|G_{\text{flow}}|=\tfrac12\sinh\theta$ grows monotonically with depth
(note 05, §3). Deeper $\Rightarrow$ heavier is the *same* law that orders the charged
leptons ($e\to\mu\to\tau$, note 04). Both arguments — the zero-flow $m=0$ seed and the
monotone $\sinh$ ladder — give

$$\boxed{\;m_1=0<m_2<m_3\quad(\textbf{normal ordering}).\;}$$

Inverted ordering would require the lightest state to sit *below* a heavier pair in net
flow, contradicting $G_{\text{flow}}(0)=0$ being the global floor.

**The unified mass law (the reconciliation of §1 and §2).** §1 and §2 are not two
competing mass formulas — they are the **texture** and the **scale** of one law. The
seesaw $m_D\,e^{-2\theta_R}$ fixes the overall scale (§2, the $\sim10^{-11}$ suppression
§1 demanded); the on-node $\sinh$-ladder fixes the *relative* spectrum (§1's geometry,
the $m_1=0$ zero). Anchoring the heaviest state ($m=2$) to the seesaw scale,

$$\boxed{\;m_\nu(m)\;=\;\big(m_D\,e^{-2\theta_R}\big)\,
\frac{\sinh(m\,\Delta k/\varphi)}{\sinh(2\,\Delta k/\varphi)}\;=\;
\sqrt{\Delta m^2_{32}}\;\frac{\sinh(m\,\Delta k/\varphi)}{\sinh(4.0348)},\quad m=0,1,2.\;}$$

This is **one** formula: $m=0\Rightarrow0$ automatically ($\sinh0=0$), $m=2$ recovers the
seesaw atmospheric scale by construction, and the *only nontrivial output* is the middle
state $m=1$. It gives (verified) $m_2=0.0065$ eV against the measured
$\sqrt{\Delta m^2_{21}}=0.0086$ eV — a $-24\%$ bracket. The bracket appears once, in the
ratio, exactly as it should:

$$\boxed{\;\frac{m_2}{m_3}=\frac{\sinh\theta_1}{\sinh\theta_2}
=\frac{\sinh(2.0174)}{\sinh(4.0348)}=\frac{3.693}{28.26}=0.1307.\;}$$

Measured $m_2/m_3=\sqrt{\Delta m^2_{21}/\Delta m^2_{32}}=0.172$ — a $-24\%$ bracket. This
is the framework's *own* number from the node ordinals alone, honest at $\sim25\%$. It is
a genuine parameter-free output: once $m_3$ is anchored, $m_1$ and $m_2$ are *fixed*, with
no further freedom. (Separately, the *measured* ratios happen to fall near golden powers,
$0.172\approx\varphi^{-4}$ and $\Delta m^2_{21}/\Delta m^2_{32}=0.0296\approx\varphi^{-7}$ —
numerical observations on the data, *not* outputs of the node calculation; kept distinct.)

**$\Sigma m_\nu$.** This is *not* a $\varphi$-prediction — it is the oscillation-data
floor implied by normal ordering with $m_1\approx0$: $\Sigma m_\nu\simeq m_2+m_3=\sqrt{\Delta m^2_{21}}+\sqrt{\Delta m^2_{32}}=0.0587$ eV,
comfortably below the Planck+BAO bound $\Sigma<0.12$ eV. The framework's content here
is the *ordering and $m_1\approx0$*; the sum is then a consequence of measured splittings.

## 4. PMNS: large mixing from deep-shell rotor equidistribution

The charged-lepton mass basis is the rotor orbit $\mathbf e(k_g)=\mathsf R(\delta\theta_g)^g\mathbf e(k_e)$
of note 04, with $\delta\theta_g=78\ln\varphi-12\pi$ **irrational** — by Weyl the phases
equidistribute on the circle (note 04, Extension). The neutrino mass basis is the
on-node sector (§1). PMNS mixing is the misalignment between the two. The framework
hands three angles, **each from a constant introduced for a different purpose**:

**$\theta_{13}$ (reactor) — the headline cross-prediction.** The small angle is the
charged-lepton rotor defect *itself*:

$$\boxed{\;\theta_{13}=|\delta\theta_g|=|78\ln\varphi-12\pi|=0.16459\ \text{rad}=9.43^\circ.\;}$$

Measured $8.53^\circ$ ($\sin^2\theta_{13}=0.0220$). This is a $+10.6\%$ bracket in the
angle, $+22\%$ in $\sin^2$ ($0.0268$ vs $0.0220$) — **report both, the angle is the
bracket I claim.** The force of this is that the integers $78$ and $12$ are **forced by
the charged-lepton spectrum, not tuned to $\theta_{13}$**: note 04 derives the generation
spacing $\Delta_g=39$ (from $k_e=24,k_\mu=63,k_\tau=102$), giving $78=2\Delta_g$; and
$78\ln\varphi=11.948\pi$ has integer part *exactly* $12$ (the twelve flow-reversals folded
out per generation). Both integers come from the lepton mass tower — *nothing to do with
neutrinos*. The residual twist a particle accumulates descending one generation reappears
as the residual misalignment of the neutrino against the charged-lepton basis: the same
rotor defect, two independent observables. That is what makes the $+10.6\%$ bracket a real
cross-prediction rather than a fit.

**$\theta_{12}$ (solar) — golden-ratio mixing.** The fundamental quantum $1/\varphi$ sets
the solar angle through golden-ratio mixing,

$$\tan\theta_{12}=\frac1\varphi\;\Rightarrow\;\theta_{12}=31.72^\circ,\quad
\sin^2\theta_{12}=\frac{1}{1+\varphi^2}=\frac{1}{2+\varphi}=0.2764$$

(using $\varphi^2=\varphi+1$, so $1+\varphi^2=2+\varphi$ — verified exactly).

Measured $33.46^\circ$ ($\sin^2=0.304$): a $-5.2\%$ bracket in the angle. *Honest
attribution:* the pattern $\tan\theta_{12}=1/\varphi$ already exists in the neutrino
literature (golden-ratio mixing, Everett–Ramond / Datta et al.) — here it is a
consistency hit, the framework supplying the *reason* the relevant constant is $1/\varphi$
(the golden boost quantum per shell), not an original numerical discovery.

**$\theta_{23}$ (atmospheric) — now-surface equal weight.** The now-projector
$P_{\text{now}}=\tfrac12(I+T)=\text{diag}(1,0)$ reads the two temporal sheets with
**equal weight $\tfrac12$** (note 14). Equal weight between the second and third families
forces maximal $2$–$3$ mixing, $\theta_{23}=45^\circ$. Measured $42^\circ$–$49^\circ$ —
consistent, but this is the *weakest* leg: maximal mixing is generic to many models, and
the framework adds little beyond the equal-weight readout.

The pattern — small $\theta_{13}$, large $\theta_{12}$, near-maximal $\theta_{23}$ — is
exactly the observed PMNS structure, and it is the *opposite* of the small CKM-style
mixing one would get from the off-node charged-lepton rotor, because the on-node neutrino
basis is maximally delocalized (osc$=\tfrac12$, the equidistribution floor).

## Extension — the Dirac CP-violation magnitude as the rotor's hyperbolic shadow

The PMNS matrix has a fourth observable the angles above do not touch: the Dirac
CP-violating phase $\delta_{CP}$. The framework predicts it from the *same* rotor defect
that fixed $\theta_{13}$, now read through the boost group rather than the compact rotor.

The charged-lepton generation operator is the **compact** rotation $\mathsf R(\delta\theta_g)\in SO(2)$
(04). Its boost-group sibling, acting on the *same* defect angle but in the
non-compact $SO(1,1)$ that governs depth (10), is the half-boost of note 07 evaluated at
the rotor defect. The CP phase is the argument that the neutrino mass eigenstate
$\mathbf V(\theta)$ acquires when transported through the rotor defect against the
on-node real axis — the hyperbolic analogue of a Berry phase, the area swept in the
$(G_{\text{sym}},G_{\text{flow}})$ plane between the charged and neutral bases:

$$\boxed{\;\big|\delta_{CP}-\pi\big|\;=\;\big|\delta\theta_g\big|\,\varphi^{p},\quad p\in\{1,2\}
\;\Rightarrow\;\big|\delta_{CP}-\pi\big|\in[15.3^\circ,\,24.7^\circ].\;}$$

The structure: the bare defect $|\delta\theta_g|$ is amplified by a golden terrace factor
$\varphi^p$ (the depth weight of note 14, where $\varphi^2$ multiplies the now-Hessian
$H=\text{diag}(\tfrac12,-1,-\tfrac89)$) because the phase is accumulated over the boost arc,
not the compact angle; and it is referred to $\pi$ because CP violation is the *deviation
from the time-reversal-even point* $\delta_{CP}=\pi$ (the $T$-fixed locus, note 14,
$P_{\text{now}}=\tfrac12(I+T)$).

**Honest reading — order, not a pinned value, and not the sign.** Unlike the integers
$78$ and $12$ in $\theta_{13}$ (which note 04 *forces* from the lepton tower), the **power
of $\varphi$ here is not forced**: $p=1$ gives $15.3^\circ$, $p=2$ gives $24.7^\circ$, and
the framework does not yet derive which. I will not sharpen it to a single value it has not
earned, nor tune $p$ to the data. The honest claim is an **order-of-magnitude prediction**:
leptonic CP violation $|\delta_{CP}-\pi|=O(|\delta\theta_g|\varphi)\sim15$–$25^\circ$,
*near-maximal but not maximal*, sourced by the same rotor defect that fixes $\theta_{13}$.
The measured best fit ($\delta_{CP}\simeq197^\circ$, i.e. $|\delta_{CP}-\pi|=17^\circ$) sits
inside this bracket. **Two further caveats:** (i) the *sign relative to $\pi$ is open* —
$155^\circ<\pi$ (the $p=2$ value) vs measured $197^\circ>\pi$ are on opposite sides, so
$\sin\delta_{CP}$ flips sign ($+0.42$ vs $-0.29$); the framework fixes the *magnitude* of CP
violation, not its octant. (ii) The prediction is genuinely that CP is violated at the
$\sim20^\circ$ level — a falsifiable statement (rules out $\delta_{CP}=\pi$ exactly).
Generation spacing $\Delta_g$, reactor angle $\theta_{13}$, and the CP-violation *magnitude*
all descend from the single constant $\delta\theta_g=78\ln\varphi-12\pi$.

## Prediction

- **$\theta_{13}=|\delta\theta_g|=9.43^\circ$** (vs measured $8.53^\circ$, $+10.6\%$;
  $\sin^2\theta_{13}=0.0268$ vs $0.0220$, $+22\%$). The reactor angle equals the
  charged-lepton generation-rotor defect — a parameter-free cross-prediction; the
  integers $78=2\Delta_g$ and $12$ are forced by the charged-lepton tower, not by neutrinos.
- **Unified mass law $m_\nu(m)=\sqrt{\Delta m^2_{32}}\,\sinh(m\Delta k/\varphi)/\sinh(2\Delta k/\varphi)$**:
  seesaw scale $\times$ node-ladder texture, one formula. $m_1=0$, and $m_2=0.0065$ eV vs
  measured $\sqrt{\Delta m^2_{21}}=0.0086$ eV ($-24\%$).
- **Normal ordering, $m_1=0$** (lightest $=$ the $m=0$ now-seed node, $G_{\text{flow}}(0)=0$;
  + the monotone $\sinh$ ladder); hence $\Sigma m_\nu\simeq0.0587$ eV given the measured
  splittings ($<0.12$ eV Planck+BAO).
- **$m_2/m_3=\sinh\theta_1/\sinh\theta_2=0.131$** (node ordinals $m=1,2$, $\theta_m=m\Delta k/\varphi$;
  vs measured $0.172$, $-24\%$) — a parameter-free framework output.
- **$\theta_{12}=31.72^\circ$** ($\tan\theta_{12}=1/\varphi$, $\sin^2=1/(2+\varphi)$; vs
  $33.46^\circ$, $-5.2\%$); **$\theta_{23}=45^\circ$** (now-surface equal weight).
- **$|\delta_{CP}-\pi|=|\delta\theta_g|\varphi^p\in[15.3^\circ,24.7^\circ]$** ($p\in\{1,2\}$,
  power not forced; measured $\simeq197^\circ$ gives $|\delta_{CP}-\pi|=17^\circ$, *inside* the
  bracket). The framework predicts the *order* of CP violation (near- but not- maximal,
  $\sim20^\circ$) from the same rotor defect as $\theta_{13}$; the **power of $\varphi$ and the
  octant/sign relative to $\pi$ are both left open** — a magnitude prediction, not a phase one.
- Seesaw places $M_R\simeq10^{10}$–$10^{14}$ GeV (mass-ladder ordinal $\sim330$, near the
  horizon/GUT shell $N_\star=291.88$).

**Falsifier:** a reactor angle pinned well below $\sim9^\circ$ at many $\sigma$ (excluding
$|\delta\theta_g|$), or confirmation of **inverted** ordering — either kills the
near-null/now-seed identification ($m_1\approx0$ requires $G_{\text{flow}}(0)=0$ to be the
mass floor). A measured $\delta_{CP}$ pinned at exactly $\pi$ (CP-conserving), or with
$|\delta_{CP}-\pi|$ far outside the predicted $15$–$25^\circ$ band, at many $\sigma$ would kill
the rotor-shadow CP-magnitude prediction.
