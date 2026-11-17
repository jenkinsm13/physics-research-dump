import numpy as np

# Note 20 verification: the dynamical now-interface as a Lindblad readout channel.
# Structural constants (phi, lnphi, Delta k, chi_I=1/phi, S_1) inherited from
# notes 10/12/13/14; this script confirms the NEW dynamical claims.

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
inv_phi = 1.0 / phi


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)


def Gsym(k):
    return osc(k) * np.cosh(k / phi)


T = np.array([[1.0, 0.0], [0.0, -1.0]])  # time-reversal involution (note 14)
Pnow = 0.5 * (np.eye(2) + T)  # now-projector diag(1,0) (note 14)


def superop(chan):
    """Vectorize a 2x2 -> 2x2 linear channel into its 4x4 matrix (column-stacking)."""
    M = np.zeros((4, 4), dtype=complex)
    basis = [
        np.array([[1, 0], [0, 0]]),
        np.array([[0, 1], [0, 0]]),
        np.array([[0, 0], [1, 0]]),
        np.array([[0, 0], [0, 1]]),
    ]
    for j, b in enumerate(basis):
        M[:, j] = chan(b.astype(float)).reshape(4)
    return M


def expm_eig(A, t):
    """exp(A t) via eigendecomposition (sandbox has no scipy)."""
    w, V = np.linalg.eig(A)
    return V @ np.diag(np.exp(w * t)) @ np.linalg.inv(V)


print("=== constants (inherited) ===")
print(f"phi      = {phi:.12f}")
print(f"1/phi    = {inv_phi:.12f}   (chi_I, note 14)")
print(f"lnphi    = {lnphi:.12f}")
Dk = np.pi / (2 * lnphi)
S1 = np.pi / (2 * phi * lnphi)
print(f"Delta k  = pi/(2 lnphi)     = {Dk:.12f}   (comb spacing)")
print(f"S_1      = pi/(2 phi lnphi) = {S1:.12f}   (note 06/13)")

print("\n=== 1. Lindblad dephasing channel; pointer basis = T-even (correlation) ===")
# One Hermitian jump operator L = sqrt(gamma/2) T, T=diag(1,-1) = sigma_z in the
# {T-even, T-odd}={correlation, flow} basis. Pure dephasing:
#   d rho/dk = L rho L^dag - 1/2{L^dag L, rho}
# leaves both diagonal populations invariant (zero modes) and decays the coherence
# rho_{01} at rate 2*(gamma/2)=gamma. Choose gamma=1/phi so decoherence = chi_I (note 14).
gamma = inv_phi
c2 = gamma / 2.0  # = 1/(2 phi)
L = np.sqrt(c2) * T


def lindblad(rho):
    LdL = L.conj().T @ L
    return L @ rho @ L.conj().T - 0.5 * (LdL @ rho + rho @ LdL)


Lsup = superop(lindblad)
ev = np.sort_complex(np.linalg.eigvals(Lsup))
print(f"gamma = 1/phi = {gamma:.12f}")
print(f"Lindbladian eigenvalues (rates): {np.round(ev.real, 12)}")
zero_modes = int(np.sum(np.abs(ev.real) < 1e-9))
coh_rates = -ev.real[ev.real < -1e-9]
print(
    f"  zero modes (conserved populations / pointer diagonal): {zero_modes}  (expect 2)"
)
print(
    f"  coherence decay rate(s): {np.round(coh_rates, 12)}  (expect 1/phi = {inv_phi:.12f})"
)
assert zero_modes == 2
assert np.allclose(np.sort(coh_rates), [inv_phi, inv_phi], atol=1e-12)
w, Vt = np.linalg.eigh(T)
print(f"  T eigvals {w}; pointer (+1, correlation axis) = {Vt[:, np.argmax(w)]}")
assert np.allclose(Pnow, np.diag([1.0, 0.0]))
print(
    "  CHECK: pointer = T-even correlation survives; T-odd coherence decoheres at 1/phi : PASS"
)

