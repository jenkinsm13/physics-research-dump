
# tts_massmix_gridrefine.py
# Deterministic grid + targeted refinement for TTS mass–mixing ansatz (NumPy-only)
# Author: (you + assistant)
# Usage: python tts_massmix_gridrefine.py

import numpy as np, time, sys

pi = np.pi; deg = pi/180.0
rng = np.random.default_rng(20250905)

# --- Experimental inputs
m_e_vec = np.array([0.00051099895, 0.1056583755, 1.77686])        # GeV
m_u_vec = np.array([0.0022, 1.27, 172.76])                        # GeV
m_d_vec = np.array([0.0047, 0.096, 4.18])                         # GeV
Vabs_target = np.array([[0.974,0.226,0.0036],
                        [0.226,0.973,0.042 ],
                        [0.0087,0.041,0.999]])

# Neutrino targets
dm21   = 7.4e-5   # eV^2
dm31   = 2.5e-3   # eV^2
th12_t = 33.4*deg
th23_t = 49.0*deg
th13_t = 8.6*deg

# --- Shared left ordinals
rL = np.array([0,1,2], dtype=int)

def D_beta(beta: float) -> np.ndarray:
    return np.diag(np.exp(beta * rL).astype(complex))

def givens(i, j, theta, phi):
    U = np.eye(3, dtype=complex); c,s = np.cos(theta), np.sin(theta)
    U[i,i]=c; U[j,j]=c; U[i,j]=np.exp(1j*phi)*s; U[j,i]=-np.exp(-1j*phi)*s
    return U

def U_from(angles, phases):
    t12,t13,t23 = angles; p12,p13,p23 = phases
    return givens(1,2,t23,p23) @ givens(0,2,t13,p13) @ givens(0,1,t12,p12)

def svd_LR(M):
    U,s,Vh = np.linalg.svd(M)
    return U, s, Vh.conj().T

def mass_fit_scale(pred, target):
    p = np.sort(np.clip(pred,1e-24,None))
    t = np.sort(np.clip(target,1e-24,None))
    return float(np.exp(np.mean(np.log(t) - np.log(p))))

def mass_ratio_loss(pred, target):
    p = np.sort(np.clip(pred,1e-24,None))
    t = np.sort(np.clip(target,1e-24,None))
    return float(np.mean((np.log(p/t))**2))

def ckm(Mu, Md):
    Uu,_,_ = svd_LR(Mu); Ud,_,_ = svd_LR(Md)
    return Uu.conj().T @ Ud

def angles(U):
    s13 = np.abs(U[0,2]); th13 = np.arcsin(np.clip(s13,0,1)); c13 = np.cos(th13)+1e-12
    s12 = np.abs(U[0,1])/c13; s23 = np.abs(U[1,2])/c13
    th12 = np.arcsin(np.clip(s12,0,1)); th23 = np.arcsin(np.clip(s23,0,1))
    num  = -U[0,0]*U[1,2]*np.conj(U[0,2])*np.conj(U[1,0]); delta = np.angle(num)
    return th12, th23, th13, delta

def texture_LR(alpha, rR, phases, eps, projectors=None, weights=None):
    rR = np.array(rR, dtype=int)
    DLR = np.abs(rL[:,None] - rR[None,:])
    Y   = np.exp(-alpha * DLR).astype(complex)
    phi12, phi13, phi23 = phases
    Ph = np.eye(3, dtype=complex)
    Ph[0,1] = np.exp(1j*phi12); Ph[1,0] = np.exp(-1j*phi12)
    Ph[0,2] = np.exp(1j*phi13); Ph[2,0] = np.exp(-1j*phi13)
    Ph[1,2] = np.exp(1j*phi23); Ph[2,1] = np.exp(-1j*phi23)
    Y = Y * Ph
    if projectors is not None and weights is not None:
        for P,w in zip(projectors, weights): Y = Y + eps * w * P
    else:
        Y = Y + eps * np.ones((3,3), dtype=complex)
    return Y

def build_sector(alpha, eps, rR, beta, kappa, phases, Xa, Xp, Ya=None, Yp=None, projs=None, wts=None):
    X = U_from(Xa, Xp)
    Y = U_from(Ya, Yp).conj().T if Ya is not None else np.eye(3, dtype=complex)
    core = D_beta(beta) + kappa * texture_LR(alpha, rR, phases, eps, projs, wts)
    return X @ core @ Y

def pretty_mat(M):
    return "\n".join(["  " + " ".join([f"{x:8.4f}" for x in row]) for row in M])

# Neutrino projectors
v1 = np.ones(3)/np.sqrt(3); P1 = np.outer(v1, v1)
u  = np.array([ 1.0, 0.0, -1.0]); u/=np.linalg.norm(u); P2 = np.outer(u, u)

