"""Verify note 35a: the chronogravitational potential U(theta) = -2 cosh(theta).

Built on the note-35 spine (verified): ONE generator K (rate 1/phi), eigenvalues
EXACTLY +-1; null rays T(theta)=e^-theta (time), G(theta)=e^+theta (gravity); the
reciprocal law T*G=1=L_y; the net force F(theta)=G-T=2 sinh(theta); beta=tanh(theta).

Claims checked here (every checkable line in the .md):

  (A) U(theta) = -2 cosh(theta) is the scalar potential whose gradient is the net force:
          -dU/dtheta = 2 sinh(theta) = F = G - T.  (exact, all theta)
      And U = -2 * G_sym^bare, where G_sym^bare = cosh(theta) is the BARE even channel.

  (B) The two null rays e^{+-theta} are the +-1 eigenfunctions of the gradient operator
      d/dtheta:  d/dtheta e^{+-theta} = (+-1) e^{+-theta}.  This is the SAME spectrum {+1,-1}
      as the generator K of note 35.  Gravity ray = +1 grad-eigendirection; time ray = -1.

  (C) HARD NUMBER + honest comparison to the now-Hessian (note 14):
        U''(0) = -2  (exact). The now is a MAXIMUM of U (U''<0) -> unstable hilltop ->
        force points AWAY from the now -> fall toward the horizon (correct physics).
      Note 14 gives G_sym''(0) (in k) = 2 ln^2 phi + 1/(2 phi^2) = +0.654113 -> a MINIMUM.
      OPPOSITE SIGN, by the defining relation U = -2 G_sym^bare. Report the opposition;
      do NOT equate them.
      Stripped rapidity-curvature comparison (both in theta): the rapidity part of
      G_sym'' in theta is osc(0)*cosh''(0) = 1/2 (note-14 triple entry +1/2);
      U's is -2. Ratio -4 is just the -2 normalization x sign; no deep meaning.

  (D) V_grav (note 16 sec 5) is the osc-dressed, source-convolved GRADIENT of U, NOT U.
      Its kernel ~ sinh((n-m)/phi) = -1/2 * U'(theta_{n-m}); U itself ~ cosh != sinh.
      Check: kernel_Vgrav(d) == sinh(d/phi)/(1+cos^2(2 d ln phi)) == (-1/2 U'(d/phi))*osc(d).

  (E) Equation of motion / boost rate. The chronon worldline V0(k)=cosh(k/phi) obeys
        dV0/dk = (1/phi) sinh(theta) = (1/(2 phi)) F(theta),
      i.e. the k-gradient of the time component is the net force divided by 2phi. The
      flow is uniform-boost theta=k/phi (1/phi is the note-10 connection INPUT, not
      forced by U); U's gradient reproduces F along it. (honest framing)

  (F) Well-depth / curvature numbers, and U'(1/phi) vs note-15 ratio:
        U(0) = -2 (bottom of the -cosh in magnitude = top in sign), F(1/phi)=2 sinh(1/phi),
        beta(1/phi)=tanh(1/phi)=0.5498 = F/(G+T) recovered from U-gradient over 2U-channel.
        NOTE (audit): 0.5498 vs corpus LIGO RE-ANALYSIS 0.548 is a 0.32% bracket (note 15's
        own figure), parameter-free in value but selecting the discrete shell n=1; not a
        published-LIGO match. Only n=1 lands near 0.548 (n=0->0, n=2->0.844) -- disclosed.

  (G) EXTENSION -- potential-force invariant U^2 - F^2 = 4 L_y = 4:
        U=-(G+T)=-2cosh, F=G-T=2sinh => U^2-F^2 = 4 G T = 4 (since T*G=1=L_y). The
        reciprocal law of note 35 in potential-force variables; equivalently
        1-beta^2 = sech^2(theta), with -U=2gamma, F=2 beta gamma. Pure algebra, no
        energy/stability claim (non-Hermitian caveat not engaged).
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
ln_phi = np.log(phi)
print(f"phi      = {phi:.10f}")
print(f"1/phi    = {1 / phi:.10f}")
print(f"ln(phi)  = {ln_phi:.10f}")


def U(th):
    return -2.0 * np.cosh(th)


def dU(th):  # analytic dU/dtheta
    return -2.0 * np.sinh(th)


def d2U(th):  # analytic d2U/dtheta2
    return -2.0 * np.cosh(th)


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * ln_phi) ** 2)


# ----------------------------------------------------------------------------
print("\n(A) F = -dU/dtheta = 2 sinh(theta) = G - T  (potential -> force)")
print(f"    {'theta':>8} {'-dU/dth':>10} {'2sinh':>10} {'G-T':>10}")
maxA = 0.0
for th in [-2.0, -1.0, -1 / phi, 0.0, 1 / phi, 1.0, 2.0, 3.0]:
    G, T = np.exp(th), np.exp(-th)
    F_pot = -dU(th)
    F_def = G - T
    F_sinh = 2 * np.sinh(th)
    maxA = max(maxA, abs(F_pot - F_def), abs(F_pot - F_sinh))
    print(f"    {th:8.4f} {F_pot:10.5f} {F_sinh:10.5f} {F_def:10.5f}")
    assert abs(F_pot - F_def) < 1e-13
    assert abs(F_pot - F_sinh) < 1e-13
print(f"    max|residual| = {maxA:.2e}  -> EXACT")
# U = -2 * bare even channel cosh
for th in [-1.3, 0.0, 0.7, 2.1]:
    assert abs(U(th) - (-2.0 * np.cosh(th))) < 1e-15
print("    U(theta) = -2 cosh(theta) = -2 * G_sym^bare(theta).  OK")

# ----------------------------------------------------------------------------
print("\n(B) null rays e^{+-theta} are +-1 eigenfunctions of d/dtheta (= K-spectrum)")
h = 1e-6
for th in [-1.0, 0.0, 0.4, 1.5]:
    G = np.exp(th)
    T = np.exp(-th)
    # numerical d/dtheta via central difference
    dG = (np.exp(th + h) - np.exp(th - h)) / (2 * h)
    dT = (np.exp(-(th + h)) - np.exp(-(th - h))) / (2 * h)
    # gravity ray: eigenvalue +1; time ray: eigenvalue -1
    assert abs(dG - (+1) * G) < 1e-6, (th, dG, G)
    assert abs(dT - (-1) * T) < 1e-6, (th, dT, T)
print("    d/dtheta G = +1*G  (gravity, +1 eigendirection)")
print("    d/dtheta T = -1*T  (time,    -1 eigendirection)")
# the gradient eigenvalues are exactly the eigenvalues of K (note 35)
K = np.array([[0.0, -1.0], [-1.0, 0.0]])
Kev = np.sort(np.linalg.eigvalsh(K))
assert np.allclose(Kev, [-1.0, 1.0])
print(
    f"    K eigenvalues = {np.round(Kev, 12)} == gradient eigenvalues {{-1,+1}}.  MATCH"
)

# ----------------------------------------------------------------------------
print("\n(C) HARD NUMBER  U''(0) = -2  (exact) + honest now-Hessian comparison")
U2_0 = d2U(0.0)
# numerical second derivative as independent check. Central 2nd-diff truncation error
# ~ h^2/12 U'''' and roundoff ~ eps/h^2; h2=1e-4 balances them near machine precision.
h2 = 1e-4
U2_num = (U(h2) - 2 * U(0.0) + U(-h2)) / h2**2
print(f"    U''(0) analytic = {U2_0:.6f}   numeric = {U2_num:.8f}")
assert abs(U2_0 - (-2.0)) < 1e-15
assert abs(U2_num - (-2.0)) < 1e-6
print("    -> U''(0) = -2 < 0  ==> the now is a MAXIMUM of U (unstable hilltop):")
print(
    "       force -U'(theta)=2 sinh(theta) points AWAY from now; chronon falls to horizon."
)
# note-14 now-Hessian amplitude entry (in k):
Gsym2_0_k = 2 * ln_phi**2 + 1.0 / (2 * phi**2)
print(
    f"    note-14  G_sym''(0)|_k = 2 ln^2 phi + 1/(2 phi^2) = {Gsym2_0_k:.6f}  (> 0, a MINIMUM)"
)
assert abs(Gsym2_0_k - 0.654113) < 1e-5
print("    SIGN OPPOSITION (NOT equality): U''(0)=-2 (max) vs G_sym''(0)=+0.654 (min),")
print(
    "    forced by U = -2 G_sym^bare. The audit-honest statement: same cosh backbone,"
)
print("    sign-flipped by the defining relation. We do NOT equate the two curvatures.")
# stripped rapidity-curvature comparison, both in theta:
#   G_sym = osc(k) cosh(theta); rapidity part at now = osc(0)*cosh''(0).
osc0 = osc(0.0)  # = 1/(1+1) = 1/2
rap_part_Gsym_theta = osc0 * 1.0  # cosh''(0)=cosh(0)=1
print(
    f"    stripped rapidity-curvature in theta: osc(0)*cosh''(0) = {rap_part_Gsym_theta:.4f} (note-14 triple +1/2)"
)
assert abs(rap_part_Gsym_theta - 0.5) < 1e-12
print(
    f"    U's rapidity curvature in theta = U''(0) = {U2_0:.1f}; ratio {U2_0 / rap_part_Gsym_theta:+.1f} is just the -2 normalization x sign (no deep meaning)."
)

# ----------------------------------------------------------------------------
print("\n(D) V_grav (note 16 sec5) is the osc-dressed convolved GRADIENT of U, not U")
print("    kernel_Vgrav(d) = sinh(d/phi)/(1+cos^2(2 d ln phi))")
print("    must equal  osc(d) * (-1/2) U'(d/phi)  [since -1/2 U'(x)=sinh(x)]")
maxD = 0.0
for d in [1, 2, 3, 5, 8, 13]:
    x = d / phi
    kernel = np.sinh(d / phi) / (1.0 + np.cos(2 * d * ln_phi) ** 2)
    via_U = osc(d) * (-0.5 * dU(x))  # -1/2 U'(x) = sinh(x)
    maxD = max(maxD, abs(kernel - via_U))
    assert abs(kernel - via_U) < 1e-12
print(f"    max|kernel - osc*(-1/2 U')| over d=1..13 = {maxD:.2e}  -> EXACT")
# and U itself (cosh) is NOT the kernel (sinh): show they differ
diff_cosh = abs(np.sinh(3 / phi) - np.cosh(3 / phi))
print(
    f"    sanity: |sinh(3/phi)-cosh(3/phi)| = {diff_cosh:.4f} != 0  => V_grav~sinh != U~cosh."
)
assert diff_cosh > 1e-3

# ----------------------------------------------------------------------------
print("\n(E) EOM / boost rate: dV0/dk = (1/phi) sinh(theta) = (1/(2 phi)) F(theta)")
maxE = 0.0
for k in [0.3, 1.0, 2.0, 4.0]:
    th = k / phi
    # V0(k) = cosh(k/phi); dV0/dk = (1/phi) sinh(k/phi)
    dV0_num = (np.cosh((k + h) / phi) - np.cosh((k - h) / phi)) / (2 * h)
    dV0_an = (1.0 / phi) * np.sinh(th)
    F = 2 * np.sinh(th)
    rel = (1.0 / (2 * phi)) * F  # should equal dV0_an
    maxE = max(maxE, abs(dV0_num - dV0_an), abs(dV0_an - rel))
    assert abs(dV0_num - dV0_an) < 1e-6
    assert abs(dV0_an - rel) < 1e-13
print(
    f"    max|residual| = {maxE:.2e}  -> dV0/dk = (1/phi)sinh = F/(2 phi). EXACT (1/phi = note-10 connection input)"
)

# ----------------------------------------------------------------------------
print("\n(F) well/curvature numbers and beta(1/phi) recovered from U-channel")
print(f"    U(0) = {U(0.0):.4f}  (extremum value; the standing-mode -cosh apex)")
F1 = 2 * np.sinh(1 / phi)
sum1 = np.exp(1 / phi) + np.exp(-1 / phi)  # G+T = 2 cosh(1/phi) = -U(1/phi)
beta1 = F1 / sum1
print(
    f"    F(1/phi)=2 sinh(1/phi) = {F1:.5f};  G+T = 2 cosh(1/phi) = -U(1/phi) = {sum1:.5f}"
)
print(
    f"    beta(1/phi) = F/(G+T) = {beta1:.4f} = tanh(1/phi) = {np.tanh(1 / phi):.4f}  (note-15 corpus re-analysis 0.548; n=1 shell)"
)
assert abs(beta1 - np.tanh(1 / phi)) < 1e-13
assert abs(beta1 - 0.5498) < 1e-3
# beta = F/(-U): the force over (minus) the potential, both built from the one channel
assert abs(beta1 - (F1 / (-U(1 / phi)))) < 1e-13
print(
    f"    note: beta = F / (-U) = (gradient)/(potential magnitude) = {F1 / (-U(1 / phi)):.4f}.  Clean."
)

# ----------------------------------------------------------------------------
# Extension: the potential-force invariant U^2 - F^2 = 4 L_y = 4.
# This is the reciprocal law T*G=1 (note 35) written purely in potential/force:
#   U = -(G+T) = -2 cosh, F = G-T = 2 sinh, so U^2 - F^2 = (G+T)^2-(G-T)^2 = 4 G T = 4.
# It is the bare (osc->1) reading of the spine invariant M^2 = G_sym^2 - G_flow^2 = osc^2,
# and equivalently 1 - beta^2 = sech^2(theta) (the Lorentz gamma in disguise: -U=2 gamma).
print(
    "\n(G) EXTENSION: potential-force invariant U^2 - F^2 = 4 L_y = 4  (reciprocal law)"
)
maxG = 0.0
for th in [-3.0, -2.0, -1.0, -1 / phi, 0.0, 1 / phi, 1.0, 2.0, 3.0]:
    G, T = np.exp(th), np.exp(-th)
    Uv, Fv = U(th), -dU(th)  # U=-2cosh, F=-U'=2 sinh
    inv = Uv**2 - Fv**2
    maxG = max(maxG, abs(inv - 4.0), abs(inv - 4.0 * G * T))
    assert abs(inv - 4.0) < 1e-12
    assert abs(inv - 4.0 * G * T) < 1e-12  # = 4 L_y since G*T=1
    # beta on the hyperbola: 1 - beta^2 = sech^2(theta) = 4/U^2
    beta = Fv / (-Uv)
    assert abs((1 - beta**2) - (1.0 / np.cosh(th) ** 2)) < 1e-12
    assert abs((1 - beta**2) - (4.0 / Uv**2)) < 1e-12
print(
    f"    max|U^2 - F^2 - 4| (and vs 4 G T) over theta in [-3,3] = {maxG:.2e}  -> EXACT"
)
print("    => (F, -U) ride the hyperbola (-U)^2 - F^2 = 4; -U=2 gamma, F=2 beta gamma,")
print(
    "       1 - beta^2 = sech^2(theta). The reciprocal law L_y=1 in potential-force form."
)

print("\nALL CHECKS PASSED — U(theta)=-2 cosh(theta): F=-U'=2 sinh; null rays are the")
print(
    "+-1 gradient eigendirections (=K-spectrum); U''(0)=-2 (now is a MAXIMUM, sign-opposite"
)
print(
    "to the note-14 amplitude minimum +0.654); V_grav is the dressed GRADIENT of U, not U;"
)
print("dV0/dk=(1/phi)sinh=F/(2phi); beta(1/phi)=tanh(1/phi)=0.5498.")
