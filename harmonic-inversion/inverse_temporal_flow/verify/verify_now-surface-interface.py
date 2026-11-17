import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)


def kappa(k):  # signed-ordinal kernel; +k retarded, -k advanced
    return osc(k) * np.exp(-k / phi)


def Gsym(k):
    return osc(k) * np.cosh(k / phi)


def Gflow(k):
    return -osc(k) * np.sinh(k / phi)


def Sbr(k):
    th = k / phi
    return np.log(2 * np.cosh(th)) - th * np.tanh(th)


def Vvis(k):  # note 06 visibility
    th = k / phi
    return 1.0 / (2 * np.cosh(2 * th) + 1)


def R(k):  # note 09 non-reciprocity ratio = -tanh(k/phi)
    return Gflow(k) / Gsym(k)


print("=== Sanity at the now (k=0) ===")
print(f"osc(0)      = {osc(0):.15f}  (expect 0.5)")
print(f"kappa(+0)   = {kappa(0):.15f}  (expect 0.5)")
print(f"kappa(-0)   = {kappa(-0.0):.15f}  (expect 0.5)")
print(f"Gsym(0)     = {Gsym(0):.15f}  (expect 0.5)")
print(f"Gflow(0)    = {Gflow(0):.2e}  (expect 0)")
print(f"Sbr(0)      = {Sbr(0):.15f}  (expect ln2={np.log(2):.15f})")
print(f"Vvis(0)     = {Vvis(0):.15f}  (expect 1/3={1 / 3:.15f})")

print("\n=== Correction 1: boost does NOT fix V(0); involution T does ===")


def V(k):
    th = k / phi
    return np.array([np.cosh(th), -np.sinh(th)])


def Lambda(alpha):  # boost by rapidity alpha
    return np.array(
        [[np.cosh(alpha), -np.sinh(alpha)], [-np.sinh(alpha), np.cosh(alpha)]]
    )


T = np.array([[1.0, 0.0], [0.0, -1.0]])  # time reversal k->-k on (Gsym,Gflow)
alpha = 1.0 / phi  # one-shell boost
V0 = V(0.0)
LV0 = Lambda(alpha) @ V0
print(f"V(0)            = {V0}")
print(f"Lambda(1/phi)V0 = {LV0}  -> should equal V(phi*alpha)=V(1)={V(1.0)}")
print(f"   boost fixes V0?  {np.allclose(LV0, V0)}  (expect False)")
print(f"   == V(phi*alpha)? {np.allclose(LV0, V(phi * alpha))}  (expect True)")
print(
    f"T V0            = {T @ V0}  -> involution fixes V0? {np.allclose(T @ V0, V0)}  (expect True)"
)
# eigenvectors of boost are the null directions, not V0:
w, vec = np.linalg.eig(Lambda(alpha))
print(
    f"   boost eigenvalues = {np.real_if_close(w)} (e^∓alpha, null directions; no real fixed nonzero vector for alpha!=0)"
)

print("\n=== Projector onto the now-surface ===")
P = 0.5 * (np.eye(2) + T)
print(f"P_now = 0.5(I+T) =\n{P}")
print(f"P^2 == P ? {np.allclose(P @ P, P)}  (idempotent)")
pe = np.linalg.eigvalsh(P)
print(f"eigenvalues(P_now) = {pe}  (expect {{0,1}})")
print(
    f"P_now V(0) = {P @ V0}  == V(0)? {np.allclose(P @ V0, V0)}  (now is +1 eigenspace)"
)
# off-now: project a deeper two-vector
Vk = V(1.0)
print(f"P_now V(1) = {P @ Vk}  (kills the flow/gravity component -sinh)")

print("\n=== Correction 2 + THE NEW EQUATION: Jacobian of readout at the now ===")
h = 1e-6
dGsym = (Gsym(h) - Gsym(-h)) / (2 * h)
dGflow = (Gflow(h) - Gflow(-h)) / (2 * h)
dR = (R(h) - R(-h)) / (2 * h)
print(
    f"d/dk Gsym |0  = {dGsym:.10f}  (expect 0: osc'(0)=0 AND cosh'(0)=0 -> correlation stationary)"
)
print(f"d/dk Gflow|0  = {dGflow:.10f}  (expect -1/(2phi) = {-1 / (2 * phi):.10f})")
print(f"d/dk R   |0  = {dR:.10f}  (expect -1/phi = {-1 / phi:.10f})")
# analytic confirmation of Gflow'(0):
# Gflow = -sinh(k/phi)*osc(k); at 0 sinh kills osc' term; osc(0)=1/2; sinh'(0)=1/phi
print(f"analytic Gflow'(0) = -(1/phi)*osc(0) = {-(1 / phi) * osc(0):.10f}")
print(
    f"analytic R'(0)     = Gflow'(0)/Gsym(0) = {(-(1 / phi) * osc(0)) / Gsym(0):.10f}"
)

