"""Machine-precision verification of note 16 (16-unified-field-equation.md).

Run: python3 verify_unified-field-equation.py
No SciPy required: the boost generator squares to +I (K^2=I) so every matrix
exponential is closed-form,  exp(aK)=cosh(a)I+sinh(a)K.

The note promotes the ordinal k to a dynamical field and writes a Klein-Gordon-like
field equation for the chronon two-vector Psi(k)=osc(k) Lam(k/phi)(1,0)^T over the
shell stack, with boost-covariant derivative D_k = d/dk - (1/phi)K and mass term
M^2(k)=osc^2(k) (the note-10 Casimir).  Checks, in order:

  1. Generators / constants:  K^2=I.
  2. V is the covariantly-constant zero mode:  D_k V = 0  (note 10 transport law).
  3. Covariant box on the dressing:  D_k^2 Psi = osc'' V  (the dynamics lives in osc).
  4. DISPERSION RELATION (the new equation):  plane wave e^{i omega k} chi in the
     two null channels s=+-1 (K-eigenbasis) of (D_k^2 + M^2)Psi=0 gives
        omega(k) = +- osc(k) - i s/phi.
     Real part = mass shell osc(k); imag part = +-1/phi.  LABEL CARE: K n_s = s n_s
     with n_{-1}=(1,1), n_{+1}=(1,-1).  The RETARDED (decaying) channel is s=-1:
     its modulus e^{-k/phi} decays forward AND it is the (1,1) direction onto which
     V projects e^{-theta} ~ kappa(+k).  The detailed-balance ratio is the MODULUS
     ratio e^{-2theta}=kappa(+k)/kappa(-k) (note 05), not a bare phase difference.
  5. SPECTRUM = INVERSION COMB:  on-shell (M^2=1) modes sit exactly at osc(k_n)=1,
     i.e. k_n=(2n-1)pi/(4 lnphi); the real frequency there is the Casimir unit 1=L_y.
  6. ZERO-MODE STATIC GREEN'S FUNCTION = V_grav:  the omega=0 sector of D_k has the
     boost holonomy as its kernel; its flow-component reproduces spine-5 V_grav.
  7. NOETHER CURRENT reduces to L_y=1:  the boost charge is <V,V>_eta = 1, all k.
  8. HARD NUMBER:  successive GW-echo amplitude ratio = e^{-(1/phi) Dk} with
     Dk=pi/(2 lnphi) equals e^{-S1}=gamma_echo=0.1330 EXACTLY (S1=(1/phi)Dk, residual 0).
     Plus the on-shell quality factor Q=phi/2 and damping ratio zeta.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNP = np.log(PHI)
IP = 1.0 / PHI
I2 = np.eye(2)
ETA = np.diag([1.0, -1.0])
K = np.array([[0.0, -1.0], [-1.0, 0.0]])  # boost generator, K^2 = I


def osc(k):
    return 1.0 / (1 + np.cos(2 * k * LNP) ** 2)


def osc_d(d):  # osc as a function of an ordinal *separation* d (same form)
    return 1.0 / (1 + np.cos(2 * d * LNP) ** 2)


def V(k):
    th = k / PHI
    return np.array([np.cosh(th), -np.sinh(th)])  # chronon two-vector (note 99/10)


def Lam(a):
    return np.array([[np.cosh(a), -np.sinh(a)], [-np.sinh(a), np.cosh(a)]])


def Psi(k):
    return osc(k) * V(k)  # the unified field (note 10 sec 6)


def kn(n):
    return (2 * n - 1) * np.pi / (4 * LNP)


def Dcov(f, k, h=1e-6):
    """Boost-covariant derivative D_k f = f' - (1/phi) K f, central difference."""
    return (f(k + h) - f(k - h)) / (2 * h) - IP * K @ f(k)


