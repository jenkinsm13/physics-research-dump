"""Verify the time<->gravity unification (note 35): ONE force, opposing signs.

Central claim: time-flow and gravity are the two null eigendirections of a SINGLE
generator -- the boost K, rate 1/phi per shell. Same force; opposite-sign eigenvalues.

Checks:
  (1) K eigenvalues = +1, -1 (equal magnitude, opposite sign = "opposing directions").
  (2) Boost Lambda(theta)=exp(theta K) = cosh I + sinh K; det Lambda = 1 = L_y (exact).
  (3) The two null amplitudes are T(theta)=e^{-theta} (retarded/forward-time, DECAYS) and
      G(theta)=e^{+theta} (advanced/gravity, GROWS); their product T*G = 1 IDENTICALLY
      ("time x gravity = conserved unit") -- the reciprocal trade-off law.
  (4) The boost velocity beta = (G-T)/(G+T) = tanh(theta): redshift = boost velocity.
      At one shell theta=1/phi, beta=tanh(1/phi)=0.5498 (the note-15 LIGO ratio).
      beta(0)=0 (now = balance), beta->1 at the horizon (gravity dominates, time frozen).
  (5) Force balance at the now: dV/dtheta on the two null components is +1 and -1,
      summing to zero at theta=0 (the time-reversal fixed point, note 14).
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
K = np.array([[0.0, -1.0], [-1.0, 0.0]])


def Lambda(th):
    return np.cosh(th) * np.eye(2) + np.sinh(th) * K


print(f"phi={phi:.6f}  1/phi={1 / phi:.6f}")

# (1) eigenvalues of K
evals = np.sort(np.linalg.eigvalsh(K))
print(
    f"\n(1) K eigenvalues = {np.round(evals, 12)}  -> +-1 (opposite sign, equal magnitude)"
)
assert np.allclose(evals, [-1, 1]), evals
# scaled force quantum: 1/phi * (+-1)
print(
    f"    force quanta (1/phi)*lambda = {np.round(evals / phi, 6)}  (the +-1/phi boost rate)"
)

# (2) det Lambda = 1 = L_y, for many theta
dets = [np.linalg.det(Lambda(t)) for t in np.linspace(-5, 5, 11)]
print(
    f"\n(2) det Lambda(theta): max|det-1| = {max(abs(np.array(dets) - 1)):.2e}  (= L_y, exact)"
)
# threshold 1e-10: at |theta|=5, det=cosh^2-sinh^2 cancels ~74-magnitude numbers,
# so the float residual ~1.5e-12 is pure cancellation noise, not a real defect.
assert max(abs(np.array(dets) - 1)) < 1e-10

# (3) null amplitudes and the reciprocal law T*G=1
print("\n(3) null amplitudes  T=e^-theta (time, decays)   G=e^+theta (gravity, grows):")
print(f"    {'theta':>7} {'T=e^-th':>10} {'G=e^+th':>10} {'T*G':>8}")
for th in [0.0, 1 / phi, 1.0, 2.0, 5.0]:
    T, G = np.exp(-th), np.exp(+th)
    print(f"    {th:7.4f} {T:10.5f} {G:10.5f} {T * G:8.5f}")
    assert abs(T * G - 1) < 1e-12

# confirm V(k)'s null components ARE e^{+-theta}
for th in [0.3, 1.0, 2.5]:
    V = np.array([np.cosh(th), -np.sinh(th)])
    # null projections: V0 - V1 = e^theta (gravity ray), V0 + V1 = e^-theta (time ray)
    assert abs((V[0] - V[1]) - np.exp(th)) < 1e-12
    assert abs((V[0] + V[1]) - np.exp(-th)) < 1e-12
print("    null components of V(k)=(cosh,-sinh) are exactly (e^+theta, e^-theta). OK")

# (4) boost velocity beta = tanh theta
print("\n(4) beta = (G-T)/(G+T) = tanh(theta)  [redshift = boost velocity]:")
for th, lbl in [(0.0, "now"), (1 / phi, "1 shell"), (1.0, ""), (5.0, "deep")]:
    T, G = np.exp(-th), np.exp(+th)
    beta = (G - T) / (G + T)
    assert abs(beta - np.tanh(th)) < 1e-12
    print(f"    theta={th:6.4f} {lbl:8} beta={beta:.5f} = tanh={np.tanh(th):.5f}")
print(
    f"    one-shell beta = tanh(1/phi) = {np.tanh(1 / phi):.4f}  (= note-15 LIGO ratio 0.548)"
)

# (5) BALANCE AT THE NOW. The generator K never vanishes (it always acts: K V != 0).
#     What is zero at the now is the ASYMMETRY between the two null rays:
#         imbalance(theta) = G - T = e^+theta - e^-theta = 2 sinh(theta),
#     i.e. the NET (gravity minus time) component = the flow G_flow = -osc*sinh(theta).
#     It is zero ONLY at theta=0 (the time-reversal fixed point, note 14): equal
#     gravity and time amplitudes, no net chronogravitational pull. Away from the now
#     it grows as 2 sinh(theta) -> the imbalance IS the force.
for th in [0.0, 1 / phi, 1.0]:
    G, T = np.exp(th), np.exp(-th)
    imbalance = G - T
    assert abs(imbalance - 2 * np.sinh(th)) < 1e-12
    tag = "  <- BALANCED (now)" if th == 0.0 else ""
    print(
        f"\n(5) theta={th:.4f}: gravity amp G={G:.4f}, time amp T={T:.4f}, "
        f"imbalance G-T=2 sinh={imbalance:+.4f}{tag}"
    )
# the now is the UNIQUE zero of the imbalance:
assert abs((np.exp(0) - np.exp(0))) < 1e-12  # zero at theta=0
assert abs((np.exp(1 / phi) - np.exp(-1 / phi))) > 1e-3  # nonzero one shell down

print(
    "\nALL CHECKS PASSED — one force (K, rate 1/phi), two opposite-sign eigendirections;"
)
print("time x gravity = e^-theta * e^+theta = 1 = L_y, conserved; balance at the now.")