print("\n=== osc stationary at now (why correlation is a critical point) ===")
dosc = (osc(h) - osc(-h)) / (2 * h)
print(f"d/dk osc |0 = {dosc:.2e}  (expect 0; cos^2 has zero slope at k=0)")

print("\n=== Sign of the critical point: now is a MINIMUM of G_sym, not a max ===")
hb = 1e-3  # larger step: G_sym'' is roundoff-sensitive at h=1e-6
d2Gsym = (Gsym(hb) - 2 * Gsym(0) + Gsym(-hb)) / (hb * hb)
expect = 2 * lnphi**2 + 1 / (
    2 * phi**2
)  # analytic G_sym''(0) = 2 ln^2 phi + 1/(2 phi^2)
print(
    f"d2/dk2 Gsym|0 = {d2Gsym:.6f}  (expect 2 ln^2 phi + 1/(2 phi^2) = {expect:.6f} > 0 -> MINIMUM)"
)
print(
    f"G_sym(0)={Gsym(0):.6f}, G_sym(0.5)={Gsym(0.5):.6f}, G_sym(1)={Gsym(1):.6f}  (strictly increasing into bulk)"
)

print("\n=== Interface susceptibility chi_I = |R'(0)| = 1/phi ===")
print(f"chi_I = 1/phi = phi-1 = {1 / phi:.12f}")
print(f"check 1/phi == phi-1 ? {np.isclose(1 / phi, phi - 1)}")

print("\n=== Curvature of branch entropy at the now (second-order readout) ===")
# analytic: Sbr = ln(2cosh th) - th tanh th, th=k/phi; in th, Sbr''(0)=-1, so in k: -1/phi^2.
# finite difference is roundoff-dominated (cancellation ~ eps*|Sbr|/h^2); analytic value is load-bearing.
hb2 = 1e-3
d2Sbr = (Sbr(hb2) - 2 * Sbr(0) + Sbr(-hb2)) / (hb2 * hb2)
print(
    f"d2/dk2 Sbr|0 (fd, h=1e-3) = {d2Sbr:.8f}  (analytic -1/phi^2 = {-1 / phi**2:.8f})"
)

print("\n=== FIX: visibility curvature is NOT 1/phi^2; it is 8/(9 phi^2) ===")
# V(k)=1/(2cosh(2 th)+1), th=k/phi. In th: V''(0)=-8/9 (expand cosh2th=1+2th^2 ->
# denom 3+4th^2 -> V ~ (1/3)(1-(4/3)th^2)), so in k: -8/(9 phi^2). DIFFERENT from Sbr.
d2V = (Vvis(hb2) - 2 * Vvis(0) + Vvis(-hb2)) / (hb2 * hb2)
print(
    f"d2/dk2 V|0 (fd, h=1e-3) = {d2V:.8f}  (analytic -8/(9 phi^2) = {-8 / (9 * phi**2):.8f})"
)
print(
    f"balance-curvature ratio V''/Sbr'' = {d2V / d2Sbr:.10f}  (exact 8/9 = {8 / 9:.10f}, phi-blind)"
)

print("\n=== EXTENSION: the now-Hessian rapidity-curvature spectrum ===")
hb = 1e-3
d2Gsym = (Gsym(hb) - 2 * Gsym(0) + Gsym(-hb)) / (hb * hb)
# Strip the lattice (osc) curvature 2 ln^2 phi off the amplitude channel; the residual
# amplitude curvature and BOTH balance curvatures are pure rapidity curvatures ~ phi^{-2}.
lattice = 2 * lnphi**2
rap = [phi**2 * (d2Gsym - lattice), phi**2 * d2Sbr, phi**2 * d2V]
print(f"lattice curvature 2 ln^2 phi          = {lattice:.10f}")
print(
    f"Gsym''(0) - 2 ln^2 phi = 1/(2phi^2)   = {d2Gsym - lattice:.10f}  (analytic {1 / (2 * phi**2):.10f})"
)
print(f"rapidity spectrum phi^2*[amp_res, Sbr, V] = {[round(x, 6) for x in rap]}")
print(
    f"   expect (+1/2, -1, -8/9) = ({0.5}, {-1.0}, {-8 / 9:.6f})  -- parameter-free, lattice-blind"
)
print("signature (+,-,-): amplitude rises into bulk; both balance observables fall")
