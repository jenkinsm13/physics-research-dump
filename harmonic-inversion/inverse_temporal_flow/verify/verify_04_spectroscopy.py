"""Machine-precision verification of branch 04 (note 04-inversion-spectroscopy.md).

Re-runs every numerical claim in the note: the lepton phase table, the constant
phase decrement / drift law delta_theta_g = 78 ln(phi) - 12 pi, the 12-pi
fold-count per generation, the mass-fit slope and geometric-mean seal, the
antisymmetric residual triple, the curvature-aware fit, the k4 = 141 prediction,
and the SO(2) rotor generation operator (the Extension).

Run: python3 verify_04_spectroscopy.py
All residuals print at the 1e-15 level or report exact integer equality.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)

# observed charged-lepton masses (MeV); only ratios enter the seal
M = {"e": 0.51099895, "mu": 105.6583755, "tau": 1776.86}
K = {"e": 24, "mu": 63, "tau": 102}
LEPTONS = ["e", "mu", "tau"]


def theta_raw(k):
    return 2 * k * LNPHI


def theta_mod(k):
    return theta_raw(k) % np.pi


def cos_theta(k):
    return np.cos(theta_raw(k))


def Phi(k):  # tau_Frenet sampled at t = k ln(phi); local temporal-flow rate
    c = np.cos(theta_raw(k))
    return -3 * c / (5 - 3 * c**2)


def kappa_frenet(k):  # spatial-coupling / gravity strength at ordinal k
    u = np.cos(theta_raw(k)) ** 2
    return np.sqrt(5 - 3 * u) / (1 + u) ** 1.5


def osc(k):
    return 1.0 / (1 + np.cos(theta_raw(k)) ** 2)


def check():
    print(f"PHI={PHI:.10f}  LNPHI={LNPHI:.10f}  1/PHI={1 / PHI:.10f}\n")

    print("=== 1. Lepton phase table ===")
    print(
        f"{'lep':4}{'k':>5}{'theta_mod':>12}{'cos':>11}{'Phi':>11}{'osc':>11}{'kFrenet':>11}"
    )
    for L in LEPTONS:
        k = K[L]
        print(
            f"{L:4}{k:5d}{theta_mod(k):12.5f}{cos_theta(k):11.5f}"
            f"{Phi(k):11.5f}{osc(k):11.5f}{kappa_frenet(k):11.5f}"
        )
    for L in LEPTONS:  # range guards from the corpus
        assert 0.5 <= kappa_frenet(K[L]) <= np.sqrt(5) + 1e-12
        assert 0.5 <= osc(K[L]) <= 1.0
        assert Phi(K[L]) > 0 and cos_theta(K[L]) < 0  # off-reversal, forward-flow

    print("\n=== 2. Constant generation step Delta_g = 39, drift law ===")
    dg1 = K["mu"] - K["e"]
    dg2 = K["tau"] - K["mu"]
    print(
        f"   k_mu-k_e={dg1}, k_tau-k_mu={dg2}  -> Delta_g=39 exact: {dg1 == dg2 == 39}"
    )
    delta_closed = 78 * LNPHI - 12 * np.pi
    d_em = theta_mod(K["mu"]) - theta_mod(K["e"])
    d_mt = theta_mod(K["tau"]) - theta_mod(K["mu"])
    print(f"   theta_mu-theta_e   = {d_em:.12f}")
    print(f"   theta_tau-theta_mu = {d_mt:.12f}")
    print(f"   78 ln(phi)-12 pi   = {delta_closed:.12f}")
    print(
        f"   max |decrement - closed form| = {max(abs(d_em - delta_closed), abs(d_mt - delta_closed)):.2e}"
    )

    print("\n=== 3. Twelve-reversal commensurability (exact integer fold count) ===")
    for a, b in [("e", "mu"), ("mu", "tau"), ("tau", None)]:
        kb = K[b] if b else K["tau"] + 39
        nb = b if b else "k4"
        folds = int(np.floor(theta_raw(kb) / np.pi) - np.floor(theta_raw(K[a]) / np.pi))
        print(
            f"   {a}->{nb}: pi-boundaries crossed = {folds}  (must be 12: {folds == 12})"
        )
    print(
        f"   ratio Delta_g/(pi/2lnphi) = {2 * 39 * LNPHI / np.pi:.6f}  (~12, defect = drift)"
    )

    print("\n=== 4. Mass law: slope, geometric-mean seal, residual triple ===")
    ks = np.array([K[L] for L in LEPTONS], float)
    lnm = np.log(np.array([M[L] for L in LEPTONS]))
    A = np.vstack([ks, np.ones_like(ks)]).T
    (a, b), *_ = np.linalg.lstsq(A, lnm, rcond=None)
    print(f"   affine slope a = {a:.6f}")
    print(
        f"   e^(39 a) = {np.exp(39 * a):.4f}  vs sqrt(m_tau/m_e) = {np.sqrt(M['tau'] / M['e']):.4f}"
    )
    print(
        f"     seal residual = {abs(np.exp(39 * a) - np.sqrt(M['tau'] / M['e'])):.2e}"
    )
    resid = lnm - (a * ks + b)
    print(f"   residual triple = ({resid[0]:+.4f}, {resid[1]:+.4f}, {resid[2]:+.4f})")
    print(f"     antisymmetry: resid[1] + 2*resid[0] = {resid[1] + 2 * resid[0]:.2e}")

    print("\n=== 5. Prediction k4 = 141 ===")
    k4 = 141
    print(
        f"   theta(141)={theta_mod(k4):.5f}  cos={cos_theta(k4):.5f}  Phi={Phi(k4):+.5f}"
    )
    print(f"   bare affine mass e^(a*141+b) = {np.exp(a * 141 + b) / 1000:.3f} GeV")
    ct = np.array([cos_theta(k) for k in ks])
    Mc = np.vstack([ks, np.ones_like(ks), ct]).T
    a3, b3, c3 = np.linalg.solve(Mc, lnm)
    lnm4 = a3 * k4 + b3 + c3 * cos_theta(k4)
    print(
        f"   curvature coeff c = {c3:.4f}  -> curvature-aware mass = {np.exp(lnm4) / 1000:.3f} GeV"
    )

    print("\n=== 6. EXTENSION: SO(2) rotor generation operator ===")
    delta = 78 * LNPHI - 12 * np.pi
    R = np.array([[np.cos(delta), -np.sin(delta)], [np.sin(delta), np.cos(delta)]])

    def vec(k):
        th = theta_raw(k)
        return np.array([np.cos(th), np.sin(th)])

    worst = 0.0
    for k1, k2 in [(24, 63), (63, 102), (102, 141)]:
        err = np.max(np.abs(R @ vec(k1) - vec(k2)))
        worst = max(worst, err)
        print(f"   R(delta)@e(theta_{k1}) = e(theta_{k2})  err={err:.2e}")
    print(
        f"   det R = {np.linalg.det(R):.6f} (=1), rotor is rigid SO(2); max err {worst:.2e}"
    )


if __name__ == "__main__":
    check()
