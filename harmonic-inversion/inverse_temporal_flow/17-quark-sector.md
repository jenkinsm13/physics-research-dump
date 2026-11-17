# 17 — The Quark Sector and CKM from the Rotor

*Round-3 frontier note. Builds on the now-closed boost group: the master vector
$\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$, with one shell $=$ the
boost $\Lambda(1/\varphi)$ (note 10); the lepton sector as the **compact real form**
$SO(2)$ rotor $\mathsf R(\delta\theta_g)$ at ordinals $24/63/102$, step $39$, with the
exact generator $\delta\theta_g=78\ln\varphi-12\pi=-0.16459$ (note 04); and the
spin-$\tfrac12$ half-boost putting **fermions on the $\text{osc}=\tfrac12$ nodes** of the
flow-reversal lattice (note 07). The leptons are a clean equispaced rotor orbit. The
quarks are the **same rotor, strained** — and that strain, read through the
mass-ratio$\leftrightarrow$ordinal bridge, identifies the Cabibbo angle with a half-boost
chord. Every algebraic identity below is confirmed to machine precision in
`verify/verify_quark-sector.py`; every physical comparison is printed with its honest
miss; and — the central honesty point of this note — the headline number is shown to be
**numerically the Gatto–Sartori–Tonin relation $\sqrt{m_d/m_s}$ with $\varphi$ and the
calibration slope cancelling out**. The framework's claim is therefore *structural* (what
kind of object $\lambda$ is), not a new digit.*
$\varphi=(1+\sqrt5)/2$, $\ln\varphi=0.4812118$, $1/\varphi=0.6180340$.

---

## 1. The mass map and the ordinal of every quark

The lepton calibration (note 04) is an affine ordinal$\to$log-mass law, $\ln m=ak+b$,
fixed by the three equispaced charged leptons to
$$a=\frac{\ln m_\tau-\ln m_e}{102-24}=0.1045383,\qquad e^{39a}=58.968=\sqrt{\tfrac{m_\mu}{m_e}\tfrac{m_\tau}{m_\mu}},$$
the slope being the geometric-mean generation step (a §4-04 consistency seal,
residual $<10^{-6}$). Crucially $a\ne\ln\varphi$: mass runs as
$m\sim\varphi^{(a/\ln\varphi)\,k}=\varphi^{0.21724\,k}$, so the **mass-ordinal scale is a
fixed rescaling of the shell ladder** $r_n=r_0\varphi^n$ — the same boost flow, read on
the mass axis. Inverting $k=(\ln m-b)/a$ on the PDG-2024 quark masses (up/down/strange
at $2\,$GeV $\overline{\text{MS}}$, charm/bottom at their own mass, top pole) gives the
quark ordinals:

| quark | $m$ (MeV) | ordinal $k$ | type |
|---|---|---|---|
| $u$ | $2.16$ | $37.79$ | up |
| $d$ | $4.70$ | $45.23$ | down |
| $s$ | $93.5$ | $73.83$ | down |
| $c$ | $1273$ | $98.81$ | up |
| $b$ | $4183$ | $110.19$ | down |
| $t$ | $172570$ | $145.77$ | up |

**Honest first fact:** unlike the leptons, the quarks are *not* equispaced. Up-type
steps are $c-u=61.0$ and $t-c=47.0$; down-type steps $s-d=28.6$ and $b-s=36.4$. The
quark sub-lattice is a **strained rotor orbit**, not a rigid one. This strain is not a
defect of the model — it *is* the physical content of CKM: a rigid rotor (leptons)
diagonalizes with no mixing; a strained one (quarks) has up- and down-type mass
eigenbases that are rotated relative to each other, and that misalignment is the CKM
matrix.

## 2. The rotor-chord bridge: a mass ratio *is* a half-boost chord

