
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fs = 1e6
T = 0.0005
N = int(fs * T)
t = np.linspace(0, T, N)

L_core = 150e-6
R_wire = 0.3
R_core = 0.5
C_res = 1e-6
V_src_rms = 5.0
f0 = 50e3
omega0 = 2 * np.pi * f0

def chronon_mod(t, freq=120e3, amp=1.0):
    return amp * np.sin(2 * np.pi * freq * t)

def simulate_case(pump=False):
    V_src = np.sqrt(2) * V_src_rms * np.sin(omega0 * t)
    if pump:
        V_src += 1.0 * chronon_mod(t)

    I = np.zeros_like(t)
    V_C = np.zeros_like(t)
    P_load = np.zeros_like(t)
    P_core = np.zeros_like(t)
    P_copper = np.zeros_like(t)
    P_src = np.zeros_like(t)

    dt = t[1] - t[0]

    for i in range(1, N):
        dI = (V_src[i-1] - V_C[i-1] - I[i-1]*(R_wire + R_core)) * dt / L_core
        I[i] = I[i-1] + dI
        dV_C = I[i-1] * dt / C_res
        V_C[i] = V_C[i-1] + dV_C

        P_src[i] = V_src[i] * I[i]
        P_copper[i] = I[i]**2 * R_wire
        P_core[i] = I[i]**2 * R_core
        P_load[i] = V_C[i]**2 / 10

    W_src = np.sum(P_src) * dt
    W_load = np.sum(P_load) * dt
    W_core = np.sum(P_core) * dt
    W_copper = np.sum(P_copper) * dt
    E_stored = 0.5 * C_res * V_C[-1]**2 + 0.5 * L_core * I[-1]**2
    residual = W_src - (W_load + W_core + W_copper + E_stored)

    df = pd.DataFrame({
        "t": t,
        "v_src": V_src,
        "i": I,
        "v_c": V_C,
        "p_load": P_load,
        "p_core": P_core,
        "p_copper": P_copper,
        "p_src": P_src,
    })

    ledger = {
        "W_src_J": W_src,
        "W_load_J": W_load,
        "W_losses_core_J": W_core,
        "W_losses_copper_J": W_copper,
        "E_stored_J": E_stored,
        "residual_J": residual
    }

    return df, ledger

df_baseline, ledger_baseline = simulate_case(pump=False)
df_chronon, ledger_chronon = simulate_case(pump=True)

df_baseline["case"] = "baseline"
df_chronon["case"] = "chronon"
df = pd.concat([df_baseline, df_chronon], ignore_index=True)

ledger_df = pd.DataFrame([ledger_baseline, ledger_chronon])
ledger_df["case"] = ["baseline", "chronon"]

plt.style.use("dark_background")
plt.figure(figsize=(10, 5))
plt.plot(df_baseline["t"] * 1e6, df_baseline["p_load"], label="Baseline", linewidth=2)
plt.plot(df_chronon["t"] * 1e6, df_chronon["p_load"], label="Chronon Pumped", linewidth=2)
plt.title("Load Power: Baseline vs Chronon-Pumped")
plt.xlabel("Time (μs)")
plt.ylabel("Load Power (W)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