def stageA_grid_refine(alpha_grid, eps_grid, refine_per_grid=400):
    best = (1e9, None)
    for alpha in alpha_grid:
        for eps in eps_grid:
            for _ in range(refine_per_grid):
                rRe   = rng.integers(0, 11, 3)
                beta  = rng.uniform(0.5, 6.0)
                kappa = rng.uniform(0.0, 1.0)
                ph    = rng.uniform(0.0, 2*pi, 3)
                Xa    = rng.uniform(0.0, 0.2, 3); Xp = rng.uniform(0.0, 2*pi, 3)
                Ya    = rng.uniform(0.0, 0.2, 3); Yp = rng.uniform(0.0, 2*pi, 3)
                Me0   = build_sector(alpha, eps, rRe, beta, kappa, ph, Xa, Xp, Ya, Yp)
                _, s, _ = svd_LR(Me0)
                Λ = mass_fit_scale(s, m_e_vec); loss = mass_ratio_loss(Λ*s, m_e_vec)
                if loss < best[0]:
                    best = (loss, dict(alpha=alpha, eps=eps, rRe=rRe, beta=beta, kappa=kappa,
                                        ph=ph, Xa=Xa, Xp=Xp, Ya=Ya, Yp=Yp, Λ=Λ, Me=Λ*Me0))
    return best

def stageB_grid_refine(alpha, eps, RUS, RDS, trials=400):
    W = np.ones((3,3)); W[0,2]=W[2,0]=160.0; W[1,2]=W[2,1]=26.0; W[0,1]=W[1,0]=6.0
    best = (1e9, None)
    for rRu in RUS:
        for rRd in RDS:
            for _ in range(trials):
                betau  = rng.uniform(2.0, 6.5);   kappau = rng.uniform(0.00, 0.20)
                betad  = rng.uniform(2.0, 6.5);   kappad = rng.uniform(0.12, 0.38)
                phu = rng.uniform(0.0, 2*pi, 3);  phd = rng.uniform(0.0, 2*pi, 3)
                Xu = U_from(rng.uniform(0.0,0.20,3), rng.uniform(0.0,2*pi,3))
                Yu = U_from(rng.uniform(0.0,0.50,3), rng.uniform(0.0,2*pi,3)).conj().T
                Xd = U_from(rng.uniform(0.0,0.20,3), rng.uniform(0.0,2*pi,3))
                Yd = U_from(rng.uniform(0.0,0.50,3), rng.uniform(0.0,2*pi,3)).conj().T
                Mu0 = Xu @ (D_beta(betau) + kappau * texture_LR(alpha, rRu, phu, eps)) @ Yu
                Md0 = Xd @ (D_beta(betad) + kappad * texture_LR(alpha, rRd, phd, eps)) @ Yd
                _, su, _ = svd_LR(Mu0); _, sd, _ = svd_LR(Md0)
                Λu = mass_fit_scale(su, m_u_vec); Λd = mass_fit_scale(sd, m_d_vec)
                Mu = Λu*Mu0; Md = Λd*Md0
                su_fit = np.sort(Λu*su); sd_fit = np.sort(Λd*sd)
                V  = ckm(Mu, Md); Vabs = np.abs(V)
                Lm   = mass_ratio_loss(su_fit, m_u_vec) + mass_ratio_loss(sd_fit, m_d_vec)
                Lckm = float(np.mean(W*(Vabs - Vabs_target)**2))
                Ltiny= 3.8*(Vabs[0,2]-0.0036)**2 + 1.4*(Vabs[1,2]-0.042)**2 + 0.7*(Vabs[0,1]-0.226)**2
                loss = 1.5*Lm + 10.0*Lckm + 12.0*Ltiny
                if loss < best[0]:
                    best = (loss, dict(Mu=Mu, Md=Md, V=V, su=su_fit, sd=sd_fit,
                                       rRu=rRu, rRd=rRd,
                                       betau=betau, betad=betad,
                                       kappau=kappau, kappad=kappad,
                                       Λu=Λu, Λd=Λd,
                                       Lm=Lm, Lckm=Lckm, Ltiny=Ltiny))
    return best