The boost group makes one identity exact and load-bearing. Because $\ln m$ is linear in
$k$, every mass ratio is a pure exponential of an ordinal gap:
$$\boxed{\;\frac{m_i}{m_j}=e^{a(k_i-k_j)}=\varphi^{(a/\ln\varphi)(k_i-k_j)}\;}$$
and therefore the *square root* of a mass ratio is the chord swept by **half** that
ordinal advance — exactly the half-boost of note 07, the $SL(2,\mathbb R)$ double cover
written on the mass axis:
$$\sqrt{\frac{m_i}{m_j}}=\exp\!\Big(\tfrac{a}{2}(k_i-k_j)\Big)
=\varphi^{\frac{a}{2\ln\varphi}(k_i-k_j)}.$$
Verified to $10^{-12}$: $\sqrt{m_d/m_s}=\varphi^{a(k_d-k_s)/(2\ln\varphi)}=0.224204$. A
generation-mixing amplitude in this framework is therefore not a free Yukawa angle but a
**half-boost chord between two ordinals** — the same object that gave fermions their
$4\pi$ period (note 07) and the leptons their $\theta/2$ transport.

### 2a. The calibration cancels — read the box honestly

The boxed exponent looks like it carries information from $\varphi$ and the lepton slope
$a$. It does not. Substitute $k_i-k_j=(\ln m_i-\ln m_j)/a$ from the §1 inversion:
$$\varphi^{\frac{a}{2\ln\varphi}(k_i-k_j)}
=\exp\!\Big[\ln\varphi\cdot\tfrac{a}{2\ln\varphi}\cdot\tfrac{\ln m_i-\ln m_j}{a}\Big]
=\exp\!\Big[\tfrac{\ln m_i-\ln m_j}{2}\Big]=\sqrt{\frac{m_i}{m_j}}\quad\text{identically.}$$
$\ln\varphi$ cancels, $a$ cancels, and the intercept $b$ never entered. **The number is a
function of $m_d,m_s$ alone.** This is confirmed to $<3\times10^{-17}$ in the verify
script (the "framework route" and the bare $\sqrt{m_d/m_s}$ agree to roundoff). The
framework does **not** add a digit to $\sqrt{m_d/m_s}$; what it adds is an *interpretation*
— that this particular function of the masses is the half-boost chord on the inversion
circle, the same algebraic object (note 07) that the spin-$\tfrac12$ double cover and the
lepton $\theta/2$ transport are built from. The content is structural, not numerical, and
calling it "$\varphi$-predicted" would be a fudge. We do not.

## 3. The Cabibbo angle is the down-sector half-chord — what is and is not claimed

The Standard-Model texture relation of Gatto–Sartori–Tonin (GST, 1968) states that the
Cabibbo angle is fixed by the down-sector mass ratio, $\sin\theta_c\simeq\sqrt{m_d/m_s}$.
In our language this is the down-type half-boost chord between ordinals $45.23$ and
$73.83$:
$$\boxed{\;\lambda\;=\;\sin\theta_c\;\overset{\text{GST}}{\simeq}\;\sqrt{\frac{m_d}{m_s}}
\;=\;\varphi^{\frac{a}{2\ln\varphi}(k_d-k_s)}\;=\;0.22420.\;}$$

**What the framework owns** is the *identification* of the GST chord with the half-boost
object — a structural claim that makes the GST relation *mandatory* in this picture
(generation mixing has nowhere else to live but a chord between ordinals) rather than an
empirical coincidence. **What it does not own** is the digit $0.22420$: that is GST, set
by $m_d/m_s$ alone, as §2a proves.

Against PDG-2024 $\lambda=0.22500$ this is a $0.4\%$ miss; against $|V_{us}|=0.22431$ it
is a $0.0\%$ miss; the implied $\theta_c=12.96^\circ$ versus the measured $13.04^\circ$ is
a $0.6\%$ miss. **But the honest error bar is set by the input, not by the agreement.**
$m_d=4.70^{+0.48}_{-0.17}\,$MeV carries $\sim10\%$ uncertainty, so the half-chord spans
$$\sqrt{m_d/m_s}\in[0.220,\,0.235]\quad(m_d\in[4.53,5.18]\,\text{MeV at }2\,\text{GeV}),$$
a band $\sim50\times$ wider than the $0.85\times10^{-3}$ error on $|V_{us}|$. The famous
$0.4\%$ agreement is **GST's** well-known success and it rides on the lattice
determination of $m_d/m_s$; it is not a sharp numerical prediction of *this* framework.
The framework's falsifiable content is the *structural* claim of §5, plus the
self-consistency seal that the lepton-fixed ordinal lattice reproduces GST exactly (§2a).

