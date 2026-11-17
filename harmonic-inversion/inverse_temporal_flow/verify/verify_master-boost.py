"""Machine-precision verification of note 10 (10-master-boost.md).

Run: python3 verify_master-boost.py
No SciPy required: every matrix exponential here is closed-form because the
generators square to +/-I (K^2 = I, sigma^2 = I, J^2 = -I), so
    exp(a K)     = cosh(a) I + sinh(a) K      (boost, K^2=I)
    exp((a/2) s) = cosh(a/2) I + sinh(a/2) s  (spinor, s^2=I)
    exp(d J)     = cos(d) I + sin(d) J         (rotor, J^2=-I).

Covers, in order:
  1. flow-space norm  ||V(k)||^2_eta = cosh^2 - sinh^2 = 1 = L_y, all k.
  2. one-shell descent  Lam(1/phi) V(k) = V(k+1); group law Lam(a)Lam(b)=Lam(a+b).
  3. generator  exp(aK)=Lam(a)  and the NEW boost-transport law  dV/dk=(1/phi)K V.
  4a (note 09) boost velocity  beta = -G_flow/G_sym = -V[1]/V[0] = tanh(theta).
  4b (note 05) null weight vectors n_+- ; kappa(+-k) = osc*(V[0] -+ V[1]) = osc e^{-+theta};
       detailed-balance ratio = ratio of the two boost weights = e^{-2theta}.
  4c (note 07) spinor double cover: s(a)^2 = exp(a sigma); Chebyshev cosh = 2cosh^2(./2)-1.
  4d (note 04) compact real form: rotor R(dtheta)=exp(dtheta J), det=1; R e(24)=e(63)=...
  5  Casimir / mass-shell  M^2 = G_sym^2 - G_flow^2 = osc^2 ; = 1 exactly on the shells k_n.
  6  UNIFIED FIELD STATEMENT  Psi(k) = osc(k) Lam(k/phi) (1,0)^T = (G_sym, G_flow),
       with the null projections n_-+ . Psi = kappa(+-k) reproducing both branches.
  7  EXTENSION: rapidity = hyperbolic ARC LENGTH of the flow-space worldline.
       <dV/dk, dV/dk>_eta = -1/phi^2 (spacelike), so the proper interval per shell is
       1/phi and s(k) = int_0^k sqrt|<.,.>| dk' = k/phi = theta.  Golden quantum = metric.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNP = np.log(PHI)
IP = 1.0 / PHI
I2 = np.eye(2)
ETA = np.diag([1.0, -1.0])

# Generators. K is the BOOST generator of so(1,1); K^2 = I (verified below).
K = np.array([[0.0, -1.0], [-1.0, 0.0]])  # boost
SIG = np.array([[0.0, 1.0], [1.0, 0.0]])  # spinor boost gen, sigma^2 = I
J = np.array([[0.0, -1.0], [1.0, 0.0]])  # compact (rotation) gen, J^2 = -I


def osc(k):
    return 1.0 / (1 + np.cos(2 * k * LNP) ** 2)


def V(k):
    th = k / PHI
    return np.array([np.cosh(th), -np.sinh(th)])  # chronon two-vector (note 99)


def normsq(v):
    return v @ ETA @ v  # Minkowski norm in flow-space


def Lam(a):  # boost by rapidity a
    return np.array([[np.cosh(a), -np.sinh(a)], [-np.sinh(a), np.cosh(a)]])


def expK(a):  # exp(aK) via K^2 = I
    return np.cosh(a) * I2 + np.sinh(a) * K


def expSIG(a):  # exp(a SIG) via SIG^2 = I
    return np.cosh(a) * I2 + np.sinh(a) * SIG


def expJ(d):  # exp(dJ) via J^2 = -I
    return np.cos(d) * I2 + np.sin(d) * J


def R(d):
    return np.array([[np.cos(d), -np.sin(d)], [np.sin(d), np.cos(d)]])


def e_phase(k):  # note-04 inversion-circle phase vector
    return np.array([np.cos(2 * k * LNP), np.sin(2 * k * LNP)])


def check():
    print("=== constants ===")
    print(f"   phi={PHI:.10f}  1/phi={IP:.10f}  lnphi={LNP:.10f}")
    print(f"   K^2-I residual = {np.max(np.abs(K @ K - I2)):.1e}  (boost generator)")
    print(f"   SIG^2-I residual = {np.max(np.abs(SIG @ SIG - I2)):.1e}  (spinor gen)")
    print(f"   J^2+I residual = {np.max(np.abs(J @ J + I2)):.1e}  (compact gen)")

    print("\n=== 1. flow-space norm  ||V||^2_eta = 1 = L_y  (all k) ===")
    mr = max(abs(normsq(V(k)) - 1) for k in [0, 0.3, 1, 1.632, 4.896, 8.161, 30])
    print(f"   max |||V||^2 - 1| = {mr:.2e}")

    print("\n=== 2. one-shell descent  Lam(1/phi)V(k)=V(k+1); group law ===")
    mr = max(np.max(np.abs(Lam(IP) @ V(k) - V(k + 1))) for k in [0, 1, 2.5, 1.632])
    print(f"   max|Lam(1/phi)V(k)-V(k+1)| = {mr:.2e}")
    mr = 0.0
    for a in [0.3, IP, 1.2]:
        for b in [0.5, 2 * IP, 0.9]:
            mr = max(mr, np.max(np.abs(Lam(a) @ Lam(b) - Lam(a + b))))
    print(
        f"   max|Lam(a)Lam(b)-Lam(a+b)| = {mr:.2e}  (rapidity addition = the kappa(a+b) rule)"
    )

    print("\n=== 3. exp(aK)=Lam(a);  NEW: dV/dk = (1/phi) K V  (boost transport) ===")
    mr = max(np.max(np.abs(expK(a) - Lam(a))) for a in [0.3, IP, 1.5])
    print(f"   max|exp(aK)-Lam(a)| = {mr:.2e}")
    mr = 0.0
    for k in [0, 0.7, 1.632, 3.3]:
        th = k / PHI
        dV = np.array([np.sinh(th), -np.cosh(th)]) / PHI  # analytic d/dk of V
        mr = max(mr, np.max(np.abs(dV - (1 / PHI) * K @ V(k))))
    print(f"   max|dV/dk - (1/phi)K V| = {mr:.2e}")

    print("\n=== 4a (09). beta = -G_flow/G_sym = -V[1]/V[0] = tanh(theta) ===")
    mr = max(
        abs(np.tanh(k / PHI) - (-V(k)[1] / V(k)[0])) for k in [0.3, 1, 1.632, 3, 4.896]
    )
    print(f"   max|tanh(theta) - (-V[1]/V[0])| = {mr:.2e}")

    print(
        "\n=== 4b (05). null weight vectors of the boost; weight ratio e^{-2theta} ==="
    )
    n_p = np.array([1.0, 1.0])  # Lam eigenvalue e^{-a}  (retarded null direction)
    n_m = np.array([1.0, -1.0])  # Lam eigenvalue e^{+a}  (advanced null direction)
    mr = 0.0
    for a in [0.3, IP, 1.1]:
        mr = max(
            mr,
            np.max(np.abs(Lam(a) @ n_p - np.exp(-a) * n_p)),
            np.max(np.abs(Lam(a) @ n_m - np.exp(a) * n_m)),
        )
    print(f"   Lam(a)(1,1)=e^-a(1,1), Lam(a)(1,-1)=e^+a(1,-1) residual = {mr:.2e}")
    mr = 0.0
    for k in [0.3, 1, 1.632, 3]:
        oV = osc(k) * V(k)
        th = k / PHI
        kp = oV[0] + oV[1]  # kappa(+k) = osc(cosh - sinh) = osc e^{-theta}  (retarded)
        km = oV[0] - oV[1]  # kappa(-k) = osc(cosh + sinh) = osc e^{+theta}  (advanced)
        mr = max(mr, abs(kp - osc(k) * np.exp(-th)), abs(km - osc(k) * np.exp(th)))
    print(f"   kappa(+-k) = osc*(V[0] -+ V[1]) = osc e^{{-+theta}} residual = {mr:.2e}")
    mr = max(
        abs(
            np.exp(-2 * k / PHI)
            - (osc(k) * np.exp(-k / PHI)) / (osc(k) * np.exp(k / PHI))
        )
        for k in [0.3, 1, 1.632, 3]
    )
    print(
        f"   detailed-balance kappa(+k)/kappa(-k) = e^{{-2theta}} (weight ratio) residual = {mr:.2e}"
    )

    print("\n=== 4c (07). spinor half-boost = SL(2,R) double cover ===")

    def s(a):
        return expSIG(a / 2)

    mr = max(np.max(np.abs(s(a) @ s(a) - expSIG(a))) for a in [0.3, IP, 1.0])
    print(f"   s(a)^2 = exp(a sigma)  (squaring = covering map) residual = {mr:.2e}")
    mr = max(
        abs(np.cosh(k / PHI) - (2 * np.cosh(k / (2 * PHI)) ** 2 - 1))
        for k in [1, 1.632, 3, 5]
    )
    print(
        f"   cosh(theta) = 2cosh^2(theta/2) - 1  (Chebyshev / cover) residual = {mr:.2e}"
    )

    print("\n=== 4d (04). compact real form: rotor R(dtheta) = exp(dtheta J) ===")
    dtheta = 78 * LNP - 12 * np.pi
    mr = max(
        np.max(np.abs(expJ(dtheta) - R(dtheta))), abs(np.linalg.det(R(dtheta)) - 1)
    )
    print(
        f"   exp(dtheta J)=R(dtheta), det=1 residual = {mr:.2e};  dtheta = {dtheta:.10f}"
    )
    mr = max(
        np.max(np.abs(R(dtheta) @ e_phase(24) - e_phase(63))),
        np.max(np.abs(R(dtheta) @ e_phase(63) - e_phase(102))),
        np.max(np.abs(R(dtheta) @ e_phase(102) - e_phase(141))),
    )
    print(f"   R e(24)=e(63), R e(63)=e(102), R e(102)=e(141) residual = {mr:.2e}")

    print(
        "\n=== 5. Casimir / mass-shell  M^2 = G_sym^2 - G_flow^2 = osc^2 ; =1 on k_n ==="
    )
    mr = 0.0
    for k in [0, 1, 3, 5]:
        Gs = osc(k) * np.cosh(k / PHI)
        Gf = -osc(k) * np.sinh(k / PHI)
        mr = max(mr, abs((Gs**2 - Gf**2) - osc(k) ** 2))
    print(f"   max|M^2 - osc^2| = {mr:.2e}")
    for n in [1, 2, 3]:
        kn = (2 * n - 1) * np.pi / (4 * LNP)
        Gs = osc(kn) * np.cosh(kn / PHI)
        Gf = -osc(kn) * np.sinh(kn / PHI)
        print(f"   k_{n} = {kn:.4f}:  M^2 = {Gs**2 - Gf**2:.12f}")

    print("\n=== 6. UNIFIED FIELD STATEMENT  Psi(k) = osc(k) Lam(k/phi) (1,0)^T ===")
    mr = max(
        np.max(np.abs(Lam(k / PHI) @ np.array([1.0, 0.0]) - V(k)))
        for k in [0, 0.7, 1.632, 3]
    )
    print(f"   Lam(k/phi)(1,0)^T = V(k)  (present-moment seed) residual = {mr:.2e}")
    mr = 0.0
    for k in [0, 0.7, 1.632, 3, 4.896]:
        Psi = osc(k) * (Lam(k / PHI) @ np.array([1.0, 0.0]))
        Gs = osc(k) * np.cosh(k / PHI)
        Gf = -osc(k) * np.sinh(k / PHI)
        kp = Psi[0] + Psi[1]  # n_+ . Psi  = kappa(+k)
        km = Psi[0] - Psi[1]  # n_- . Psi  = kappa(-k)
        mr = max(
            mr,
            np.max(np.abs(Psi - np.array([Gs, Gf]))),
            abs(kp - osc(k) * np.exp(-k / PHI)),
            abs(km - osc(k) * np.exp(k / PHI)),
        )
    print(f"   Psi=(G_sym,G_flow); kappa(+-k)=Psi[0]+-Psi[1]: residual = {mr:.2e}")

    print("\n=== 7. EXTENSION: rapidity = hyperbolic arc length of the worldline ===")

    # dV/dk = (1/phi)(sinh, -cosh); its eta-norm is constant and SPACELIKE.
    def dV(k):
        th = k / PHI
        return np.array([np.sinh(th), -np.cosh(th)]) / PHI

    mr = max(
        abs((dV(k) @ ETA @ dV(k)) - (-1.0 / PHI**2))
        for k in [0, 0.3, 1, 1.632, 3, 4.896, 8.161]
    )
    print(
        f"   max|<dV/dk,dV/dk>_eta - (-1/phi^2)| = {mr:.2e}  (constant spacelike speed 1/phi)"
    )
    # Arc length s(k)=int_0^k sqrt|<.,.>| dk' = (1/phi)*k = theta. Speed is constant so
    # the closed form is exact; cross-check the quadrature against k/phi.
    ks = np.linspace(0, 5, 200001)
    speed = np.array([np.sqrt(abs(dV(kk) @ ETA @ dV(kk))) for kk in ks])
    s_num = np.trapezoid(speed, ks)
    print(
        f"   |s(5)_numeric - 5/phi| = {abs(s_num - 5 / PHI):.2e}   (s(k)=k/phi=theta)"
    )
    print(f"   per-shell proper interval = s(k+1)-s(k) = 1/phi = {IP:.10f}")
    print("\nALL CHECKS COMPLETE")


if __name__ == "__main__":
    check()