def stageC_grid_refine(alpha, eps, Me, RNS, trials=1200):
    Ue,_,_ = svd_LR(Me)
    best = (1e9, None)
    v1 = np.ones(3)/np.sqrt(3); P1 = np.outer(v1, v1)
    u  = np.array([ 1.0, 0.0, -1.0]); u/=np.linalg.norm(u); P2 = np.outer(u, u)
    for rRn in RNS:
        for _ in range(trials):
            beta_n  = rng.uniform(-0.1, 0.3)
            kappa_n = rng.uniform(1.2, 2.2)
            phases  = rng.uniform(0.0, 2*pi, 3)
            g1      = rng.uniform(2.0, 4.0)
            g2      = rng.uniform(-2.8, -0.6)
            Xa = rng.uniform(0.0, 0.3, 3);  Xp = rng.uniform(0.0, 2*pi, 3)
            Ya = rng.uniform(0.0, 0.3, 3);  Yp = rng.uniform(0.0, 2*pi, 3)
            Mnu0 = build_sector(alpha, eps, rRn, beta_n, kappa_n, phases, Xa, Xp, Ya, Yp,
                                projs=[P1,P2], wts=[g1,g2])
            Unu, s0, _ = svd_LR(Mnu0)
            m0 = np.sort(s0); dm31_0 = m0[2]**2 - m0[0]**2
            if dm31_0 <= 0: continue
            gscale = np.sqrt(dm31 / dm31_0); m = gscale * m0
            UPMNS = Ue.conj().T @ Unu
            th12, th23, th13, delta = angles(UPMNS)
            dm21_pred = m[1]**2 - m[0]**2
            Ldm  = ((dm21_pred - dm21)/dm21)**2
            Lang = 1.8*((th12-th12_t)/th12_t)**2 + 1.8*((th23-th23_t)/th23_t)**2 + 1.2*((th13-th13_t)/th13_t)**2
            loss = 6.0*Ldm + Lang
            if loss < best[0]:
                m_bb=float(np.abs((UPMNS[0,0]**2)*m[0] + (UPMNS[0,1]**2)*m[1] + (UPMNS[0,2]**2)*m[2]))
                Σm=float(np.sum(m))
                best = (loss, dict(m=m, U=UPMNS, delta=delta,
                                   m_bb=m_bb, sum_m=Σm,
                                   beta_n=beta_n, kappa_n=kappa_n,
                                   rRn=rRn, g1=g1, g2=g2,
                                   Ldm=Ldm, Lang=Lang))
    return best

def run(grid_refine_A=400, grid_refine_B=400, grid_refine_C=1200):
    t0=time.time()
    # Stage A grid
    alpha_grid = np.array([0.8, 1.0, 1.2, 1.5])
    eps_grid   = np.array([0.03, 0.06, 0.09, 0.12])
    A_loss, A = stageA_grid_refine(alpha_grid, eps_grid, refine_per_grid=grid_refine_A)
    print(f"Stage A — leptons: loss={A_loss:.6g}   alpha={A['alpha']:.4f}  eps={A['eps']:.4f}  rR^e={A['rRe']}")

    # Stage B grid
    RUS = np.array([[0,1,10],[0,2,10],[1,2,11],[0,1,11],[0,3,10]])
    RDS = np.array([[0,2,8],[1,2,8],[0,1,8],[0,2,9],[1,3,8]])
    B_loss, B = stageB_grid_refine(A['alpha'], A['eps'], RUS, RDS, trials=grid_refine_B)
    print(f"\nStage B — quarks: loss={B_loss:.6g}  (Lm={B['Lm']:.6g}, Lckm={B['Lckm']:.6g}, Ltiny={B['Ltiny']:.6g})")
    print("  rR^u=", B["rRu"], "  rR^d=", B["rRd"])
    print("  up masses fit (GeV):   ", B["su"])
    print("  down masses fit (GeV): ", B["sd"])
    print("  |V_CKM| (fit):\n"   + pretty_mat(np.abs(B["V"])))
    print("  |V_CKM| (target):\n"+ pretty_mat(Vabs_target))

    # Stage C grid
    RNS = np.array([[0,1,2],[0,1,3],[0,2,3],[1,2,3]])
    C_loss, C = stageC_grid_refine(A['alpha'], A['eps'], A['Me'], RNS, trials=grid_refine_C)
    t12,t23,t13,_ = angles(C["U"])
    print(f"\nStage C — neutrinos: loss={C_loss:.6g}  (Ldm={C['Ldm']:.6g}, Lang={C['Lang']:.6g})")
    print("  rR^ν=", C["rRn"], f"  beta_ν={C['beta_n']:.3f}  kappa_ν={C['kappa_n']:.3f}  (g1,g2)=({C['g1']:.3f},{C['g2']:.3f})")
    print("  ν masses (eV):         ", np.array2string(C["m"], precision=6))
    print("  Δm21, Δm31 (eV^2):     ", (C["m"][1]**2 - C["m"][0]**2, C["m"][2]**2 - C["m"][0]**2))
    print("  PMNS angles (deg):     ", f"θ12={t12/deg:.2f}  θ23={t23/deg:.2f}  θ13={t13/deg:.2f}")
    print("  δ_CP (deg):            ", f"{C['delta']/deg:.1f}")
    print("  m_beta_beta (eV):      ", f"{C['m_bb']:.5f}")
    print("  Σm (eV):               ", f"{C['sum_m']:.5f}")

    print("\nElapsed (s):", round(time.time()-t0,2))
    return A,B,C

if __name__ == "__main__":
    # You can increase these numbers for deeper searches on your machine.
    run(grid_refine_A=600, grid_refine_B=800, grid_refine_C=1800)