The bare lepton rotor angle does *not* give this number on its own — and that, too, is an
honesty point. The compact-$SO(2)$ step is $|\delta\theta_g|=0.16459$ (note 04), and
$\sin|\delta\theta_g|=0.1638$ lands $\sim27\%$ *low* of $\lambda$. So the rotor sets the
*kind* of object (a half-boost chord on the inversion circle); the measured down-sector
ordinal gap sets its *length*. The two are different statements and we keep them separate.

## 4. The CKM hierarchy $\lambda,\lambda^2,\lambda^3$ — honest brackets, not hits

Wolfenstein organizes the matrix as $|V_{us}|\sim\lambda$, $|V_{cb}|\sim A\lambda^2$,
$|V_{ub}|\sim A\lambda^3\sqrt{\rho^2+\eta^2}$. The framework reproduces the **ladder of
powers** because each step down a generation is one more half-chord, but at $\lambda^2$
and $\lambda^3$ the agreement *fails as a pure prediction* and survives only as a bracket:

- **$|V_{us}|\sim\lambda=0.2242$** vs $0.2243$ — $0.0\%$. (§3; this is GST, see caveat.)
- **$|V_{cb}|\sim\lambda^2=0.0503$** vs $0.0408$ — **high by $23\%$.** The residual is the
  Wolfenstein $A=|V_{cb}|/\lambda^2=0.812\ne1$. The single-sector $2\!\to\!3$ chords do
  *not* rescue it: the down cross-chord $\sqrt{m_s/m_b}=0.150$ overshoots by $266\%$ and
  the linear $m_s/m_b=0.0224$ undershoots by $45\%$. They bracket $V_{cb}=0.0408$
  ($0.0224<0.0408<0.150$) but the bracket is wide and unselective — this is **not** a
  framework win, it is the honest statement that $V_{cb}$ requires the unexplained
  $A\approx0.81$.
- **$|V_{ub}|\sim\lambda^3=0.0113$** vs $0.00382$ — **high by $195\%$ (factor $\sim3$).**
  The down $1\!\to\!3$ chord $\sqrt{m_d/m_b}=0.0335$ overshoots even worse. The ratio
  $|V_{ub}/V_{cb}|=0.094$ sits *above* the up-sector chord $\sqrt{m_u/m_c}=0.041$ (which
  undershoots by $56\%$); the residual factor is the unitarity-triangle apex
  $\sqrt{\rho^2+\eta^2}\approx0.42$. That factor is genuinely a **modulus the chord cannot
  supply** — it carries the CP phase, whose natural seat in the framework is the $SO(2)$
  rotor phase $\delta\theta_g$ (note 04), not the half-boost modulus.

So the framework **predicts the power-ladder structure** $\{\lambda,\lambda^2,\lambda^3\}$
and (via GST) matches $\lambda$, while $A$ and the CP apex are **unexplained residuals it
only brackets**. We state this without dressing: $\lambda^2$ is $+23\%$, $\lambda^3$ is
$\times3$, and the cross-sector chords do not close the gap.

## 5. Why quarks strain and leptons do not — the parity class (the structural claim)

Note 07 placed bosons on the lattice peaks ($\text{osc}=1$) and fermions on the nodes
($\text{osc}=\tfrac12$, the self-coupling shell $c(0)$), interleaved at the half-period
$P/2$. The doubled-depth half-boost shell lands exactly on $\text{osc}(2k_n)=\tfrac12$
(verified to $10^{-12}$). Leptons, being color singlets, ride the **rigid** compact rotor
— their three ordinals are exactly equispaced ($\Delta_g=39$), so their up-type-like and
down-type-like mass bases coincide and there is no lepton CKM at tree level (matching the
near-diagonal PMNS-at-tree intuition). Quarks carry color; their ordinals are the rotor
orbit **pulled off equispacing** by the QCD-scale dressing of the half-boost node, the
strain being the $61/47$ vs $29/36$ asymmetry of §1. The Cabibbo angle is the
**misalignment chord** between the strained down sub-lattice and the strained up
sub-lattice — small because the strain is small, and identified with $\sqrt{m_d/m_s}$
because that is the down-sector half-chord. *This* — "CKM = misalignment of two strained
sub-lattices of one rotor, and generation mixing is structurally a half-boost chord" — is
the framework's actual, falsifiable assertion. The number $0.2242$ is GST's; the
*reason GST must hold* is ours.