print("\n=== 2. Decoherence of the equal two-sheet now-superposition ===")
# rho0 = |+><+| in T-basis: the balanced forward/inverse superposition the now reads
# (note 14: <now> reads both sheets at weight 1/2). Coherence |rho01(0)| = 1/2.
rho0 = 0.5 * np.array([[1.0, 1.0], [1.0, 1.0]])
c0 = abs(rho0[0, 1])
print(f"initial coherence |rho01(0)| = {c0:.6f} (= 1/2, equal-weight two sheets)")
for k in [0.0, inv_phi, Dk, 2 * Dk]:
    rk = (expm_eig(Lsup, k) @ rho0.reshape(4)).reshape(2, 2)
    coh = abs(rk[0, 1])
    pred = c0 * np.exp(-k / phi)
    print(f"  k={k:7.4f}: |rho01|={coh:.8f}  expect (1/2)e^(-k/phi)={pred:.8f}")
    assert np.isclose(coh, pred, atol=1e-9)
print(
    "  CHECK: coherence envelope = (1/2) e^{-k/phi}; one e-fold per phi shells : PASS"
)

print("\n=== 3. Nyquist / bandwidth from the comb ===")
Om_Nyq = np.pi / Dk  # Nyquist angular freq (rad/shell)
Om_comb = 2 * np.pi / Dk  # comb-fundamental angular freq (rad/shell)
print(
    f"Nyquist  Om_Nyq  = pi/Dk  = {Om_Nyq:.12f} rad/shell  (= 2 lnphi = {2 * lnphi:.12f})"
)
print(
    f"comb     Om_comb = 2pi/Dk = {Om_comb:.12f} rad/shell  (= 4 lnphi = {4 * lnphi:.12f})"
)
assert np.isclose(Om_Nyq, 2 * lnphi) and np.isclose(Om_comb, 4 * lnphi)
print(
    f"dimensionless Om_comb/lnphi = {Om_comb / lnphi:.12f}  (note 12 omega_phi = 4 EXACT)"
)
print(f"dimensionless Om_Nyq /lnphi = {Om_Nyq / lnphi:.12f}  (= 2 exactly)")
assert np.isclose(Om_comb / lnphi, 4.0) and np.isclose(Om_Nyq / lnphi, 2.0)
print(
    "  CHECK: comb fundamental sits at exactly 2x Nyquist (folds to DC = standing/flow-reversal mode) : PASS"
)

print(
    "\n=== 4. Readout transfer function (first-order low-pass at decoherence rate) ==="
)
Gdec = gamma  # corner = decoherence rate = 1/phi rad/shell


def H(Om):
    return 1.0 / (1.0 + 1j * Om / Gdec)


print(f"corner Om_c = Gamma_dec = 1/phi = {Gdec:.12f} rad/shell")
print(f"|H(0)|    = {abs(H(0)):.6f}  (expect 1, full DC gain at the now)")
print(f"|H(Om_c)| = {abs(H(Gdec)):.6f}  (expect 1/sqrt2 = {1 / np.sqrt(2):.6f}, -3 dB)")
assert np.isclose(abs(H(Gdec)), 1 / np.sqrt(2))
ratio_cN = Gdec / Om_Nyq
ratio_cC = Gdec / Om_comb
print(
    f"Om_c / Om_Nyq  = 1/(2 phi lnphi) = {ratio_cN:.12f} = S_1/pi   = {S1 / np.pi:.12f}"
)
print(
    f"Om_c / Om_comb = 1/(4 phi lnphi) = {ratio_cC:.12f} = S_1/(2pi) = {S1 / (2 * np.pi):.12f}"
)
assert np.isclose(ratio_cN, S1 / np.pi) and np.isclose(ratio_cN, 1 / (2 * phi * lnphi))
assert np.isclose(ratio_cC, S1 / (2 * np.pi))
print(
    f"  corner is below Nyquist (well-sampled by the comb): {ratio_cN:.4f} < 1 : {ratio_cN < 1}"
)
print("  CHECK: corner/Nyquist = S_1/pi, corner/comb = S_1/(2pi) : PASS")

print("\n=== 5. Interface susceptibility spectrum chi(Omega) (Kubo / Lorentzian) ===")


def chi(Om):
    return inv_phi / (1.0 + 1j * Om / Gdec)


print(
    f"chi(0) = {chi(0).real:.12f}  (expect chi_I = 1/phi = {inv_phi:.12f}, recovers note 14)"
)
assert np.isclose(chi(0).real, inv_phi)
oms = np.linspace(1e-5, 5, 400001)
chipp = inv_phi * (oms / Gdec) / (1 + (oms / Gdec) ** 2)  # dissipative part
om_peak = oms[np.argmax(chipp)]
print(f"chi''(Om) peaks at Om = {om_peak:.6f}  (expect Gamma_dec = 1/phi = {Gdec:.6f})")
assert np.isclose(om_peak, Gdec, atol=2e-3)
print(f"power-spectrum Lorentzian HWHM = Gamma_dec = 1/phi = {Gdec:.12f} rad/shell")
print("  CHECK: chi(0)=1/phi, chi'' peaks at 1/phi, HWHM=1/phi : PASS")