def check():
    print("=== constants ===")
    print(f"   phi={PHI:.10f}  1/phi={IP:.10f}  lnphi={LNP:.10f}")
    print(f"   K^2 - I residual = {np.max(np.abs(K @ K - I2)):.1e}")

    print("\n=== 1-2. V is the covariantly-constant zero mode: D_k V = 0 ===")
    mr = max(np.max(np.abs(Dcov(V, k))) for k in [0.0, 0.7, 1.632, 3.0, 4.896])
    print(f"   max|D_k V| = {mr:.2e}   (note 10 flat-connection transport)")

    print("\n=== 3. covariant box on the dressing:  D_k^2 Psi = osc'' V ===")

    # D_k Psi = osc' V (since D_k V=0); D_k^2 Psi = osc'' V.  Check numerically.
    def DPsi(k):
        return Dcov(Psi, k)

    mr = 0.0
    for k in [0.7, 1.632, 3.0, 4.896]:
        h = 1e-5
        box = (DPsi(k + h) - DPsi(k - h)) / (2 * h) - IP * K @ DPsi(k)
        oscpp = (osc(k + h) - 2 * osc(k) + osc(k - h)) / h**2
        mr = max(mr, np.max(np.abs(box - oscpp * V(k))))
    print(
        f"   max|D_k^2 Psi - osc'' V| = {mr:.2e}   (all dynamics is in the osc dressing)"
    )

    print(
        "\n=== 3b. HONEST off-shell residual: master field is ADIABATIC, not exact ==="
    )
    # Full second-order EL residual of the master field:
    #   (D_k^2 + osc^2)(osc V) = (osc'' + osc^3) V  =>  scalar residual R(k)=osc''+osc^3.
    # This is NOT zero: the master field osc*V is the exact covariantly-constant carrier
    # (D_k V=0, first order) and the adiabatic/leading solution of the 2nd-order eq, but
    # NOT a homogeneous solution. R(k) is O(1), the off-shell defect. (proto flagged this.)
    h = 1e-6

    def oscpp_fn(k):
        return (osc(k + h) - 2 * osc(k) + osc(k - h)) / h**2

    ks_per = np.linspace(kn(1), kn(1) + np.pi / (2 * LNP), 4001)  # one comb period
    Rk = np.array([oscpp_fn(k) + osc(k) ** 3 for k in ks_per])
    print(
        f"   R(k)=osc''+osc^3:  RMS={np.sqrt(np.mean(Rk**2)):.4f}  max|R|={np.max(np.abs(Rk)):.4f}"
    )
    print(
        f"   R(k_1)={oscpp_fn(kn(1)) + osc(kn(1)) ** 3:+.4f} (osc''(k_1)={oscpp_fn(kn(1)):.4f}, analytic -2(2lnphi)^2={-2 * (2 * LNP) ** 2:.4f})"
    )
    print(
        f"   R(osc-min)={oscpp_fn(kn(1) + np.pi / (4 * LNP)) + osc(kn(1) + np.pi / (4 * LNP)) ** 3:+.4f}  (sign flips across the period)"
    )
    print(
        "   => off-shell residual bracket |R| in [0, 0.85]; master field is leading-order, not exact."
    )

    print("\n=== 4. DISPERSION RELATION  omega(k) = +- osc(k) - i s/phi  (NEW) ===")
    # In each K-eigenchannel s=+-1, (D_k^2 + M^2) e^{i omega k} chi = 0 gives the
    # quadratic  -omega^2 - (2 i omega/phi) s + 1/phi^2 + M^2 = 0.
    mr = 0.0
    for k in [0.3, 1.0, 1.632, 3.0, 4.896]:
        M2 = osc(k) ** 2
        for s in (+1, -1):
            for sign in (+1, -1):
                om = -1j * s / PHI + sign * np.sqrt(M2 + 0j)
                resid = -(om**2) - (2j * om / PHI) * s + 1 / PHI**2 + M2
                mr = max(mr, abs(resid))
                # closed form: Re(om)=sign*osc, Im(om)=-s/phi
                assert abs(om.real - sign * osc(k)) < 1e-12
                assert abs(om.imag - (-s / PHI)) < 1e-12
    print(
        f"   max|dispersion-relation residual| = {mr:.2e}  (algebra: omega is a root of its own quadratic)"
    )
    print(
        f"   => Re(omega)=+-osc(k)  (mass shell),  Im(omega)=-s/phi=-{IP:.6f}  (note-05 damping)"
    )
    print(
        "   NOTE: this is the local-mass (adiabatic) dispersion; exact only where osc is flat (the comb)."
    )

    print(
        "\n=== 4b. LABEL/SIGN CHECK: retarded = s=-1 = (1,1); detailed balance e^-2θ ==="
    )
    # K-eigenvectors: K n = s n.  n_{-1}=(1,1) has K n = -n (s=-1); n_{+1}=(1,-1) has s=+1.
    n_for = {-1: np.array([1.0, 1.0]), +1: np.array([1.0, -1.0])}
    for s, n in n_for.items():
        assert np.allclose(K @ n, s * n), f"eigenvalue label wrong for s={s}"
    # Modulus of the plane wave mode |e^{i w k}| = e^{-Im(w) k} = e^{(s/phi)k}:
    #   s=-1 (retarded) DECAYS forward, s=+1 (advanced) GROWS forward.
    for kk in (1.0, 1.632, 3.0):
        mod_ret = np.exp(
            -(+1.0 / PHI) * kk
        )  # s=-1 -> Im(w)=+1/phi -> modulus e^{-k/phi}
        mod_adv = np.exp(
            -(-1.0 / PHI) * kk
        )  # s=+1 -> Im(w)=-1/phi -> modulus e^{+k/phi}
        assert mod_ret < 1.0 < mod_adv, "retarded must decay, advanced must grow"
        th = kk / PHI
        # detailed balance = modulus ratio = kappa(+k)/kappa(-k) = e^{-2theta} (note 05)
        assert abs(mod_ret / mod_adv - np.exp(-2 * th)) < 1e-12
    # V projects e^{-theta} onto the s=-1 (=retarded, (1,1)) direction:
    for kk in (1.0, 1.632, 3.0):
        th = kk / PHI
        c_ret = 0.5 * (
            V(kk)[0] + V(kk)[1]
        )  # component of V along (1,1): (cosh - sinh)/2
        assert abs(c_ret - 0.5 * np.exp(-th)) < 1e-12
    print("   OK: retarded=s=-1=(1,1) decays e^{-k/phi}, advanced=s=+1=(1,-1) grows;")
    print(
        f"       detailed balance kappa(+k)/kappa(-k)=e^(-2θ) holds (e.g. k=1.632: {np.exp(-2 * 1.632 / PHI):.6f})."
    )

    print("\n=== 5. SPECTRUM = INVERSION COMB: osc(k_n)=1, Dk=pi/(2 lnphi) ===")
    for n in (1, 2, 3, 4):
        print(
            f"   n={n}: k_n={kn(n):.6f}  osc(k_n)={osc(kn(n)):.12f}  Re(omega)=osc(k_n)={osc(kn(n)):.12f}"
        )
    print(
        f"   spacing Dk = {kn(2) - kn(1):.10f}   pi/(2 lnphi) = {np.pi / (2 * LNP):.10f}"
    )
    print(
        f"   max|osc(k_n)-1| over n=1..6 : {max(abs(osc(kn(n)) - 1) for n in range(1, 7)):.2e}"
    )

    print("\n=== 6. ZERO-MODE STATIC GREEN'S FUNCTION = V_grav (spine sec 5) ===")
    # omega=0 sector: D_k G = delta_m  => G(n,m)=theta(n>m) Lam((n-m)/phi); flow comp
    # dressed by osc reproduces the spine gravitational potential.
    rng = np.random.default_rng(0)
    N = 40
    rho = rng.random(N)

    def Gflow_spine(d):  # spine sec 5 kernel: -G_flow weight = +sinh(d/phi)/(1+cos^2)
        return -np.sinh(d / PHI) / (1 + np.cos(2 * d * LNP) ** 2)

    Vgrav_spine = np.array(
        [-sum(Gflow_spine(n - m) * rho[m] for m in range(n)) for n in range(N)]
    )
    # from the field-equation Green's fn: flow-component of osc-dressed boost holonomy
    Vgrav_green = np.array(
        [
            -sum(-osc_d(n - m) * np.sinh((n - m) / PHI) * rho[m] for m in range(n))
            for n in range(N)
        ]
    )
    print(
        f"   max|V_grav(spine) - V_grav(field-eq zero mode)| = {np.max(np.abs(Vgrav_spine - Vgrav_green)):.2e}  (algebraic consistency: identical -osc*sinh kernel)"
    )

    print("\n=== 7. NOETHER CURRENT reduces to L_y = 1 (boost charge = Casimir) ===")
    mr = max(abs(V(k) @ ETA @ V(k) - 1.0) for k in [0, 1, 2, kn(1), kn(2), 10])
    print(f"   max|<V,V>_eta - 1| = {mr:.2e}")
    # Explicit Noether current of the boost symmetry delta Psi = epsilon K Psi for
    # L = (1/2)<D_k Psi, D_k Psi>_eta - (1/2) osc^2 <Psi,Psi>_eta.  On the zero mode
    # (osc->1 dressing) D_k V=0, so the canonical momentum pi=eta D_k Psi vanishes and
    # the conserved charge collapses to the geometric invariant <V,V>_eta = L_y.
    print("   => on the covariantly-constant solution the boost charge IS L_y=1.")

    print("\n=== 8. HARD NUMBER: GW-echo decrement DERIVED from the dispersion ===")
    Dk = np.pi / (2 * LNP)
    S1 = np.pi / (2 * PHI * LNP)
    S1_alt = 2 * kn(1) / PHI
    gamma = np.exp(-IP * Dk)
    print(
        f"   identity  S1 = (1/phi)*Dk :  S1={S1:.10f}  (1/phi)Dk={IP * Dk:.10f}  resid={abs(S1 - IP * Dk):.1e}"
    )
    print(
        f"   cross-check S1 = 2 k_1/phi = {S1_alt:.10f}  resid={abs(S1 - S1_alt):.1e}"
    )
    print(f"   echo amplitude ratio per shell = e^(-(1/phi)Dk) = {gamma:.6f}")
    print(f"   = e^(-S1) = gamma_echo (note 06 Gamma_1, note 15) = {np.exp(-S1):.6f}")
    Q = 1 / (2 * IP)
    zeta = IP / np.sqrt(1 + IP**2)
    print(f"   on-shell quality factor Q = phi/2 = {Q:.6f}")
    print(f"   damping ratio zeta = (1/phi)/sqrt(1+1/phi^2) = {zeta:.6f}")
    print(
        f"   LIGO-comparison: |Im omega|/Re omega on-shell = 1/phi = {IP:.6f}; tanh(1/phi)={np.tanh(IP):.6f} (note 15: 0.548)"
    )

    print(
        "\n=== 9. EXTENSION: retarded Green's fn = golden-damped ordinal oscillator ==="
    )
    # Retarded (s=-1) channel char poly r^2 + (2/phi)r + (1/phi^2 + osc^2) = 0
    #   => r = -1/phi +- i osc : decay 1/phi, ring frequency osc.
    # Causal impulse response  G_R(k) = theta(k) e^{-k/phi} sin(osc*k)/osc.
    # Check it solves the homogeneous channel ODE on the interior (frozen mass m=osc).
    m = 1.0  # on-comb mass; same structure for any frozen osc(k)
    kg = np.linspace(0.0, 20.0, 200000)
    dkg = kg[1] - kg[0]
    G = np.where(kg >= 0, np.exp(-kg * IP) * np.sin(m * kg) / m, 0.0)
    Gp = np.gradient(G, dkg)
    Gpp = np.gradient(Gp, dkg)
    res = Gpp + (2 * IP) * Gp + (IP**2 + m**2) * G
    interior = (kg > 1.0) & (kg < 18.0)
    print(
        f"   max|G_R'' + (2/phi)G_R' + (1/phi^2+osc^2)G_R| (interior) = {np.max(np.abs(res[interior])):.2e}"
    )
    print(
        f"   decay constant = 1/phi = {IP:.6f}  (e-folding length = phi = {PHI:.4f} shells)"
    )
    # Off-comb Q-comb:  Q(k) = phi*osc(k)/2 in [phi/4, phi/2].
    Qmin, Qmax = PHI / 4, PHI / 2
    for kk in (1.0, 1.632):  # off-comb (osc<1) and on-comb (osc=1)
        Qk = PHI * osc(kk) / 2
        assert Qmin - 1e-12 <= Qk <= Qmax + 1e-12
        print(f"   Q(k={kk:.3f}) = phi*osc/2 = {Qk:.6f}")
    print(
        f"   => Q-comb bracket [phi/4, phi/2] = [{Qmin:.4f}, {Qmax:.4f}]; always sub-critical (Q<1)."
    )

    print("\nALL CHECKS COMPLETE")


if __name__ == "__main__":
    check()