## Extension — the CP apex as the accumulated rotor phase

The one place §4 found a residual that the half-boost chord *structurally cannot* supply
is the CP apex $\sqrt{\rho^2+\eta^2}\approx0.42$ in $|V_{ub}|$: a chord carries a modulus,
but a phase needs the **compact sibling** of the boost — the $SO(2)$ rotor of note 04,
whose generator is the imaginary rotation $iK$ (the Wick-rotated boost, $\theta\to i\theta$
at fixed ordinal lattice — *not* literal $k\to ik$). The boost group thus splits CKM
cleanly: **half-boost chords on the non-compact $SO(1,1)$ leg give the moduli
$\{\lambda,\lambda^2,\lambda^3\}$; the compact $SO(2)$ rotor phase $\delta\theta_g$ gives
the single CP angle.** The natural candidate for the apex is the rotor phase accumulated
across the two generations that separate $u$ and $b$ — a *two-step* rotor advance, the
phase analogue of the $\lambda^2$ chord:
$$\boxed{\;\sqrt{\rho^2+\eta^2}\;\sim\;\sin\!\big(2\,|\delta\theta_g|\big)
=\sin(0.3292)=0.3233.\;}$$
Against the global-fit apex $\sqrt{\bar\rho^2+\bar\eta^2}=0.383$ this is **$16\%$ low** —
an honest bracket, not a hit: the measured apex sits between the two- and three-step rotor
advances, $\sin(2|\delta\theta_g|)=0.323<0.383<\sin(3|\delta\theta_g|)=0.474$. The content
is structural and *parameter-free*: the CP-violating apex is a low integer multiple of the
**lepton-fixed** rotor step $\delta\theta_g=78\ln\varphi-12\pi$ (note 04) — unlike the
chord moduli, this number genuinely carries $\varphi$, because $\delta\theta_g$ does. The
sharp falsifiable claim: the unitarity-triangle apex is $\sin$ of an integer multiple of
$0.16459$, and a future global fit driving the apex outside $[0.32,0.47]$ kills the
identification of the CP phase with the compact rotor.

## Extension B — the strain ratio as a one-shot Wolfenstein $A$

If §5 is right, the down/up strain asymmetry should itself carry the prefactor $A$ that
§4 left unexplained. Define the **strain ratio** of the two sub-lattices from the §1
ordinal steps, comparing the $2\!\to\!3$ gaps that build $V_{cb}$ to the $1\!\to\!2$ gaps
that build $\lambda$:
$$\boxed{\;A_{\text{strain}}\;=\;\sqrt{\frac{(k_s-k_d)_{\downarrow}\,(k_c-k_u)_{\uparrow}}
{(k_b-k_s)_{\downarrow}\,(k_t-k_c)_{\uparrow}}}
=\sqrt{\frac{(s\!-\!d)(c\!-\!u)}{(b\!-\!s)(t\!-\!c)}}\;}$$
i.e. the geometric mean of the first-rung steps relative to the second-rung steps across
both sectors. Numerically, on the full-precision ordinals (steps
$(s\!-\!d,b\!-\!s)=(28.61,36.36)$, $(c\!-\!u,t\!-\!c)=(61.02,46.96)$),
$$A_{\text{strain}}=\sqrt{\frac{28.61\times61.02}{36.36\times46.96}}=1.011$$
(the rounded-gap shorthand $\sqrt{28.6\cdot61.0/(36.4\cdot47.0)}=1.010$ rounds the same
number), which does **not** reproduce $A=0.81$ — it is high by $24.6\%$, the same sign and
nearly the same size as the raw $\lambda^2$ miss ($+23\%$).