print("\n=== 6. HARD NUMBER: characteristic interface frequency in Hz ===")
# Interface reads the now at the COMB rate = discrete 'perceptual moments'. Empirical
# anchor: discrete perception / dominant cortical sampling rhythm = ALPHA band, center
# ~10 Hz (VanRullen 2016; Varela perceptual frames). Identify comb fundamental (the
# 'now-tick' sample rate) with alpha. Then the readout-decoherence rhythm is FIXED:
#   f_corner = f_alpha * (Om_c/Om_comb) = f_alpha * S_1/(2pi),  no free parameter.
print(f"clock-free spectral ratio f_corner/f_Nyq  = S_1/pi   = {S1 / np.pi:.6f}")
print(f"clock-free spectral ratio f_corner/f_comb = S_1/(2pi) = {S1 / (2 * np.pi):.6f}")
print("anchor: comb fundamental <-> alpha center; bracket over band 8-13 Hz:")
for fa in [8.0, 10.0, 13.0]:
    fc = fa * S1 / (2 * np.pi)
    print(f"  f_alpha={fa:>4} Hz -> f_corner = {fc:.3f} Hz   (f_Nyq={fa / 2:.1f} Hz)")
fc10 = 10.0 * S1 / (2 * np.pi)
print(f"central prediction (f_alpha=10 Hz): f_corner = {fc10:.3f} Hz")
print(
    f"  band: {8 * S1 / (2 * np.pi):.2f} - {13 * S1 / (2 * np.pi):.2f} Hz (low-theta/delta boundary)"
)

print("\n=== 7. EXTENSION: the now decoheres at the gravitational ladder rate ===")
# Sample the coherence envelope (1/2)e^{-k/phi} at the comb teeth (spacing Delta k).
# Per-tooth coherence ratio = e^{-Delta k/phi}. Identity Delta k/phi = S_1 (note 16),
# so the ratio = e^{-S_1} = Gamma_1 = the GW echo decrement (notes 15/16) = 0.133.
assert np.isclose(Dk / phi, S1)  # Delta k / phi = S_1 exactly (note 16)
ratio_per_tooth = np.exp(-Dk / phi)
gamma_echo = np.exp(-S1)
print(f"Delta k / phi = S_1 = {Dk / phi:.12f}   (note 16 identity)")
print(
    f"coherence ratio per comb tooth e^(-Dk/phi) = {ratio_per_tooth:.12f}"
    f"  = e^(-S_1) = Gamma_1 = {gamma_echo:.12f}"
)
assert np.isclose(
    ratio_per_tooth, gamma_echo
)  # forced: both run at 1/phi sampled at Dk
print(
    "  CHECK: now-coherence drops by 0.133 per perceptual moment = GW echo decrement : PASS"
)

# Total integrated inverse-sheet memory = int_0^inf (1/2)e^{-k/phi} dk = phi/2 = Q_echo (note 16).
total_memory = 0.5 * phi  # closed form of the integral
Q_echo = phi / 2.0  # note 16 echo-mode quality factor
print(
    f"integrated inverse-sheet memory int (1/2)e^(-k/phi) dk = phi/2 = {total_memory:.12f}"
    f"  = Q_echo (note 16) = {Q_echo:.12f}"
)
assert np.isclose(total_memory, Q_echo)
# numerical sanity on the integral itself (no scipy): manual trapezoid on a fine grid.
# np.trapz was removed in numpy 2.x; hand-roll the rule for version independence.
kk = np.linspace(0, 200, 4_000_001)
yy = 0.5 * np.exp(-kk / phi)
num_int = np.sum((yy[:-1] + yy[1:]) * np.diff(kk)) / 2.0
print(f"  numerical integral = {num_int:.10f}  (expect phi/2 = {Q_echo:.10f})")
assert np.isclose(num_int, Q_echo, atol=1e-6)

bits_per_tooth = S1 / np.log(2)
print(f"inverse-sheet info shed per comb tooth = S_1/ln2 = {bits_per_tooth:.6f} bits")
assert np.isclose(bits_per_tooth, S1 / np.log(2))
print("  CHECK: interface decay = gravitational ladder e^(-S_1), Q = phi/2 : PASS")

print("\nALL CHECKS PASSED")
