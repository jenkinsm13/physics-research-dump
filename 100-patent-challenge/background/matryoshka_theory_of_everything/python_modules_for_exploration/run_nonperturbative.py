#!/usr/bin/env python3
# run_nonperturbative.py - Run demonstrations of non-perturbative effects

from matryoshka_nonperturbative import *
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import constants as const

print("=" * 80)
print("MATRYOSHKA TEMPORAL SHELL THEORY - NON-PERTURBATIVE DEMONSTRATIONS")
print("=" * 80)

def run_shell_instanton_demo():
    """Run demonstrations of shell instantons and topological effects."""
    print("\n" + "=" * 80)
    print("SHELL INSTANTONS AND TOPOLOGICAL EFFECTS")
    print("=" * 80)
    
    # Generate instanton configuration
    print("\nGenerating instanton configuration...")
    A_mu, F_munu, action_density = generate_instanton_configuration(grid_size=30)
    
    # Visualize instanton
    print("\nVisualizing instanton...")
    fig = visualize_instanton(A_mu, action_density)
    
    # Calculate winding number
    print("\nCalculating topological winding number...")
    Q = calculate_shell_winding_number(A_mu, 5, 8)
    
    # Calculate instanton action
    print("\nCalculating instanton action...")
    S_inst = calculate_instanton_action(Q, 5, 8, framework['coupling'])
    
    return {
        'A_mu': A_mu,
        'F_munu': F_munu,
        'action_density': action_density,
        'winding_number': Q,
        'instanton_action': S_inst
    }

def run_theta_qcd_demo():
    """Run demonstration of theta QCD parameter calculation."""
    print("\n" + "=" * 80)
    print("THETA QCD PARAMETER CALCULATION")
    print("=" * 80)
    
    # Calculate theta QCD from shell couplings
    theta_qcd = calculate_theta_qcd(framework, max_shell=30)
    
    # Compare with experimental bound
    print(f"\nExperimental bound on theta QCD: |θ| < 10^-10")
    print(f"Calculated value from shell structure: {theta_qcd:.16e}")
    
    # Demonstrate parameter dependency
    print("\nDemonstrating theta QCD dependency on shell parameters...")
    
    # Test different values of lambda_ord (ordinal decay parameter)
    lambda_values = np.linspace(0.05, 0.15, 5)
    theta_results = []
    
    original_lambda = framework['parameters']['lambda_ord']
    
    print("\nLambda value | Theta QCD (raw value)")
    print("-" * 40)
    
    for lambda_val in lambda_values:
        # Temporarily modify framework parameter
        framework['parameters']['lambda_ord'] = lambda_val
        
        # Calculate theta QCD with this parameter
        theta = calculate_theta_qcd(framework, max_shell=15)
        theta_results.append(theta)
        
        # Print raw values with high precision to see what's actually happening
        print(f"λ_ord = {lambda_val:.4f} → θ_QCD = {theta:.16e}")
    
    # Restore original parameter
    framework['parameters']['lambda_ord'] = original_lambda
    
    # Plot dependency with linear scale to show actual values
    plt.figure(figsize=(10, 6))
    plt.plot(lambda_values, theta_results, 'bo-', linewidth=2, label='θ_QCD values')
    plt.axhline(y=1e-10, color='r', linestyle='--', label='Experimental bound')
    
    # Use linear scale instead of logarithmic to show small/zero values
    plt.yscale('linear')
    plt.xlabel('Ordinal Decay Parameter (λ_ord)')
    plt.ylabel('θ_QCD (linear scale)')
    plt.title('Strong CP Parameter Dependency on Shell Coupling Decay')
    plt.grid(True)
    plt.legend()
    plt.savefig('theta_qcd_parameter_dependency.png', dpi=300)
    
    print("\nParameter dependency plot saved as 'theta_qcd_parameter_dependency.png'")
    print("Note: Using linear scale to show actual values")
    
    return {
        'theta_qcd': theta_qcd,
        'lambda_values': lambda_values,
        'theta_results': theta_results
    }

