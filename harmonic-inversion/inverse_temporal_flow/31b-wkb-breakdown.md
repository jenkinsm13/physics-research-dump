# 31b — Mechanism B — Adiabatic / WKB Breakdown Depth

**Status:** Honest negative. Tests whether the adiabatic/WKB description of the charged carrier $\Psi=\mathrm{osc}\cdot V$ ceases to define a particle beyond some depth, singling out the desert depth $n_e=107.08$ (note 30). It does not: the breakdown criterion is *periodic*, not depth-monotone, and the carrier is never adiabatic to begin with, so there is nothing to "break down."

## Question addressed

This is a **(b) TERMINATION**-flavoured probe — does the charged mode stop existing at depth? — but it cannot even reach a single depth, so it answers nothing about placement either. I use the **rotor ordinal $k$** (note 16/04) throughout; the absolute Planck ordinal $n_e=107.08$ relates by the intercept $n = k + b$ (notes 04, 24), with $b$ the Planck-to-electron-shell offset. The two are never conflated below.

## The setup from note 16

In the $K$-eigenbasis the field equation $(D_k^2+M^2)\Psi=0$ reduces, after stripping the envelope $\psi_\pm=e^{\pm k/\varphi}\chi_\pm$, to
$$\chi_\pm''+\mathrm{osc}^2(k)\,\chi_\pm=0,\qquad \mathrm{osc}(k)=\frac{1}{1+\cos^2(2k\ln\varphi)},\quad \Delta k=\frac{\pi}{2\ln\varphi}=3.26425.$$
The frozen/adiabatic dispersion is $\omega(k)=\pm\,\mathrm{osc}(k)-i\,s/\varphi$. The adiabatic carrier is $\Psi=\mathrm{osc}\cdot V$ with the O(1) off-shell defect $R(k)=\mathrm{osc}''+\mathrm{osc}^3$ (RMS $0.66$, worst at the comb).

## The breakdown criterion (pre-registered, no knob)

WKB/adiabaticity requires the standard dimensionless smallness parameter built from the dispersion alone,
$$\alpha(k)=\left|\frac{M'(k)}{M^2(k)}\right|=\left|\frac{\mathrm{osc}'(k)}{\mathrm{osc}^2(k)}\right|,$$
or equivalently the relative defect $|R|/M^2=|\mathrm{osc}''+\mathrm{osc}^3|/\mathrm{osc}^2$. WKB is valid where $\alpha\ll1$; the mode "ceases to be a well-defined particle" where $\alpha\gtrsim1$. **No threshold, anchor, or integer is chosen** — the criterion is read off the equation.

## The fatal periodicity

