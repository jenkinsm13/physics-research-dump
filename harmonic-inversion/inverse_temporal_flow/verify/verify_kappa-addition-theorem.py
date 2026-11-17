"""
verify_kappa-addition-theorem.py
================================
Numerical verification for note 11 — The kappa(a+b) Theorem.

Confirms, to machine precision, that the correct two-leg kernel is
kappa(a+b) = osc(a+b) e^{-(a+b)/phi}, that the product kappa(a)kappa(b)
fails by exactly the lattice defect Delta(a,b)=osc(a)osc(b)/osc(a+b)
(envelope cancels identically), and that the additive law is forced by
the SO(1,1) boost group (rapidity addition) and the relativistic
velocity-addition of the chronon drift.

All identities here are EXACT; residuals are ~1e-13 or smaller.
Run: python3 verify_kappa-addition-theorem.py
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2.0
lnphi = np.log(phi)


def osc(k):
    # flow-reversal lattice weight; NEVER smoothed (it IS the inversion comb)
    return 1.0 / (1.0 + np.cos(2.0 * k * lnphi) ** 2)


def g(k):
    # reciprocal weight g = 1/osc = 1 + cos^2(2 k lnphi) in [1,2]
    return 1.0 + np.cos(2.0 * k * lnphi) ** 2


def kappa(k):
    # dressed propagator: retarded (k>0) / advanced (k<0)
    return osc(k) * np.exp(-k / phi)


def Gsym(k):
    return osc(k) * np.cosh(k / phi)


def Gflow(k):
    return -osc(k) * np.sinh(k / phi)


def V(k):
    # chronon two-vector, de-weighted: unit timelike (note 99 / 03)
    return np.array([np.cosh(k / phi), np.sinh(k / phi)])


def Lambda(theta):
    c, s = np.cosh(theta), np.sinh(theta)
    return np.array([[c, s], [s, c]])


def Delta(a, b):
    # the lattice defect: kappa(a)kappa(b)/kappa(a+b) = osc(a)osc(b)/osc(a+b)
    return g(a + b) / (g(a) * g(b))


def main():
    maxres = 0.0
    ki = lambda n: (2 * n - 1) * np.pi / (4 * lnphi)  # inversion-shell ordinals

    print("phi =", phi, " lnphi =", lnphi, " 1/phi =", 1 / phi)

    # ---- 1. counterexample (a,b) = (k1, 2 k1) ----
    k1 = ki(1)
    a, b = k1, 2 * k1
    print("\n[1] COUNTEREXAMPLE (a,b)=(k1,2k1), k1 =", k1)
    print("    osc(a)=", osc(a), " osc(b)=", osc(b), " osc(a+b)=", osc(a + b))
    print("    correct kappa(a+b)        =", kappa(a + b))
    print("    product kappa(a)kappa(b)  =", kappa(a) * kappa(b))
    print(
        "    ratio product/correct     =",
        (kappa(a) * kappa(b)) / kappa(a + b),
        "(exact lattice defect = 1/2)",
    )
    maxres = max(maxres, abs((kappa(a) * kappa(b)) / kappa(a + b) - 0.5))

    # ---- 2. envelope is right, oscillatory weight is wrong ----
    env_c = np.exp(-(a + b) / phi)
    env_p = np.exp(-a / phi) * np.exp(-b / phi)
    print(
        "\n[2] envelope e^{-(a+b)/phi} vs e^{-a/phi}e^{-b/phi}: residual =",
        abs(env_c - env_p),
        "(product envelope EXACTLY right -> error is purely lattice)",
    )
    maxres = max(maxres, abs(env_c - env_p))

    # ---- 3. the new equation: Delta(a,b)=kappa-ratio=osc-ratio over random (a,b) ----
    rng = np.random.default_rng(137)
    worst = 0.0
    for _ in range(20000):
        aa, bb = rng.uniform(0, 12), rng.uniform(0, 12)
        worst = max(
            worst, abs((kappa(aa) * kappa(bb)) / kappa(aa + bb) - Delta(aa, bb))
        )
    print(
        "\n[3] NEW EQ Delta(a,b)=osc(a)osc(b)/osc(a+b): max residual over 20000 random =",
        worst,
    )
    maxres = max(maxres, worst)

    # ---- 4. velocity over-saturation ----
    beta = lambda k: np.tanh(k / phi)
    ba, bb_ = beta(a), beta(b)
    add = (ba + bb_) / (1 + ba * bb_)
    print(
        "\n[4] relativistic add (ba+bb)/(1+ba bb) =",
        add,
        " vs beta(a+b)=",
        beta(a + b),
        " residual=",
        abs(add - beta(a + b)),
    )
    maxres = max(maxres, abs(add - beta(a + b)))
    print(
        "    deep shells a=6,b=7: naive sum ba+bb =",
        beta(6) + beta(7),
        ">1 UNPHYSICAL; relativistic add =",
        (beta(6) + beta(7)) / (1 + beta(6) * beta(7)),
        "<1 OK",
    )

    # ---- 5. boost composition Lambda(t1)Lambda(t2)V0 = V(k1+k2) ----
    print("\n[5] BOOST COMPOSITION Lambda(k1/phi)Lambda(k2/phi)V(0)=V(k1+k2)")
    V0 = V(0.0)
    for k1t, k2t in [(1.0, 2.0), (k1, 2 * k1), (0.5, 4.8964), (3.264, 3.264)]:
        r = np.max(np.abs(Lambda(k1t / phi) @ (Lambda(k2t / phi) @ V0) - V(k1t + k2t)))
        print(f"    (k1,k2)=({k1t:.4f},{k2t:.4f})  residual={r:.2e}")
        maxres = max(maxres, r)

    # ---- 6. mass-shell invariant ----
    print("\n[6] mass-shell M^2=Gsym^2-Gflow^2=osc^2, =1 at inversion shells")
    for n in [1, 2, 3]:
        kn = ki(n)
        M2 = Gsym(kn) ** 2 - Gflow(kn) ** 2
        print(f"    k_{n}={kn:.4f}: M^2={M2:.12f}")
        maxres = max(maxres, abs(M2 - 1.0))

    # ---- 7. product valid iff g(a)g(b)=g(a+b): codim-1, NOT the osc-peaks ----
    print("\n[7] product valid iff g(a)g(b)=g(a+b) (one eqn, two unknowns -> codim-1)")
    # peak+peak is the WORST case, not the admissible one: osc=1 at ODD multiples of k1,
    # odd+odd=even -> a+b on a trough (osc=1/2) -> Delta=2 (global max).
    Dpp = Delta(k1, k1)
    print(
        f"    Delta(k1,k1) = osc(k1)^2/osc(2k1) = {Dpp} (GLOBAL MAX, peak+peak->trough)"
    )
    maxres = max(maxres, abs(Dpp - 2.0))
    print(
        f"    osc(k1)={osc(k1)}, osc(2k1)={osc(2 * k1)} -> condition osc(a)=osc(b)=osc(a+b)=1 is UNSATISFIABLE"
    )
    print(
        "    contact limit: Delta(0,0)=osc(0)=",
        Delta(1e-9, 1e-9),
        "(~1/2, NO small-theta recovery)",
    )
    bs = np.linspace(0.001, 20, 200000)
    D = Delta(k1, bs)
    print(
        "    a=k1 swept b in [0,20]: Delta min,max =",
        D.min(),
        D.max(),
        "(=1 only on discrete cardinal crossings, never an interval)",
    )

    # ---- 8. EXACT reachable band [2/5, 2] (note 11 Extension) ----
    # infimum lives on the diagonal a=b. Let c=cos^2(2 a lnphi) in [0,1];
    # g(a)=1+c, and the comb double-angle gives g(2a)=1+(2c-1)^2, so
    # Delta_diag(c)=(1+(2c-1)^2)/(1+c)^2. Stationarity -> 12c-8=0 -> c*=2/3,
    # Delta_diag(2/3)=(10/9)/(25/9)=2/5 EXACTLY. Supremum is Delta(k1,k1)=2.
    print("\n[8] EXACT reachable band [2/5, 2] (note 11 Extension)")
    cstar = 2.0 / 3.0
    Ddiag_star = (1 + (2 * cstar - 1) ** 2) / (1 + cstar) ** 2
    print(f"    Delta_diag(c*=2/3) = {Ddiag_star} (exact inf = 2/5 = 0.4)")
    maxres = max(maxres, abs(Ddiag_star - 0.4))
    # realize it on the manifold: pick a with cos^2(2 a lnphi)=2/3, on the diagonal a=b
    a_inf = np.arccos(np.sqrt(2.0 / 3.0)) / (2.0 * lnphi)
    print(f"    realized at a=b={a_inf:.6f}: Delta(a,a) = {Delta(a_inf, a_inf):.10f}")
    maxres = max(maxres, abs(Delta(a_inf, a_inf) - 0.4))
    # global infimum never breached over a large random sweep in [0,50]^2
    rng2 = np.random.default_rng(2718)
    A = rng2.uniform(0, 50, 5_000_000)
    B = rng2.uniform(0, 50, 5_000_000)
    Dall = Delta(A, B)
    print(
        f"    5e6 random (a,b) in [0,50]^2: min={Dall.min():.10f} (>=2/5), max={Dall.max():.10f} (<=2)"
    )
    assert Dall.min() >= 0.4 - 1e-6 and Dall.max() <= 2.0 + 1e-6, "band breached"
    gc = np.sqrt(0.4 * 2.0)
    print(
        f"    geometric centre sqrt(2/5 * 2) = {gc:.10f} = 2/sqrt(5) = {2 / np.sqrt(5):.10f}, log-width ln5={np.log(5):.6f}"
    )
    maxres = max(maxres, abs(gc - 2 / np.sqrt(5)))

    print("\nMAX RESIDUAL over all exact-identity checks =", maxres)
    assert maxres < 1e-9, "an exact identity failed"
    print("ALL CHECKS PASSED.")


if __name__ == "__main__":
    main()