def run_transplanckian_demo():
    """Run demonstration of trans-Planckian regularization."""
    print("\n" + "=" * 80)
    print("TRANS-PLANCKIAN REGULARIZATION")
    print("=" * 80)
    
    # Test trans-Planckian regularization
    tp_results = test_transplanckian_regularization()
    
    # Visualize physical consequences
    print("\nVisualizing physical consequences of trans-Planckian regularization...")
    
    # Extract results
    energy_scales = tp_results['energy_scales']
    form_factors = tp_results['form_factors']
    alpha_EM_eff = tp_results['alpha_EM_eff']
    G_eff = tp_results['G_eff']
    
    # Create figure for extended analysis
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot form factor
    axes[0, 0].loglog(energy_scales, form_factors, 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Energy Scale (E²/M_P²)')
    axes[0, 0].set_ylabel('Form Factor F(x)')
    axes[0, 0].set_title('Trans-Planckian Form Factor')
    axes[0, 0].grid(True, which='both', linestyle='--', alpha=0.7)
    
    # Plot effective couplings
    axes[0, 1].loglog(energy_scales, alpha_EM_eff, 'b-', 
                    label='α_EM', linewidth=2)
    axes[0, 1].loglog(energy_scales, G_eff, 
                    'r-', label='G', linewidth=2)
    axes[0, 1].set_xlabel('Energy Scale (E²/M_P²)')
    axes[0, 1].set_ylabel('Effective Coupling')
    axes[0, 1].set_title('Coupling Strengths vs Energy')
    axes[0, 1].grid(True, which='both', linestyle='--', alpha=0.7)
    axes[0, 1].legend()
    
    # Plot running of αG/αEM ratio (unification parameter)
    axes[1, 0].loglog(energy_scales, 
                    G_eff/(alpha_EM_eff * const.c**4 / (8 * np.pi)), 
                    'g-', linewidth=2)
    axes[1, 0].set_xlabel('Energy Scale (E²/M_P²)')
    axes[1, 0].set_ylabel('αG/αEM Ratio')
    axes[1, 0].set_title('Unified Coupling Ratio')
    axes[1, 0].grid(True, which='both', linestyle='--', alpha=0.7)
    
    # Plot change rates (derivative of couplings)
    d_alpha = np.gradient(np.log(alpha_EM_eff), np.log(energy_scales))
    d_G = np.gradient(np.log(G_eff), np.log(energy_scales))
    axes[1, 1].semilogx(energy_scales, d_alpha, 'b-', label='d ln(α_EM)/d ln(E)', linewidth=2)
    axes[1, 1].semilogx(energy_scales, d_G, 'r-', label='d ln(G)/d ln(E)', linewidth=2)
    axes[1, 1].set_xlabel('Energy Scale (E²/M_P²)')
    axes[1, 1].set_ylabel('Rate of Change')
    axes[1, 1].set_title('Running of Coupling Constants')
    axes[1, 1].grid(True, which='both', linestyle='--', alpha=0.7)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('transplanckian_extended_analysis.png', dpi=300)
    print("\nExtended trans-Planckian analysis saved as 'transplanckian_extended_analysis.png'")
    
    # Calculate unification characteristics
    print("\nAnalyzing coupling unification characteristics:")
    ratio_min = float('inf')
    ratio_min_scale = 0
    
    # Find minimum in the coupling ratio (closest approach to unification)
    ratio = G_eff/(alpha_EM_eff * const.c**4 / (8 * np.pi))
    min_idx = np.argmin(ratio)
    
    print(f"Closest approach to unification at E²/M_P² ≈ {energy_scales[min_idx]:.4e}")
    print(f"αG/αEM ratio at this scale: {ratio[min_idx]:.6e}")
    
    return tp_results

def run_information_theory_demo():
    """Run demonstration of information-theoretic foundation."""
    print("\n" + "=" * 80)
    print("INFORMATION-THEORETIC FOUNDATION")
    print("=" * 80)
    
    # Create different density matrices for testing
    print("\nCalculating information-theoretic action for different quantum states...")
    
    dim = 10  # Dimension of Hilbert space for demonstration
    
    # Create simple position and momentum operators
    x_ops = []
    p_ops = []
    for i in range(dim):
        # Position eigenstate projectors
        x_i = np.zeros((dim, dim))
        x_i[i, i] = 1.0
        x_ops.append(x_i)
        
        # Momentum eigenstate projectors (simplified discrete Fourier transform relation)
        p_i = np.zeros((dim, dim), dtype=complex)
        for j in range(dim):
            for k in range(dim):
                p_i[j, k] = np.exp(2j * np.pi * i * (j-k) / dim) / np.sqrt(dim)
        p_ops.append(p_i)
    
    observables = {
        'position': x_ops,
        'momentum': p_ops
    }
    
    # 1. Maximally mixed state (ρ = I/d)
    rho_mixed = np.eye(dim) / dim
    
    # 2. Pure state (ρ = |ψ⟩⟨ψ|)
    psi = np.zeros(dim)
    psi[0] = 1.0  # Ground state
    rho_pure = np.outer(psi, psi.conj())
    
    # 3. Thermal state (ρ ∝ e^(-βH))
    H = np.diag(np.arange(dim))  # Simple Hamiltonian with equally spaced levels
    beta = 0.5  # Temperature parameter
    rho_thermal = np.diag(np.exp(-beta * np.arange(dim)))
    rho_thermal /= np.trace(rho_thermal)  # Normalize
    
    # 4. Coherent superposition state
    n = 3  # Number of states in superposition
    psi_super = np.zeros(dim, dtype=complex)
    for i in range(n):
        psi_super[i] = np.exp(2j * np.pi * i / n) / np.sqrt(n)
    rho_super = np.outer(psi_super, psi_super.conj())
    
    # Calculate information-theoretic action for each state
    print("\nMaximally mixed state:")
    action_mixed = information_theoretic_action(framework, rho_mixed, observables)
    
    print("\nPure state:")
    action_pure = information_theoretic_action(framework, rho_pure, observables)
    
    print("\nThermal state:")
    action_thermal = information_theoretic_action(framework, rho_thermal, observables)
    
    print("\nCoherent superposition state:")
    action_super = information_theoretic_action(framework, rho_super, observables)
    
    # Summarize results
    print("\nInformation-theoretic action summary:")
    print(f"Maximally mixed state: {action_mixed:.6f}")
    print(f"Pure state: {action_pure:.6f}")
    print(f"Thermal state: {action_thermal:.6f}")
    print(f"Coherent superposition: {action_super:.6f}")
    
    # Plot action values
    states = ['Mixed', 'Pure', 'Thermal', 'Superposition']
    actions = [action_mixed, action_pure, action_thermal, action_super]
    
    plt.figure(figsize=(10, 6))
    plt.bar(states, actions, color=['blue', 'green', 'red', 'purple'])
    plt.ylabel('Information-Theoretic Action')
    plt.title('Information-Theoretic Action for Different Quantum States')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('information_action_comparison.png', dpi=300)
    
    print("\nInformation action comparison saved as 'information_action_comparison.png'")
    
    return {
        'states': states,
        'actions': actions,
        'density_matrices': {
            'mixed': rho_mixed,
            'pure': rho_pure,
            'thermal': rho_thermal,
            'superposition': rho_super
        }
    }

def run_uniqueness_demo():
    """Run demonstration of framework uniqueness and discrete-continuous transition."""
    print("\n" + "=" * 80)
    print("FRAMEWORK UNIQUENESS AND DISCRETE-CONTINUOUS TRANSITION")
    print("=" * 80)
    
    # Verify framework uniqueness
    uniqueness = verify_framework_uniqueness()
    
    # Demonstrate discrete-continuous transition
    dc_transition = demonstrate_discrete_continuous_transition(framework)
    
    return {
        'uniqueness': uniqueness,
        'dc_transition': dc_transition
    }

def run_all_demos():
    """Run all non-perturbative demonstrations."""
    print("\n" + "=" * 80)
    print("RUNNING ALL NON-PERTURBATIVE DEMONSTRATIONS")
    print("=" * 80)
    
    start_time = time.time()
    
    # Run individual demonstrations
    print("\nRunning Shell Instanton Demo...")
    instanton_results = run_shell_instanton_demo()
    
    print("\nRunning Theta QCD Demo...")
    theta_results = run_theta_qcd_demo()
    
    print("\nRunning Trans-Planckian Demo...")
    tp_results = run_transplanckian_demo()
    
    print("\nRunning Information Theory Demo...")
    info_results = run_information_theory_demo()
    
    print("\nRunning Uniqueness Demo...")
    uniqueness_results = run_uniqueness_demo()
    
    end_time = time.time()
    
    # Summarize results
    print("\n" + "=" * 80)
    print("SUMMARY OF NON-PERTURBATIVE DEMONSTRATIONS")
    print("=" * 80)
    
    print(f"\nTotal runtime: {end_time - start_time:.2f} seconds")
    
    print("\n1. Shell Instantons and Topological Effects:")
    print(f"   - Winding number: {instanton_results['winding_number']:.4f}")
    print(f"   - Instanton action: {instanton_results['instanton_action']:.6e}")
    
    print("\n2. Theta QCD Parameter:")
    print(f"   - Calculated value: {theta_results['theta_qcd']:.16e}")
    print(f"   - Experimental bound: < 10^-10")
    
    print("\n3. Trans-Planckian Regularization:")
    min_form_factor = np.min(tp_results['form_factors'])
    min_idx = np.argmin(tp_results['form_factors'])
    min_scale = tp_results['energy_scales'][min_idx]
    print(f"   - Minimum form factor: {min_form_factor:.6e} at E²/M_P² ≈ {min_scale:.4e}")
    
    print("\n4. Information-Theoretic Foundation:")
    for i, state in enumerate(info_results['states']):
        print(f"   - {state} state action: {info_results['actions'][i]:.6f}")
    
    print("\n5. Framework Uniqueness:")
    num_alternatives = len(uniqueness_results['uniqueness']['alternative_theories'])
    print(f"   - {num_alternatives} alternative theories tested, all violate constraints")
    print(f"   - Discrete-to-continuous transition measure: {uniqueness_results['dc_transition']['discreteness_measure']:.6f}")
    
    print("\n" + "=" * 80)
    print("NON-PERTURBATIVE DEMONSTRATIONS COMPLETE")
    print("=" * 80)
    
    # Combine all results
    all_results = {
        'instanton_results': instanton_results,
        'theta_results': theta_results,
        'tp_results': tp_results,
        'info_results': info_results,
        'uniqueness_results': uniqueness_results,
        'runtime': end_time - start_time
    }
    
    return all_results

# Run all demonstrations if executed directly
if __name__ == "__main__":
    all_results = run_all_demos() 