Because $\mathrm{osc}(k)$ and every derivative are $\Delta k$-periodic, $\alpha(k)$ is **exactly periodic**:
$$\alpha(k+\Delta k)=\alpha(k)\quad\text{(verified to }1.3\times10^{-9}\text{).}$$
The closed form is clean: with $u=2k\ln\varphi$, $\mathrm{osc}'=2\ln\varphi\,\sin(2u)\,\mathrm{osc}^2$, so
$$\alpha(k)=\frac{|\mathrm{osc}'|}{\mathrm{osc}^2}=2\ln\varphi\,\bigl|\sin(4k\ln\varphi)\bigr|\in[0,\,2\ln\varphi=0.9624].$$
(An earlier draft quoted a spurious $\alpha_{\max}=1.4422$; the correct peak is exactly $2\ln\varphi=0.9624$. The verify script now self-checks the finite-difference $\alpha$ against this closed form and against the per-period gain below, both two independent corroborations.) It vanishes at the comb nodes $k_n=(2n-1)\pi/(4\ln\varphi)$ (where $\sin(4k\ln\varphi)=0$, $\mathrm{osc}'=0$, $\mathrm{osc}=1$) and reaches $\alpha_{\max}=0.96$ at the steep flanks. So the naive criterion $\alpha\sim\mathcal{O}(1)$ is met **in a band inside every period, forever** — a *comb of breakdown windows* repeating with spacing $\Delta k$, not a single deepest depth. There is no $k_\star$.

Worse: $\alpha$ reaches $\mathcal{O}(1)$ ($\alpha_{\max}=0.96$, essentially unity) **already in the first period** ($0\le k\le3.26$). Combined with $Q(k)=\varphi\,\mathrm{osc}/2\in[0.405,0.809]<1$ everywhere (sub-critical, note 16), this means **the carrier is never adiabatic anywhere** — there is no shallow adiabatic regime to "break down" *from*. The WKB description is uniformly marginal, not asymptotically valid then suddenly failing at depth. The premise of the mechanism (an adiabatic regime that ends) is empirically false.

A sharper way to see there is no bulk depth scale at all: the **per-period non-adiabaticity gain** is
$$\int_{k}^{k+\Delta k}\alpha\,dk' = \langle\alpha\rangle\,\Delta k = \Bigl(2\ln\varphi\cdot\tfrac{2}{\pi}\Bigr)\Bigl(\tfrac{\pi}{2\ln\varphi}\Bigr)=2\quad\text{(exactly, $\varphi$-independent).}$$
The accumulated non-adiabaticity grows by exactly $2$ per period — a pure integer, with no dependence on $\varphi$ and no preferred origin. A $\varphi$-independent constant simply cannot encode the log-ratio $\log_\varphi(E_P/m_e)=107.08$ of two externally supplied masses. The bulk equation has nothing in it that knows about $107$.

## Is there ANY depth-monotone rescue?

Two candidates, both parameter-free, both fail:

1. **Cumulative WKB phase** $\Phi(k)=\int_0^k\mathrm{osc}\,dk'$. Monotone but exactly *linear*: slope $=\langle\mathrm{osc}\rangle=1/\sqrt2=0.7071$ (the labelled period-mean, allowed — not a smoothing). Featureless; no preferred depth.
2. **Cumulative non-adiabaticity** $\int_0^k\alpha\,dk'$. Also linear (per-period gain $2.02$). Diverges smoothly; never crosses a parameter-free finite cutoff.

The only genuinely monotone object in the problem is the envelope $e^{\pm k/\varphi}$ — but it is a *similarity transform* removed in note 16, giving a decay **rate** ($e$-fold $=\varphi$ shells), not a cutoff. Defining "breakdown = envelope below $e^{-T}$" introduces $T$ as a free threshold (knob), giving $k_\star=T\varphi$ that slides to *any* target.

## Why this mechanism is structurally barred (the theorem behind the negative)

The failure is not bad luck with one criterion — it is forced by the *form* of the equation. $\chi''+\mathrm{osc}^2(k)\chi=0$ is **homogeneous, linear, with $\Delta k$-periodic coefficients**. By Floquet/Bloch, every solution is $\chi(k)=e^{\mu k}\,p(k)$ with $p$ exactly $\Delta k$-periodic and $\mu$ the (here purely imaginary, sub-critical) characteristic exponent. The *only* $k$-scale this equation possesses is the period $\Delta k=\pi/(2\ln\varphi)$ and the rate $1/\varphi$ in the envelope it sits inside — **both are rates per shell, neither carries a preferred origin or a preferred depth.** A translation-covariant homogeneous ODE is invariant under $k\to k+a$; it cannot single out an absolute depth $k_\star$ because it does not know where $k=0$ is in any physical sense.

But $n_e=107.08=\log_\varphi(E_P/m_e)$ is a **ratio of two externally supplied masses**. To produce it, the equation would have to contain *two pinned shells* — a source at the Planck shell and a sink/absorber at the electron shell — i.e. an **inhomogeneous** problem whose boundary data *is* the mass ratio. The homogeneous bulk equation contains neither mass. Hence:

> **No depth scale can come from the bulk; it can only come from boundary data — and the only boundary data that yields $107$ is $E_P$ and $m_e$ themselves.** To get $107$ out, one must put $E_P$ and $m_e$ in. The mechanism is circular.

This is the precise structural ingredient that is *absent* here and would be *required* to select $107$: an inhomogeneity $(D_k^2+M^2)\Psi=J(k)$ with $J$ supported at the Planck shell and a boundary condition imposed at the electron shell. That is not a derivation of the desert depth — it is a restatement of it.

## Disownment test (D1–D5)

- **D1 — NO FREE KNOB:** PASS for the criterion ($\alpha$ has zero tuned parameters) but the mechanism produces no number, so the question is moot. Any *forced* cutoff requires a threshold $T$ → that would be a knob.
- **D2 — MANDATORY CROSS-CHECK (decisive):** **FAIL / not applicable.** The mechanism yields **no unique depth**, hence predicts neither $107$ nor $63$/$102$/$92$. A rule that cannot produce one number cannot reproduce the tower. This is the controlling failure.
- **D3 — TOWER CONSISTENCY:** vacuously satisfied — with no boundary at all, $\tau$ (102) and $\mu$ (63) are trivially "inside the allowed region" (everything is). No predictive content.
- **D4 — ROBUSTNESS:** the breakdown windows are robustly periodic under any reasonable derivative discretisation; but a forced cutoff is maximally *non*-robust — to land $\{63,92,102,107,111.5\}$ one needs $T=\{38.9,56.9,63.0,66.1,68.9\}$ respectively. The knob is fully exposed.
- **D5 — 111 FAILURE FLAG:** confronted head-on. The forced-threshold knob reaches $111.5$ as easily as $107$ ($T=68.9$ vs $66.1$); landing near $111$ here would be the $N_\star/\varphi^2$ soft attractor (note 30), **not** an explanation. Reported as a failure mode, not a hit.

## Verdict

**negative.** The WKB/adiabaticity parameter $\alpha=2\ln\varphi\,|\sin(4k\ln\varphi)|$ is $\Delta k$-periodic and $\mathcal{O}(1)$ ($\alpha_{\max}=2\ln\varphi=0.96$) everywhere, so breakdown forms a repeating comb with no deepest depth; the sub-critical carrier ($Q<1$) is never adiabatic, so there is no regime to break down from; and no parameter-free depth-monotone invariant (cumulative phase with slope $1/\sqrt2$, cumulative $\int\alpha$ with the exactly-$\varphi$-independent per-period gain $2$) selects a finite cutoff. Structurally, the homogeneous periodic-coefficient bulk equation is translation-covariant — by Floquet it has only *rates* ($\Delta k$, $1/\varphi$), no preferred depth — while $107.08$ is a ratio of two external masses; a depth scale can only enter through inhomogeneous boundary data, which would *be* the mass ratio one is trying to derive (circular). The mechanism supplies no $107$, and therefore nothing to cross-check against $63/102/92$. The only monotone object, the $e^{\pm k/\varphi}$ envelope, gives a *rate* not a *cutoff*; any threshold $T$ is a knob ($k_\star=T\varphi$), and it cannot even resolve the target ($T=66.1$) from the $N_\star/\varphi^2=111.5$ attractor ($T=68.9$).

**Falsifier:** if a parameter-free, depth-monotone adiabatic invariant derived *solely* from $\chi''+\mathrm{osc}^2\chi=0$ produced a single finite cutoff matching $107$ **and** independently one of $\{63,102,92\}$, this negative would be overturned.