**Same honesty caveat as §2a applies, and we state it plainly.** $A_{\text{strain}}$ is a
ratio of ordinal *gaps*, and each gap is $\Delta\ln m/a$, so the four factors of $1/a$
cancel and $\varphi$ never enters:
$$A_{\text{strain}}=\sqrt{\frac{(\ln m_s-\ln m_d)(\ln m_c-\ln m_u)}
{(\ln m_b-\ln m_s)(\ln m_t-\ln m_c)}}\quad\text{(calibration-independent, no }\varphi\text{).}$$
Like $\lambda$, it is a pure function of the six quark masses — a specific combination of
log-mass gaps, not a $\varphi$-prediction. Its content is *which* combination the strain
picks out, not a new digit. Reported honestly as a bracket: the strain ratio is of order
unity (the sub-lattices are *nearly* uniformly strained), consistent with $A=O(1)$ but not
pinning $0.81$. The prediction this makes is sharp and falsifiable: **$A$ is a ratio of
generation gaps, hence renormalization-group-scheme-dependent through the running masses,
and should drift toward $0.81$ as the quark ordinals are recomputed at a common scale**
(the table mixes $2\,$GeV, on-shell, and pole masses). If $A_{\text{strain}}$ stays
pinned at $1.0$ under a uniform-scale recomputation while measured $A$ stays at $0.81$,
the strain-ratio identification is dead and $A$ is genuinely external to the lattice.

## Prediction

- **Headline (honest):** the Cabibbo angle is the down-sector half-boost chord,
  $$\lambda=\sin\theta_c\;\overset{\text{GST}}{=}\;\sqrt{m_d/m_s}
  =\varphi^{\,a(k_d-k_s)/(2\ln\varphi)}=0.2242,$$
  versus PDG-2024 $\lambda=0.2250$ ($0.4\%$) and $|V_{us}|=0.2243$ ($0.0\%$);
  $\theta_c=12.96^\circ$ vs $13.04^\circ$ ($0.6\%$). **This is the GST relation; $\varphi$
  and the calibration slope $a$ cancel identically (§2a), so the framework supplies the
  *interpretation* (a half-boost chord), not the digit.** The honest input band from
  $m_d=4.70^{+0.48}_{-0.17}$ is $\lambda\in[0.220,0.235]$.
- **Hierarchy (bracketed, not hit):** $\{\lambda,\lambda^2,\lambda^3\}$ is the right power
  ladder, but $|V_{cb}|=\lambda^2$ is $+23\%$ ($A=0.81$ unexplained) and
  $|V_{ub}|=\lambda^3$ is $\times3$ (CP apex $\sqrt{\rho^2+\eta^2}\approx0.42$ unexplained
  by the chord modulus).
- **CP apex (boost-group native, bracketed):** the unitarity-triangle apex is the
  accumulated **compact-rotor phase**, $\sqrt{\rho^2+\eta^2}\sim\sin(2|\delta\theta_g|)
  =0.323$ vs measured $0.383$ ($-16\%$), bracketed by
  $\sin(2|\delta\theta_g|)<0.383<\sin(3|\delta\theta_g|)$. Parameter-free and genuinely
  $\varphi$-carrying (via $\delta\theta_g=78\ln\varphi-12\pi$): chord moduli live on the
  non-compact $SO(1,1)$ leg, the single CP phase on the compact $SO(2)$ leg.
- **Structural (the real claim):** quark mass-ordinals are a *strained* rotor orbit (steps
  $61/47$, $29/36$, not $39/39$); the CKM matrix is the misalignment between the up and
  down strained sub-lattices; generation mixing is a half-boost chord on the inversion
  circle. The strain ratio $A_{\text{strain}}=1.011$ (high by $24.6\%$) brackets
  $A=O(1)$ and predicts $A$ drifts toward $0.81$ under common-scale mass recomputation.

**Falsifier:** if a future lattice/global-fit determination drives $\sqrt{m_d/m_s}$ away
from $|V_{us}|$ by more than the input band (a few percent) — i.e. if the down-sector
half-chord and the measured Cabibbo angle decouple — the identification
$\lambda=\sqrt{m_d/m_s}$ as a half-boost chord on the inversion circle is dead, and the
quark sector is *not* the strained image of the lepton rotor. Likewise, if $A_{\text{strain}}$
fails to converge toward $0.81$ under a uniform-scale recomputation of the quark ordinals,
the §5 strain story does not explain the Wolfenstein prefactor; and if a future global fit
drives the CP apex outside $[0.32,0.47]=[\sin2|\delta\theta_g|,\sin3|\delta\theta_g|]$, the
identification of the CP phase with the compact-rotor advance is dead.
