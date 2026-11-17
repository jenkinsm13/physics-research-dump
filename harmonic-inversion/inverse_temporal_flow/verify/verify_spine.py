"""Machine-precision verification of the four spine results (note 00-spine.md).

Run: python3 verify_spine.py
All checks should print residuals at the 1e-15 level or report exact equality.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)


def rp(t):  # r'(t)
    return np.array([np.cos(t), np.cos(2 * t), -np.sin(t)])


def rpp(t):  # r''(t)
    return np.array([-np.sin(t), -2 * np.sin(2 * t), -np.cos(t)])


def tau_frenet(t):
    u = np.cos(2 * t) ** 2
    return -3 * np.cos(2 * t) / (5 - 3 * u)


def kappa_signed(k):
    # signed-ordinal coupling kernel; k may be negative (advanced branch)
    return 1.0 / (1 + np.cos(2 * k * LNPHI) ** 2) * np.exp(-k / PHI)


def check():
    print("=== 1. Conserved chronon current  L_y = (r' x r'')_y == 1 ===")
    ts = np.linspace(0, 2 * np.pi, 17)
    Ly = np.array([np.cross(rp(t), rpp(t))[1] for t in ts])
    print(f"   max |L_y - 1| = {np.max(np.abs(Ly - 1)):.2e}  (exact: 1)")

    print(
        "\n=== 2. Inversion shells: coupling max == torsion zero == flow reversal ==="
    )
    for n in range(1, 4):
        k = (2 * n - 1) * np.pi / (4 * LNPHI)
        osc = 1.0 / (1 + np.cos(2 * k * LNPHI) ** 2)
        print(
            f"   k{n}={k:7.4f}  oscfactor={osc:.6f} (max=1)  "
            f"tau(t=k lnphi)={tau_frenet(k * LNPHI):+.2e} (zero)"
        )

    print("\n=== 3. Retarded/advanced split -> cosh/sinh ===")
    for k in [0.0, 1.0, 1.632, 3.0]:
        sym = 0.5 * (kappa_signed(k) + kappa_signed(-k))
        anti = 0.5 * (kappa_signed(k) - kappa_signed(-k))
        osc = 1.0 / (1 + np.cos(2 * k * LNPHI) ** 2)
        dsym = abs(sym - osc * np.cosh(k / PHI))
        dflow = abs(anti - (-osc * np.sinh(k / PHI)))
        print(
            f"   k={k:5.3f}  G_sym={sym:+.6f} (res {dsym:.1e})  "
            f"G_flow={anti:+.6f} (res {dflow:.1e})"
        )

    print("\n=== 4. Hyperbolic invariant  G_sym^2 - G_flow^2 = 1/(1+cos^2)^2 ===")
    for k in [0.0, 1.0, 1.632, 3.0]:
        sym = 0.5 * (kappa_signed(k) + kappa_signed(-k))
        anti = 0.5 * (kappa_signed(k) - kappa_signed(-k))
        inv = sym**2 - anti**2
        target = (1.0 / (1 + np.cos(2 * k * LNPHI) ** 2)) ** 2
        print(
            f"   k={k:5.3f}  inv={inv:.6f}  target={target:.6f}  res {abs(inv - target):.1e}"
        )


if __name__ == "__main__":
    check()
