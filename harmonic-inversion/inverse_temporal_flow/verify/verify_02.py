"""Machine-precision verification of branch 02 (note 02-effective-metric.md).

The effective metric  ds^2 = kappa_Frenet d sigma^2 - c tau_Frenet dt^2  and the
signature-flip Wick rotation.  The Wick rotation acts on the LAPSE / RAPIDITY
(N -> iN, theta -> i theta), NOT on the argument t of the Frenet functions.

Run: python3 verify_02.py
All checks should print residuals at the 1e-15 level or report exact equality.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)


def u_of(t):
    return np.cos(2 * t) ** 2


def kappa_frenet(t):
    u = u_of(t)
    return np.sqrt(5 - 3 * u) / (1 + u) ** 1.5


def tau_frenet(t):
    u = u_of(t)
    return -3 * np.cos(2 * t) / (5 - 3 * u)


def v_flow(t):  # twist-to-bend ratio = local temporal-flow speed
    return np.abs(tau_frenet(t)) / kappa_frenet(t)


def check():
    ts = np.linspace(0, 2 * np.pi, 200001)

    print("=== 1. Frenet ranges (corpus constants) ===")
    ka, ta = kappa_frenet(ts), tau_frenet(ts)
    print(
        f"   kappa in [{ka.min():.6f}, {ka.max():.6f}]  (corpus [0.5, sqrt5={np.sqrt(5):.6f}])"
    )
    print(f"   tau   in [{ta.min():+.6f}, {ta.max():+.6f}]  (corpus [-1.5, +1.5])")

    print("\n=== 2. v_flow = |tau|/kappa range and closed form (eq 2.4) ===")
    vf = v_flow(ts)
    vf_cf = (
        3 * np.abs(np.cos(2 * ts)) * (1 + u_of(ts)) ** 1.5 / (5 - 3 * u_of(ts)) ** 1.5
    )
    print(f"   v_flow in [{vf.min():.3e}, {vf.max():.6f}]  (claim [0, 3])")
    print(
        f"   max|v_flow - 3|cos2t|(1+u)^1.5/(5-3u)^1.5| = {np.max(np.abs(vf - vf_cf)):.2e}"
    )

    print(
        "\n=== 3. Inversion shells k_n: tau=0 (null/horizon), kappa=sqrt5, v_flow=0 ==="
    )
    for n in range(1, 4):
        k = (2 * n - 1) * np.pi / (4 * LNPHI)
        t = k * LNPHI
        print(
            f"   k{n}={k:7.4f}  tau={tau_frenet(t):+.2e}  "
            f"kappa={kappa_frenet(t):.6f}  v_flow={v_flow(t):.2e}"
        )

    print(
        "\n=== 4. Cardinal points t=n pi/2: |tau|=3/2, kappa=1/2, v_flow=3, sign ALTERNATES ==="
    )
    for n in range(5):
        t = n * np.pi / 2
        print(
            f"   t={t:.4f} (n={n})  tau={tau_frenet(t):+.4f}  "
            f"kappa={kappa_frenet(t):.4f}  v_flow={v_flow(t):.4f}"
        )

    print(
        "\n=== 5. DISCRIMINATOR: 't->it' does NOT flip tau's sign (so it is NOT the Wick rotation) ==="
    )
    # cos(2 i t) = cosh(2t):  tau_Frenet(it) = -3 cosh2t/(5 - 3 cosh^2 2t)
    tau_it = lambda t: -3 * np.cosh(2 * t) / (5 - 3 * np.cosh(2 * t) ** 2)
    for t in [0.0, 0.1, 0.3]:
        print(
            f"   t={t}: tau(it)={tau_it(t):+.4f}   -tau(t)={-tau_frenet(t):+.4f}   (unequal => 't->it' wrong)"
        )
    print("   => the correct continuation is N->iN / theta->i theta at FIXED t.")

    print("\n=== 6. Correct Wick rotation: rapidity theta=k/phi -> i theta ===")
    for k in [1.0, 1.632, 3.0]:
        th = k / PHI
        dc = abs(np.cosh(1j * th).real - np.cos(th))
        ds = abs(np.sinh(1j * th) - 1j * np.sin(th))
        print(
            f"   k={k:.3f} theta={th:.4f}  |cosh(i th)-cos th|={dc:.1e}  |sinh(i th)-i sin th|={ds:.1e}"
        )

    print("\n=== 7. Lapse continuation N->iN flips g_tt sign; |det g| preserved ===")
    c = 1.0
    for t in [0.3, 1.1, 2.0]:
        Om2 = kappa_frenet(t)
        N2 = c * tau_frenet(t)  # signed lapse-squared
        gtt = -N2  # Lorentzian temporal block
        gtt_wick = +N2  # after N -> iN  (g_tt = -(iN)^2 = +N^2)
        detL, detE = Om2 * gtt, Om2 * gtt_wick
        print(
            f"   t={t:.2f}  g_tt={gtt:+.4f} -> {gtt_wick:+.4f}  "
            f"|det| {abs(detL):.4f} == {abs(detE):.4f}  ({np.isclose(abs(detL), abs(detE))})"
        )

    print(
        "\n=== 8. Signature-flip Maslov phase per shell crossing: e^{i pi/2}=i, four-shell period ==="
    )
    for dn in range(5):
        print(f"   dn={dn}:  i^dn = {1j**dn:+.4f}")

    print(
        "\n=== 9. EXTENSION: Euclidean action per inverse-flow patch  S_E = int sqrt(c|tau|) dt ==="
    )

    # Inverse-flow (tau<0) patch is centred on a cardinal point; one such patch is
    # t in (-pi/4, pi/4) (between two consecutive torsion zeros), where tau<0 throughout.
    def trap(a, b, N=2000001):
        x = np.linspace(a, b, N)
        return np.trapezoid(np.sqrt(c * np.abs(tau_frenet(x))), x)

    S_E = trap(-np.pi / 4, np.pi / 4)
    S_L = trap(np.pi / 4, 3 * np.pi / 4)  # adjacent forward patch, equal by symmetry
    tt = np.linspace(-np.pi / 4 + 1e-9, np.pi / 4 - 1e-9, 5001)
    print(
        f"   inverse patch t in (-pi/4, pi/4): tau in [{tau_frenet(tt).min():+.4f}, {tau_frenet(tt).max():+.4f}] (all<0)"
    )
    print(
        f"   S_E = {S_E:.6f}   tunneling weight e^-S_E = {np.exp(-S_E):.6f}   S_E/pi = {S_E / np.pi:.6f}"
    )
    print(f"   forward patch S_L = {S_L:.6f}   |S_E - S_L| = {abs(S_E - S_L):.1e}")


if __name__ == "__main__":
    check()
